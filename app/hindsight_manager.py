"""Persistent local memory with an optional Hindsight Cloud mirror."""
import datetime
import json
import logging
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import settings

logger = logging.getLogger("opensite.hindsight")

try:
    from hindsight_client import Hindsight
    HINDSIGHT_SDK_AVAILABLE = True
except ImportError:
    HINDSIGHT_SDK_AVAILABLE = False


class LocalMemoryStore:
    """Small durable memory store used when a remote Hindsight bank is unavailable."""

    def __init__(self, path: Optional[Path] = None):
        configured_path = os.getenv("OPENSITE_MEMORY_PATH")
        self.path = path or (Path(configured_path).expanduser() if configured_path else Path(__file__).resolve().parent / "data" / "memories.json")
        self.banks: Dict[str, List[Dict[str, Any]]] = {}
        self._load()

    def _load(self) -> None:
        try:
            if self.path.exists():
                data = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    self.banks = {str(k): v for k, v in data.items() if isinstance(v, list)}
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Could not load local OpenSite memories: %s", exc)

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(self.banks, ensure_ascii=False, indent=2), encoding="utf-8")
        temp_path.replace(self.path)

    def retain(self, bank_id: str, content: str, timestamp: Optional[str] = None,
               tags: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        bank = self.banks.setdefault(bank_id, [])
        ts = timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat()
        item = {
            "id": f"mem_{uuid.uuid4().hex}",
            "content": content,
            "timestamp": ts,
            "tags": tags or [],
            "metadata": metadata or {},
        }
        bank.append(item)
        self._save()
        return {"status": "success", "id": item["id"], "bank_id": bank_id}

    def recall(self, bank_id: str, query: str, tags: Optional[List[str]] = None, limit: int = 6) -> List[Dict[str, Any]]:
        memories = self.banks.get(bank_id, [])
        stop_words = {"what", "when", "where", "which", "have", "does", "did", "from", "with", "that", "this", "your", "our", "the", "and", "for", "has", "been", "was", "were", "into", "about"}
        query_words = {w for w in re.findall(r"\w+", query.lower()) if len(w) > 2 and w not in stop_words}
        query_tags = {t.lower() for t in (tags or [])}
        scored = []
        for index, mem in enumerate(memories):
            content_words = set(re.findall(r"\w+", mem.get("content", "").lower()))
            tag_words = set(re.findall(r"\w+", " ".join(mem.get("tags", [])).lower()))
            overlap = len(query_words & (content_words | tag_words))
            tag_match = bool(query_tags & {t.lower() for t in mem.get("tags", [])})
            if not query_words and not query_tags:
                overlap = 1
            score = overlap * 2.0 + (3.0 if tag_match else 0.0) + index * 0.0001
            if score:
                scored.append((score, mem))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [mem for _, mem in scored[:limit]]

    def reflect(self, bank_id: str, query: str) -> str:
        memories = self.recall(bank_id, query, limit=8)
        if not memories:
            return "No matching growth history yet. Record an experiment or connect a property to build useful memory."
        lines = [f"OpenSite found {len(memories)} relevant growth signals:"]
        lines.extend(f"- {item['content']}" for item in memories[:5])
        return "\n".join(lines)

    def get_all(self, bank_id: str) -> List[Dict[str, Any]]:
        return self.banks.get(bank_id, [])

    def list_banks(self) -> List[str]:
        return list(self.banks)


class HindsightManager:
    """Use local durable memory and mirror writes/queries to Hindsight when configured."""

    def __init__(self):
        self.local_store = LocalMemoryStore()
        self.client: Optional[Any] = None
        if HINDSIGHT_SDK_AVAILABLE and settings.HINDSIGHT_API_KEY:
            try:
                self.client = Hindsight(base_url=settings.HINDSIGHT_BASE_URL, api_key=settings.HINDSIGHT_API_KEY, timeout=30.0)
            except Exception as exc:
                logger.warning("Hindsight connection unavailable; using local memory: %s", exc)

    def retain(self, bank_id: str, content: str, timestamp: Optional[str] = None,
               tags: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        result = self.local_store.retain(bank_id, content, timestamp, tags, metadata)
        if self.client:
            try:
                self.client.retain(bank_id=bank_id, content=content, timestamp=timestamp, tags=tags, metadata=metadata)
                result["status"] = "retained_remote"
            except Exception as exc:
                logger.warning("Remote retain failed; local memory is safe: %s", exc)
        return result

    def recall(self, bank_id: str, query: str, tags: Optional[List[str]] = None, limit: int = 6) -> List[Dict[str, Any]]:
        if self.client:
            try:
                response = self.client.recall(bank_id=bank_id, query=query, tags=tags)
                remote = getattr(response, "memories", [])
                if remote:
                    return [{"content": getattr(item, "content", str(item)), "timestamp": getattr(item, "timestamp", ""),
                             "tags": getattr(item, "tags", []) or [], "metadata": getattr(item, "metadata", {}) or {}}
                            for item in remote[:limit]]
            except Exception as exc:
                logger.warning("Remote recall failed; using local memory: %s", exc)
        return self.local_store.recall(bank_id, query, tags=tags, limit=limit)

    def reflect(self, bank_id: str, query: str) -> str:
        if self.client:
            try:
                result = self.client.reflect(bank_id=bank_id, query=query)
                text = getattr(result, "text", None) or getattr(result, "content", None)
                if text:
                    return str(text)
            except Exception as exc:
                logger.warning("Remote reflection failed; using local synthesis: %s", exc)
        return self.local_store.reflect(bank_id, query)

    def get_bank_memories(self, bank_id: str) -> List[Dict[str, Any]]:
        return self.local_store.get_all(bank_id)

    def get_all_banks(self) -> List[str]:
        return self.local_store.list_banks()


hindsight_mgr = HindsightManager()
