"""FastAPI REST API and Band AI Desktop bridge for OpenSite."""
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import settings
from app.hindsight_manager import hindsight_mgr
from app.growth_agent import advise
from app.site_auditor import crawl_site
from app.experiment_analysis import analyze_two_variant
from app.seed_seo_data import SEED_SITES, seed_seo_memories
from app.site_registry import load_custom_sites, add_site

app = FastAPI(
    title="OpenSite API",
    description="Autonomous SEO & Conversion Intelligence Agent powered by Hindsight Persistent Memory",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to ensure baseline memory is seeded
@app.on_event("startup")
async def startup_event():
    existing = set(hindsight_mgr.get_all_banks())
    if any(site["site_id"] not in existing for site in SEED_SITES):
        seed_seo_memories()

# ── Pydantic Request Models ──
class AdviseRequest(BaseModel):
    site_id: str = Field(..., example="opensite_io")
    question: str = Field(..., example="What drove our best organic rankings and conversions?")
    model: Optional[str] = None

class RetainRequest(BaseModel):
    site_id: str = Field(..., example="opensite_io")
    content: str = Field(..., example="[A/B TEST] Hero CTA test lifted conversion by 34%")
    tags: Optional[List[str]] = Field(default_factory=list, example=["ab_test", "cro"])
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class RecallRequest(BaseModel):
    site_id: str = Field(..., example="opensite_io")
    query: str = Field(..., example="pricing page conversion")
    tags: Optional[List[str]] = None
    limit: int = Field(default=6, ge=1, le=20)

class ReflectRequest(BaseModel):
    site_id: str = Field(..., example="opensite_io")
    query: str = Field(default="Synthesize key growth and ranking patterns for this property", example="pricing")

class AuditRequest(BaseModel):
    url: str = Field(..., example="https://opensite.io")
    max_pages: int = Field(default=15, ge=1, le=50)

class ABTestRequest(BaseModel):
    control_visitors: int = Field(..., ge=1, example=1200)
    control_conversions: int = Field(..., ge=0, example=48)
    variant_visitors: int = Field(..., ge=1, example=1250)
    variant_conversions: int = Field(..., ge=0, example=72)
    alpha: float = Field(default=0.05)

class BandAIInvokeRequest(BaseModel):
    tool: str = Field(..., example="opensite_advise")
    parameters: Dict[str, Any] = Field(default_factory=dict)

# ── Core Endpoints ──
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "hindsight_backend": "Hindsight Cloud / Persistent Memory Active"
    }

@app.get("/api/sites")
def list_sites():
    sites = {s["site_id"]: s for s in SEED_SITES}
    sites.update({s["site_id"]: s for s in load_custom_sites()})
    result = []
    for s_id, s in sites.items():
        memories = hindsight_mgr.get_bank_memories(s_id)
        result.append({
            "site_id": s_id,
            "domain": s.get("domain", s_id),
            "title": s.get("title", s_id),
            "memory_count": len(memories) if memories else len(s.get("history", []))
        })
    return {"sites": result}

@app.get("/api/memories/{site_id}")
def get_memories(site_id: str):
    memories = hindsight_mgr.get_bank_memories(site_id)
    return {"site_id": site_id, "count": len(memories), "memories": memories}

@app.post("/api/advise")
def advise_endpoint(req: AdviseRequest):
    evidence = hindsight_mgr.recall(req.site_id, req.question, limit=8)
    advice = advise(req.question, evidence, model=req.model or "")
    return {
        "site_id": req.site_id,
        "question": req.question,
        "answer": advice["answer"],
        "mode": advice["mode"],
        "evidence_count": len(evidence),
        "evidence": evidence
    }

@app.post("/api/retain")
def retain_endpoint(req: RetainRequest):
    res = hindsight_mgr.retain(
        bank_id=req.site_id,
        content=req.content,
        timestamp=req.timestamp,
        tags=req.tags,
        metadata=req.metadata
    )
    return {"status": "success", "result": res}

@app.post("/api/recall")
def recall_endpoint(req: RecallRequest):
    results = hindsight_mgr.recall(
        bank_id=req.site_id,
        query=req.query,
        tags=req.tags,
        limit=req.limit
    )
    return {"site_id": req.site_id, "query": req.query, "count": len(results), "results": results}

@app.post("/api/reflect")
def reflect_endpoint(req: ReflectRequest):
    reflection = hindsight_mgr.reflect(bank_id=req.site_id, query=req.query)
    return {"site_id": req.site_id, "query": req.query, "reflection": reflection}

@app.post("/api/audit")
def audit_endpoint(req: AuditRequest):
    try:
        audit_res = crawl_site(req.url, max_pages=req.max_pages)
        return {"status": "success", "audit": audit_res}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/api/ab-test")
def ab_test_endpoint(req: ABTestRequest):
    try:
        analysis = analyze_two_variant(
            req.control_visitors,
            req.control_conversions,
            req.variant_visitors,
            req.variant_conversions,
            req.alpha
        )
        return {"status": "success", "analysis": analysis}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

# ── Band AI Desktop Bridge ──
@app.get("/api/band-ai/manifest")
def band_ai_manifest():
    """Manifest conforming to Band AI tool standards."""
    return {
        "name": "OpenSite Growth Intelligence",
        "version": settings.APP_VERSION,
        "description": "Autonomous SEO and conversion intelligence agent that learns using Hindsight memory.",
        "tools": [
            {
                "name": "opensite_advise",
                "description": "Ask OpenSite for SEO and conversion guidance grounded in past site memories.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "site_id": {"type": "string", "description": "Tracked property ID (e.g. 'opensite_io')"},
                        "question": {"type": "string", "description": "The question to investigate using past memory"}
                    },
                    "required": ["site_id", "question"]
                }
            },
            {
                "name": "opensite_recall",
                "description": "Search historical SEO, ranking, and A/B test memories using Hindsight TEMPR retrieval.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "site_id": {"type": "string", "description": "Tracked property ID"},
                        "query": {"type": "string", "description": "Search term or concept"}
                    },
                    "required": ["site_id", "query"]
                }
            },
            {
                "name": "opensite_retain",
                "description": "Store an experiment outcome, ranking update, or SEO signal into durable Hindsight memory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "site_id": {"type": "string", "description": "Tracked property ID"},
                        "content": {"type": "string", "description": "Detailed description of the change, date, and outcome"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Category tags"}
                    },
                    "required": ["site_id", "content"]
                }
            }
        ]
    }

@app.post("/api/band-ai/invoke")
def band_ai_invoke(req: BandAIInvokeRequest):
    """Executes a Band AI Desktop tool call."""
    tool = req.tool
    p = req.parameters
    if tool == "opensite_advise":
        site_id = p.get("site_id", "opensite_io")
        question = p.get("question", "")
        evidence = hindsight_mgr.recall(site_id, question, limit=8)
        res = advise(question, evidence)
        return {"result": res}
    elif tool == "opensite_recall":
        site_id = p.get("site_id", "opensite_io")
        query = p.get("query", "")
        memories = hindsight_mgr.recall(site_id, query, limit=6)
        return {"result": memories}
    elif tool == "opensite_retain":
        site_id = p.get("site_id", "opensite_io")
        content = p.get("content", "")
        tags = p.get("tags", [])
        ret = hindsight_mgr.retain(site_id, content, tags=tags)
        return {"result": ret}
    else:
        raise HTTPException(status_code=404, detail=f"Unknown tool '{tool}'")
