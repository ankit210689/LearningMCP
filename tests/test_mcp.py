import os
import json
import hmac
import hashlib

from fastapi.testclient import TestClient
from server import app


client = TestClient(app)


def test_publish_and_fetch():
    secret = os.environ.get("MCP_SECRET")
    assert secret, "set MCP_SECRET for tests"

    bundle = {"id": "bundle-test", "version": "1.0.0", "data": {"x": 1}}
    bbytes = json.dumps(bundle, sort_keys=True, separators=(",", ":")).encode()
    sig = hmac.new(secret.encode(), bbytes, hashlib.sha256).hexdigest()

    resp = client.post("/mcp/publish", json={"path": "bundle-test", "bundle": bundle}, headers={"X-MCP-Signature": sig})
    assert resp.status_code == 200, resp.text

    f = client.get("/mcp/fetch/bundle-test")
    assert f.status_code == 200
    data = f.json()
    assert data["bundle"]["id"] == "bundle-test"
