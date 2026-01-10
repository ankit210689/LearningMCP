from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
import uvicorn
import os
import time
from typing import Optional

from mcp import storage, signing

app = FastAPI(title="MCP Simple Server")


@app.get("/mcp/health")
def health():
    return {"status": "ok", "time": int(time.time())}


@app.post("/mcp/publish")
async def publish(request: Request, x_mcp_signature: Optional[str] = Header(None), x_mcp_ts: Optional[str] = Header(None)):
    payload = await request.json()
    # expect {"path": "bundle:...", "bundle": {...}}
    path = payload.get("path")
    bundle = payload.get("bundle")
    if not path or bundle is None:
        raise HTTPException(status_code=400, detail="missing 'path' or 'bundle' in payload")

    # verify signature
    if x_mcp_signature is None:
        raise HTTPException(status_code=401, detail="missing X-MCP-Signature header")
    ok = signing.verify_dict(bundle, x_mcp_signature, ts=x_mcp_ts)
    if not ok:
        raise HTTPException(status_code=401, detail="invalid signature or timestamp")

    # store
    try:
        storage.store(path, {"bundle": bundle, "published_at": int(time.time())})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse({"status": "ok", "path": path})


@app.get("/mcp/fetch/{path:path}")
def fetch(path: str):
    data = storage.load(path)
    if data is None:
        raise HTTPException(status_code=404, detail="bundle not found")
    return data


if __name__ == "__main__":
    # Note: in production, use uvicorn/gunicorn externally
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
