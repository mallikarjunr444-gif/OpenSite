"""Evidence-first growth advisor with optional local Ollama inference."""
import os
from typing import Any, Dict, List

import requests


def advise(query: str, memories: List[Dict[str, Any]], model: str = "") -> Dict[str, str]:
    model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    evidence = "\n\n".join(
        f"[{item.get('timestamp','date unknown')}] tags={','.join(item.get('tags',[]))}\n{item.get('content','')}"
        for item in memories[:8]
    )
    if not evidence:
        return {"answer":"There is not enough saved growth history to answer yet. Connect a data source, run an audit, or record an experiment first.","mode":"memory fallback"}
    system = (
        "You are OpenSite, an SEO and conversion analyst. Answer only from the supplied site evidence. "
        "Separate observed facts from hypotheses. Do not claim causation from simple before/after correlation. "
        "When data is insufficient, say so. Give one concise recommendation and cite the relevant dates or experiment names."
    )
    prompt = f"Question: {query}\n\nSite evidence:\n{evidence}"
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    if os.getenv("OLLAMA_ENABLED", "").lower() in {"1", "true", "yes"}:
        try:
            response=requests.post(f"{base_url}/api/chat",json={"model":model,"stream":False,"messages":[{"role":"system","content":system},{"role":"user","content":prompt}]},timeout=45)
            response.raise_for_status()
            answer=response.json().get("message",{}).get("content","").strip()
            if answer: return {"answer":answer,"mode":f"local Ollama · {model}"}
        except (requests.RequestException,ValueError) as exc:
            return {"answer":"Local Ollama is enabled but not reachable. OpenSite's relevant saved evidence is shown below.\n\n"+"\n\n".join(item.get("content","") for item in memories[:4]),"mode":f"memory fallback · {str(exc)[:120]}"}
    return {"answer":"Based on saved history:\n\n"+"\n\n".join(item.get("content","") for item in memories[:4]),"mode":"memory recall · enable Ollama for generated synthesis"}
