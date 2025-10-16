# ⚡ Snowflake Native MCP Server - Quick Start

Get up and running with the Snowflake-managed MCP server in 5 minutes!

## 🚀 Quick Setup (5 Steps)

### Step 1: Run the Setup Script (2 minutes)

```sql
-- Connect to Snowflake and run:
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Execute the setup
!source sql/10_snowflake_native_mcp_server.sql
```

**What it creates:**
- ✅ OAuth integration for authentication
- ✅ 3 Cortex Search services (ghosts, sightings, evidence)
- ✅ MCP server with 4 AI tools
- ✅ Access control and monitoring views

### Step 2: Get OAuth Credentials (30 seconds)

```sql
-- Get your credentials
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('GHOST_MCP_OAUTH');
```

**Save these values:**
```json
{
  "OAUTH_CLIENT_ID": "abc123...",
  "OAUTH_CLIENT_SECRET": "xyz789..."
}
```

### Step 3: Get Your MCP Endpoint (30 seconds)

```sql
-- Get your endpoint URL
SELECT * FROM VW_MCP_SERVER_INFO;
```

**Your endpoint will look like:**
```
https://myaccount.snowflakecomputing.com/api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER
```

### Step 4: Configure Your MCP Client (1 minute)

Edit `mcp/snowflake_native_mcp_client_config.json`:

```json
{
  "connection": {
    "account": "myaccount",  // ← Replace with your account
    "endpoint_url": "https://myaccount.snowflakecomputing.com/api/v2/..." // ← Your endpoint
  },
  "authentication": {
    "client_id": "abc123...",     // ← From Step 2
    "client_secret": "xyz789...", // ← From Step 2
    "scope": "session:role:GHOSTBUSTER"
  }
}
```

### Step 5: Test It! (1 minute)

```sql
-- Test the ghost search
SELECT * FROM TABLE(TEST_GHOST_SEARCH('shadow entity'));
```

**Or use the HTTP API:**

```bash
curl -X POST "https://myaccount.snowflakecomputing.com/api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

## 🎯 Available Tools

Your MCP server now exposes **4 powerful AI tools**:

### 1. 👻 ghost-search
Search ghost data semantically
```json
{"query": "dangerous shadow entity", "limit": 5}
```

### 2. 📊 ghost-analytics  
Ask natural language questions
```json
{"message": "What are the top 5 most active ghosts?"}
```

### 3. 📍 sighting-search
Search sighting events
```json
{"query": "hospital with high EMF", "limit": 10}
```

### 4. 🔬 evidence-search
Search evidence repository
```json
{"query": "thermal images", "filter": {"@eq": {"evidence_type": "Image"}}}
```

## 🔌 Connect Your AI Agent

### Option A: Claude Desktop

Create/edit `~/.claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ghost-detection": {
      "type": "snowflake",
      "account": "myaccount",
      "database": "GHOST_DETECTION",
      "schema": "APP",
      "server": "GHOST_DETECTION_MCP_SERVER",
      "oauth": {
        "client_id": "<your_client_id>",
        "client_secret": "<your_client_secret>",
        "redirect_uri": "http://localhost:3000/oauth/callback"
      }
    }
  }
}
```

Restart Claude Desktop. Your ghost detection tools are now available!

### Option B: Python Client

```python
import requests

endpoint = "https://myaccount.snowflakecomputing.com/api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER"
headers = {
    "Authorization": "Bearer <oauth_token>",
    "Content-Type": "application/json"
}

# List tools
response = requests.post(endpoint, json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
}, headers=headers)

print(response.json())

# Search for ghosts
response = requests.post(endpoint, json={
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "ghost-search",
        "arguments": {
            "query": "poltergeist",
            "limit": 5
        }
    }
}, headers=headers)

print(response.json())
```

### Option C: Custom MCP Client

See `mcp/snowflake_native_mcp_client_config.json` for detailed examples.

## ✅ Verify Everything Works

### Check 1: Server Created
```sql
DESCRIBE MCP SERVER GHOST_DETECTION_MCP_SERVER;
```

### Check 2: Tools Available
```sql
-- Should show 4 tools
SELECT * FROM VW_MCP_SERVER_INFO;
```

### Check 3: Search Works
```sql
-- Should return results
SELECT * FROM TABLE(TEST_GHOST_SEARCH('shadow'));
```

### Check 4: OAuth Works
```sql
-- Should show your credentials
SHOW INTEGRATIONS LIKE 'GHOST_MCP_OAUTH';
```

## 🎉 You're Done!

Your Snowflake-managed MCP server is now **live and ready** for AI agents!

### What You Can Do Now:

- ✅ Connect Claude Desktop to query ghost data
- ✅ Build custom AI applications with MCP tools
- ✅ Perform semantic search across ghost database
- ✅ Ask natural language analytics questions
- ✅ Integrate with LangChain, LlamaIndex, etc.

## 🆘 Troubleshooting

### "Invalid consent request"
Change OAuth scope from `session:role:all` to `session:role:GHOSTBUSTER`

### "Tool not found"
Verify search services exist:
```sql
SHOW CORTEX SEARCH SERVICES IN SCHEMA APP;
```

### "Insufficient privileges"
Grant access:
```sql
GRANT USAGE ON MCP SERVER GHOST_DETECTION_MCP_SERVER TO ROLE <your_role>;
```

## 📚 Learn More

- **Full Guide:** `SNOWFLAKE_MCP_GUIDE.md`
- **Official Docs:** https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp
- **MCP Protocol:** https://modelcontextprotocol.io/

---

**Time to Production:** 5 minutes ⚡  
**Infrastructure Required:** Zero 🎯  
**Status:** Production Ready ✅

