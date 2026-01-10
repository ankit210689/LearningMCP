import os
import json
import tempfile
from pathlib import Path
from typing import Optional

DATA_DIR = Path(os.getenv("MCP_DATA_DIR", "./data")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _safe_path(path: str) -> str:
    # simple sanitization: replace .. and slashes
    safe = path.replace("..", "").replace("/", "_")
    return safe


def store(path: str, obj: dict) -> None:
    safe = _safe_path(path)
    target = DATA_DIR / f"{safe}.json"
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(DATA_DIR)) as tf:
        json.dump(obj, tf, sort_keys=True, separators=(",", ":"))
        tmpname = tf.name
    # atomic replace
    os.replace(tmpname, target)


def load(path: str) -> Optional[dict]:
    safe = _safe_path(path)
    target = DATA_DIR / f"{safe}.json"
    if not target.exists():
        return None
    with open(target, "r") as f:
        return json.load(f)

