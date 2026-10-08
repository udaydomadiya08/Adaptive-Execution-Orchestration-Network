"""AEON-3 v3: auditable persistent sidecar substrate.

Research-only. The state is explicitly serialized into every subsequent model transition;
no hidden provider memory is assumed. Tool results and verifier decisions are recorded.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple
import hashlib, json, time

@dataclass
class Completion:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    reasoning_tokens: Optional[int] = None
    latency_s: float = 0.0
    cost_usd: Optional[float] = None
    finish_reason: str = "stop"
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    raw_usage: Dict[str, Any] = field(default_factory=dict)
    def validate(self):
        if not self.model or min(self.input_tokens,self.output_tokens)<0: raise ValueError("invalid completion")
        if self.reasoning_tokens is not None and self.reasoning_tokens<0: raise ValueError("invalid reasoning tokens")
        if self.latency_s<0 or (self.cost_usd is not None and self.cost_usd<0): raise ValueError("invalid accounting")
        return self

class Provider(Protocol):
    name: str
    def complete(self, messages: List[Dict[str,Any]], tools=None, effort="fixed", budget=None) -> Completion: ...

@dataclass
class PersistentState:
    goal: str
    facts: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, str] = field(default_factory=dict)
    plan: List[str] = field(default_factory=list)
    completed_steps: List[str] = field(default_factory=list)
    uncertainty: float = 0.0
    verifier_status: str = "unverified"
    transition_index: int = 0
    def snapshot(self): return asdict(self)

def state_hash(s: PersistentState):
    return hashlib.sha256(json.dumps(s.snapshot(),sort_keys=True,separators=(",",":")).encode()).hexdigest()[:16]

def state_message(s: PersistentState) -> Dict[str,str]:
    # Explicit, auditable state channel. No hidden memory.
    return {"role":"system","content":"AEON_PERSISTENT_STATE\n"+json.dumps(s.snapshot(),sort_keys=True)}

@dataclass
class Tool:
    name: str; description: str; fn: Callable[[Dict[str,Any]],Any]; schema: Dict[str,Any]
    def execute(self,args):
        t=time.perf_counter(); result=self.fn(args); return result,time.perf_counter()-t

@dataclass
class Trace:
    task_id:str; mode:str; model:str; actions:List[Dict[str,Any]]; final_text:str
    total_input_tokens:int; total_output_tokens:int; total_reasoning_tokens:int
    total_model_calls:int; total_tool_calls:int; total_latency_s:float
    total_cost_usd:Optional[float]; state_hashes:List[str]; valid:bool=True; invalid_reason:Optional[str]=None
    def validate(self):
        if self.mode not in {"baseline","aeon"}: raise ValueError("bad mode")
        if self.total_model_calls != sum(a.get("kind")=="model_call" for a in self.actions): raise ValueError("model accounting")
        if self.total_tool_calls != sum(a.get("kind")=="tool_call" for a in self.actions): raise ValueError("tool accounting")
        if any(a.get("precomputed") for a in self.actions if a.get("kind")=="model_call"): raise ValueError("precompute")
        return self

class BaselineRunner:
    def __init__(self,provider,effort="fixed"): self.provider,self.effort=provider,effort
    def run(self,task_id,messages,tools=None):
        t=time.perf_counter(); c=self.provider.complete(messages,tools=tools,effort=self.effort); elapsed=time.perf_counter()-t; c.validate()
        a={"kind":"model_call","index":0,"model":c.model,"input_tokens":c.input_tokens,"output_tokens":c.output_tokens,"reasoning_tokens":c.reasoning_tokens or 0,"latency_s":c.latency_s,"cost_usd":c.cost_usd,"precomputed":False}
        return Trace(task_id,"baseline",c.model,[a],c.text,c.input_tokens,c.output_tokens,c.reasoning_tokens or 0,1,len(c.tool_calls),elapsed,c.cost_usd,[],True,None).validate()

class AEONRunner:
    def __init__(self,provider,tools,max_model_calls=6,effort="fixed",verifier:Optional[Callable[[str,PersistentState],Tuple[bool,str]]]=None):
        self.provider,self.tools,self.max_model_calls,self.effort,self.verifier=provider,tools,max_model_calls,effort,verifier
    def run(self,task_id,messages,goal,memory=None):
        s=PersistentState(goal=goal,memory=dict(memory or {})); actions=[]; hashes=[state_hash(s)]; history=list(messages)
        total_in=total_out=total_reason=0; total_latency=0.; total_cost=0.; cost_known=True; final=""; model="unknown"
        base_system={"role":"system","content":"You are operating inside AEON. Use ONLY the explicit persistent state supplied by the system. You may answer or request a listed tool. Never assume unseen results."}
        for step in range(self.max_model_calls):
            s.transition_index=step
            prompt=[base_system,state_message(s)]+history
            t=time.perf_counter(); c=self.provider.complete(prompt,tools=[{"name":x.name,"description":x.description,"parameters":x.schema} for x in self.tools.values()],effort=self.effort,budget={"remaining_model_calls":self.max_model_calls-step}); elapsed=time.perf_counter()-t; c.validate()
            model=c.model; total_in+=c.input_tokens; total_out+=c.output_tokens; total_reason+=c.reasoning_tokens or 0; total_latency+=elapsed
            if c.cost_usd is None: cost_known=False
            else: total_cost+=c.cost_usd
            actions.append({"kind":"model_call","index":step,"model":c.model,"input_tokens":c.input_tokens,"output_tokens":c.output_tokens,"reasoning_tokens":c.reasoning_tokens or 0,"latency_s":c.latency_s,"cost_usd":c.cost_usd,"precomputed":False,"state_hash_before":state_hash(s)})
            final=c.text
            if not c.tool_calls:
                s.completed_steps.append("model_answer")
                ok=True; verdict="no_verifier"
                if self.verifier is not None: ok,verdict=self.verifier(final,s)
                s.verifier_status=verdict
                actions.append({"kind":"verification","accepted":ok,"status":verdict})
                hashes.append(state_hash(s))
                if ok: break
                history += [{"role":"assistant","content":c.text},{"role":"user","content":"Verifier rejected the answer. Reconsider using the persistent state and provide a corrected answer."}]
                continue
            for tc in c.tool_calls:
                name=tc.get("name"); args=tc.get("arguments") or {}
                if name not in self.tools: raise ValueError("unavailable tool: "+str(name))
                result,lat=self.tools[name].execute(args); s.facts[name]=result; s.completed_steps.append(name)
                actions.append({"kind":"tool_call","name":name,"arguments":args,"latency_s":lat,"result_digest":hashlib.sha256(json.dumps(result,sort_keys=True,default=str).encode()).hexdigest()[:16]})
                history += [{"role":"assistant","content":c.text},{"role":"tool","name":name,"content":json.dumps(result,default=str)}]
                hashes.append(state_hash(s))
        else:
            s.verifier_status="budget_exhausted"; actions.append({"kind":"budget_exhausted"})
        tr=Trace(task_id,"aeon",model,actions,final,total_in,total_out,total_reason,sum(a.get("kind")=="model_call" for a in actions),sum(a.get("kind")=="tool_call" for a in actions),total_latency,total_cost if cost_known else None,hashes,True,None)
        return tr.validate()

def save_trace(path,trace):
    with open(path,"w") as f: json.dump(asdict(trace),f,sort_keys=True,indent=2)

if __name__=="__main__":
    class P:
        name="scripted-foundation"
        def complete(self,messages,tools=None,effort="fixed",budget=None):
            state=next((m["content"] for m in messages if m.get("content","").startswith("AEON_PERSISTENT_STATE")),"")
            if "lookup_done" not in state and tools:
                return Completion("request lookup",self.name,100,4,0,.001,0.,tool_calls=[{"name":tools[0]["name"],"arguments":{}}])
            return Completion("final with persistent state",self.name,100,8,0,.001,0.)
    p=P(); tool=Tool("lookup","lookup",lambda a:{"lookup_done":True,"value":42},{"type":"object","properties":{}})
    tr=AEONRunner(p,{tool.name:tool}).run("smoke",[{"role":"user","content":"solve"}],"smoke")
    assert tr.valid and tr.total_model_calls==2 and tr.total_tool_calls==1 and len(set(tr.state_hashes))>1
    print("AEON-3 v3 persistent-state audit: PASS")
    print(json.dumps({"calls":tr.total_model_calls,"tools":tr.total_tool_calls,"state_transitions":len(tr.state_hashes)-1},indent=2))
