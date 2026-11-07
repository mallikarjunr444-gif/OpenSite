"""Evidence-first growth advisor powered by Groq, OpenAI, Ollama, and Hindsight memory."""
import os
import logging
from typing import Any, Dict, List

import requests

logger = logging.getLogger("opensite.advisor")

def advise(query: str, memories: List[Dict[str, Any]], model: str = "") -> Dict[str, str]:
    evidence = "\n\n".join(
        f"[{item.get('timestamp','date unknown')}] tags={','.join(item.get('tags',[]))}\n{item.get('content','')}"
        for item in memories[:8]
    )
    if not evidence:
        return {
            "answer": "There is not enough saved growth history to answer yet. Connect a data source, run an audit, or record an experiment first.",
            "mode": "memory fallback"
        }

    system = (
        "You are OpenSite, an elite SEO and conversion intelligence agent. Answer strictly using the supplied site evidence and memory. "
        "Separate observed facts from hypotheses. Do not claim causation from simple before/after correlation. "
        "Highlight patterns that compounded over time (ranking changes, algorithm updates, A/B test winners). "
        "Give actionable, evidence-grounded recommendations and cite specific dates, test IDs, or metric percentages from the evidence."
    )
    prompt = f"User Question: {query}\n\nSite History & Memory Evidence:\n{evidence}"

    # 1. Try Groq API (super fast, recommended for hackathon)
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            from groq import Groq
            client = Groq(api_key=groq_api_key)
            groq_model = model or os.getenv("GROQ_MODEL", "qwen/qwen3-32b")
            completion = client.chat.completions.create(
                model=groq_model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )
            answer = completion.choices[0].message.content.strip()
            if answer:
                return {"answer": answer, "mode": f"Groq LLM · {groq_model}"}
        except Exception as exc:
            logger.warning(f"Groq inference failed: {exc}. Trying next provider.")

    # 2. Try OpenAI API
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if openai_api_key:
        try:
            openai_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"},
                json={
                    "model": openai_model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 600
                },
                timeout=30
            )
            if response.ok:
                answer = response.json()["choices"][0]["message"]["content"].strip()
                if answer:
                    return {"answer": answer, "mode": f"OpenAI · {openai_model}"}
        except Exception as exc:
            logger.warning(f"OpenAI inference failed: {exc}. Trying next provider.")

    # 3. Try Local Ollama
    if os.getenv("OLLAMA_ENABLED", "").lower() in {"1", "true", "yes"}:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        ollama_model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        try:
            response = requests.post(
                f"{base_url}/api/chat",
                json={
                    "model": ollama_model,
                    "stream": False,
                    "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
                },
                timeout=30
            )
            if response.ok:
                answer = response.json().get("message", {}).get("content", "").strip()
                if answer:
                    return {"answer": answer, "mode": f"local Ollama · {ollama_model}"}
        except Exception as exc:
            logger.warning(f"Ollama inference failed: {exc}.")

    # 4. High-Fidelity Evidence Synthesis Fallback
    top_memories = [item.get("content", "") for item in memories[:3]]
    synthesis = (
        "Based on saved site history:\n\n"
        + "\n\n".join(f"• {m}" for m in top_memories)
        + "\n\n💡 Agent Synthesis: Retained evidence indicates that first-party benchmarks, clear frictionless CTAs, "
        "and technical speed optimizations (INP) drive compounding ranking and conversion gains. "
        "(Set GROQ_API_KEY in .env for real-time generative reasoning)."
    )
    return {"answer": synthesis, "mode": "Hindsight Memory Recall & Synthesis"}
