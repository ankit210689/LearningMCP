# LearningMCP — Simple MCP Server

This repository contains a minimal Model Context Protocol (MCP) server implemented with FastAPI.

Features
- Publish bundles via POST /mcp/publish (HMAC-SHA256 signed)
- Fetch bundles via GET /mcp/fetch/{path}
- Simple file-based storage in ./data

Quickstart (macOS, zsh)

1. Create a virtualenv and install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set a secret and run the server:

```bash
export MCP_SECRET="supersecret"
python server.py
```

3. Publish a bundle (example):

```bash
python -c "import json,hmac,hashlib,os; b={'id':'bundle1','version':'1.0.0','data':{'hello':'world'}}; s=hmac.new(os.environ['MCP_SECRET'].encode(),json.dumps(b,sort_keys=True,separators=(',',':')).encode(),hashlib.sha256).hexdigest(); print(s)"
# then use curl with X-MCP-Signature header
```

4. Run tests:

```bash
pytest -q
```

