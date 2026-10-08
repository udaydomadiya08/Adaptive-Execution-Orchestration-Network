"""Dependency-free HTTP provider adapters for AEON-3.

No credential is bundled. The adapter fails closed when the relevant environment variable is absent.
It is intentionally compatible with OpenAI-style chat/completions APIs so the same AEON harness can
be evaluated against multiple providers without changing the substrate.
"""
from __future__ import annotations
import json, os, time, urllib.request
from typing import Any, Dict, List, Optional
from aeon3_sidecar_v2 import Completion

class HTTPProvider:
    def __init__(self, name: str, base_url: str, model: str, api_key_env: str):
        self.name, self.base_url, self.model, self.api_key_env = name, base_url.rstrip('/'), model, api_key_env
    def _key(self):
        key=os.getenv(self.api_key_env)
        if not key: raise RuntimeError(f"{self.api_key_env} is not set; refusing an unauthenticated experiment")
        return key
    def complete(self, messages: List[Dict[str, Any]], tools=None, effort="fixed", budget=None):
        payload={"model":self.model,"messages":messages}
        if tools: payload["tools"]=[{"type":"function","function":t} for t in tools]
        if effort not in (None,"fixed"):
            # Provider-specific effort is deliberately opt-in via a raw environment setting later.
            payload["reasoning_effort"]=effort
        if budget and budget.get("max_output_tokens") is not None:
            payload["max_tokens"]=int(budget["max_output_tokens"])
        data=json.dumps(payload).encode()
        req=urllib.request.Request(self.base_url+"/chat/completions",data=data,method="POST",
            headers={"Authorization":"Bearer "+self._key(),"Content-Type":"application/json"})
        t=time.perf_counter()
        with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
        latency=time.perf_counter()-t
        choice=raw["choices"][0]; msg=choice.get("message",{})
        usage=raw.get("usage",{}) or {}
        calls=[]
        for tc in msg.get("tool_calls",[]) or []:
            fn=tc.get("function",{})
            try: args=json.loads(fn.get("arguments") or "{}")
            except Exception: args={"_raw":fn.get("arguments")}
            calls.append({"name":fn.get("name",""),"arguments":args})
        return Completion(
            text=msg.get("content") or "", model=raw.get("model",self.model),
            input_tokens=int(usage.get("prompt_tokens",0) or 0),
            output_tokens=int(usage.get("completion_tokens",0) or 0),
            reasoning_tokens=usage.get("reasoning_tokens"), latency_s=latency,
            cost_usd=None, finish_reason=choice.get("finish_reason","stop"),
            tool_calls=calls, raw_usage=usage)


def deepseek(model="deepseek-v4-pro"):
    return HTTPProvider("deepseek","https://api.deepseek.com",model,"DEEPSEEK_API_KEY")

def openai(model="gpt-6.1-sol"):
    return HTTPProvider("openai","https://api.openai.com/v1",model,"OPENAI_API_KEY")
