# 🌟 Snowflake Native MCP Server - Complete Guide

## Overview

The Ghost Detection System now includes a **Snowflake-managed MCP (Model Context Protocol) server** that runs natively in Snowflake, eliminating the need for separate infrastructure.

**Reference:** [Snowflake MCP Server Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)

---

## 🎯 What is Snowflake-Managed MCP?

The Snowflake-managed MCP server provides:

- ✅ **Standardized Integration:** Unified interface for tool discovery and invocation
- ✅ **OAuth Authentication:** Snowflake's built-in OAuth service  
- ✅ **Robust Governance:** Role-based access control (RBAC)
- ✅ **Zero Infrastructure:** No separate servers to deploy or maintain
- ✅ **Enterprise Security:** Built on Snowflake's security model

**MCP Protocol Version:** `2025-06-18`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client (AI Agent)                     │
│              (Claude, Custom App, etc.)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │ OAuth 2.0
                      │ HTTPS/JSON-RPC
                      ▼
┌─────────────────────────────────────────────────────────────┐
│         Snowflake-Managed MCP Server                         │
│         (GHOST_DETECTION_MCP_SERVER)                         │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │ ghost-search   │  │ ghost-analytics│  │sighting-search│ │
│  │ (Cortex Search)│  │(Cortex Analyst)│  │(Cortex Search)│ │
│  └────────┬───────┘  └────────┬───────┘  └──────┬───────┘  │
│           │                   │                  │          │
│  ┌────────▼────────────────────▼──────────────────▼───────┐ │
│  │              Snowflake Data Layer                       │ │
│  │  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  │ │
│  │  │ GHOSTS │  │ SIGHTINGS│  │ EVIDENCE │  │ANALYTICS│  │ │
│  │  └────────┘  └──────────┘  └──────────┘  └─────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Setup Guide

### Step 1: Execute Setup SQL

```sql
-- Run the setup script
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Execute the complete setup
!source sql/10_snowflake_native_mcp_server.sql
```

This creates:
- ✅ OAuth Security Integration (`GHOST_MCP_OAUTH`)
- ✅ 3 Cortex Search Services (ghosts, sightings, evidence)
- ✅ MCP Server with 4 tools
- ✅ Access control and privileges
- ✅ Monitoring views

### Step 2: Get OAuth Credentials

```sql
-- Get your OAuth client credentials (SAVE THESE SECURELY!)
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('GHOST_MCP_OAUTH');
```

**Output:**
```json
{
  "OAUTH_CLIENT_ID": "abc123xyz...",
  "OAUTH_CLIENT_SECRET": "def456uvw...",
  "OAUTH_CLIENT_ID_ISSUED_ON": "2024-01-01 12:00:00",
  "OAUTH_CLIENT_SECRET_ISSUED_ON": "2024-01-01 12:00:00"
}
```

### Step 3: Get MCP Server Endpoint

```sql
-- Get your MCP server endpoint URL
SELECT * FROM VW_MCP_SERVER_INFO;
```

**Example endpoint:**
```
https://myaccount.snowflakecomputing.com/api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER
```

---

## 🔧 Available Tools

The MCP server exposes 4 tools to AI agents:

### 1. 👻 **ghost-search** (Cortex Search)
**Type:** `CORTEX_SEARCH_SERVICE_QUERY`  
**Purpose:** Semantic search across ghost data

**Search Fields:**
- Ghost name, type, description
- Behavioral patterns
- Locations, threat levels, status

**Example Query:**
```json
{
  "query": "shadow entity with electronic interference",
  "limit": 10,
  "columns": ["ghost_name", "ghost_type", "threat_level"]
}
```

### 2. 📊 **ghost-analytics** (Cortex Analyst)
**Type:** `CORTEX_ANALYST_MESSAGE`  
**Purpose:** Natural language analytics queries

**Capabilities:**
- Ghost statistics and trends
- Sighting pattern analysis
- Threat assessments
- Location hotspot identification

**Example Query:**
```json
{
  "message": "What are the top 5 most dangerous ghosts by threat level and sighting count?"
}
```

### 3. 📍 **sighting-search** (Cortex Search)
**Type:** `CORTEX_SEARCH_SERVICE_QUERY`  
**Purpose:** Search sighting events

**Search Fields:**
- Location names and coordinates
- Witness descriptions
- Environmental conditions
- Activity levels, EMF, temperature

**Example Query:**
```json
{
  "query": "hospital sightings with high EMF readings",
  "filter": {
    "@gte": {"emf_reading": 5.0}
  }
}
```

### 4. 🔬 **evidence-search** (Cortex Search)
**Type:** `CORTEX_SEARCH_SERVICE_QUERY`  
**Purpose:** Search evidence repository

**Search Fields:**
- File paths and metadata
- AI-generated descriptions
- Evidence types (image, audio, video)
- Processing status

**Example Query:**
```json
{
  "query": "thermal camera images from january",
  "filter": {
    "@eq": {"evidence_type": "Image"}
  }
}
```

---

## 🔐 Authentication Setup

### OAuth 2.0 Configuration

The MCP server uses OAuth 2.0 for authentication. Configure your MCP client with:

**Configuration Parameters:**
```json
{
  "oauth": {
    "client_id": "<from SYSTEM$SHOW_OAUTH_CLIENT_SECRETS>",
    "client_secret": "<from SYSTEM$SHOW_OAUTH_CLIENT_SECRETS>",
    "authorization_url": "https://<account>.snowflakecomputing.com/oauth/authorize",
    "token_url": "https://<account>.snowflakecomputing.com/oauth/token",
    "redirect_uri": "http://localhost:3000/oauth/callback",
    "scope": "session:role:GHOSTBUSTER"
  }
}
```

### Fixing "Invalid Consent Request" Error

If you see `Invalid consent request` on first login:

1. Find the authorization URL with scope parameter:
   ```
   &scope=session%3Arole%3Aall
   ```

2. Change to your specific role:
   ```
   &scope=session%3Arole%3AGHOSTBUSTER
   ```

3. Resubmit the modified URL

---

## 🔌 MCP Protocol Usage

### 1. Initialize Connection

**Request:**
```http
POST /api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER
Content-Type: application/json
Authorization: Bearer <oauth_token>

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {}
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "proto_version": "2025-06-18",
    "capabilities": {
      "tools": {
        "listChanged": false
      }
    },
    "server_info": {
      "name": "GHOST_DETECTION_MCP_SERVER",
      "title": "Snowflake Server: GHOST_DETECTION_MCP_SERVER",
      "version": "1.0.0"
    }
  }
}
```

### 2. List Available Tools

**Request:**
```http
POST /api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER
Content-Type: application/json
Authorization: Bearer <oauth_token>

{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "ghost-search",
        "description": "Semantic search service for ghost detection data...",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {"type": "string"},
            "columns": {"type": "array"},
            "filter": {"type": "object"},
            "limit": {"type": "integer", "default": 10}
          }
        }
      },
      {
        "name": "ghost-analytics",
        "description": "Natural language interface to query ghost detection analytics...",
        "inputSchema": {
          "type": "object",
          "properties": {
            "message": {"type": "string"}
          }
        }
      }
      // ... other tools
    ]
  }
}
```

### 3. Call a Tool

**Example: Ghost Search**

**Request:**
```http
POST /api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER

{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "ghost-search",
    "arguments": {
      "query": "dangerous poltergeist",
      "limit": 5,
      "columns": ["ghost_name", "threat_level", "status"]
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"results\": [{\"ghost_name\": \"The Hurler\", \"threat_level\": \"Extreme\", \"status\": \"Active\"}, ...], \"request_id\": \"abc-123\"}"
      }
    ]
  }
}
```

**Example: Cortex Analyst Query**

**Request:**
```http
POST /api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER

{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "ghost-analytics",
    "arguments": {
      "message": "Show me the ghost activity trends by month for the last 6 months"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "SELECT MONTH(sighting_datetime) as month, COUNT(*) as activity_count FROM GHOST_SIGHTINGS WHERE sighting_datetime >= DATEADD(month, -6, CURRENT_DATE()) GROUP BY month ORDER BY month"
      }
    ]
  }
}
```

---

## 🛡️ Access Control

### Privileges

| Privilege | Object | Purpose |
|-----------|--------|---------|
| `OWNERSHIP` | MCP Server | Update object configuration |
| `MODIFY` | MCP Server | Update, drop, describe, show, use tools |
| `USAGE` | MCP Server | Connect and discover tools |
| `USAGE` | Cortex Search | Invoke search tools |
| `USAGE` | Semantic View | Invoke Cortex Analyst tools |

### Roles

The setup grants privileges to:
- ✅ `GHOSTBUSTER` - Full USAGE on all tools
- ✅ `GHOST_ANALYST` - Full USAGE on all tools  
- ✅ `GHOST_ADMIN` - MODIFY privileges

### Grant Additional Access

```sql
-- Grant to a new role
GRANT USAGE ON MCP SERVER GHOST_DETECTION_MCP_SERVER TO ROLE <role_name>;

-- Grant search service access
GRANT USAGE ON CORTEX SEARCH SERVICE GHOST_SEARCH_SERVICE TO ROLE <role_name>;
```

---

## 🧪 Testing the MCP Server

### Test 1: Verify Server Creation

```sql
-- Describe the server
DESCRIBE MCP SERVER GHOST_DETECTION_MCP_SERVER;

-- Show all MCP servers
SHOW MCP SERVERS IN SCHEMA APP;

-- View server info
SELECT * FROM VW_MCP_SERVER_INFO;
```

### Test 2: Test Search Functionality

```sql
-- Test ghost search directly
SELECT * FROM TABLE(TEST_GHOST_SEARCH('shadow entity'));

-- Test sighting search
SELECT * 
FROM TABLE(
  SIGHTING_SEARCH_SERVICE(
    QUERY => 'hospital with high EMF',
    LIMIT => 5
  )
);
```

### Test 3: Test with MCP Client

Use an MCP client (like Claude Desktop, LangChain MCP client, or custom client):

1. Configure OAuth credentials
2. Initialize connection
3. List tools
4. Call tools with sample queries

---

## 📊 Monitoring and Management

### View Server Status

```sql
-- Check MCP server configuration
DESCRIBE MCP SERVER GHOST_DETECTION_MCP_SERVER;

-- View endpoint information
SELECT * FROM VW_MCP_SERVER_INFO;

-- Check OAuth integration
SHOW INTEGRATIONS LIKE 'GHOST_MCP_OAUTH';
```

### Monitor Usage

```sql
-- Check audit logs
SELECT *
FROM AUDIT_LOG
WHERE table_name = 'MCP_SERVER'
ORDER BY operation_datetime DESC
LIMIT 10;

-- Monitor Cortex Search usage
-- (Use Snowflake's query history and monitoring tools)
SELECT 
    query_text,
    execution_status,
    total_elapsed_time
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE query_text LIKE '%CORTEX_SEARCH%'
ORDER BY start_time DESC
LIMIT 20;
```

### Update Server Configuration

```sql
-- Update the MCP server (recreate with new tools)
CREATE OR REPLACE MCP SERVER GHOST_DETECTION_MCP_SERVER
FROM SPECIFICATION $$
  tools:
    - name: "ghost-search"
      type: "CORTEX_SEARCH_SERVICE_QUERY"
      identifier: "GHOST_DETECTION.APP.GHOST_SEARCH_SERVICE"
      description: "Updated description..."
      title: "Ghost Data Search"
    # ... additional tools
$$;
```

### Drop Server (if needed)

```sql
-- Drop the MCP server
DROP MCP SERVER GHOST_DETECTION_MCP_SERVER;
```

---

## 🔄 Integration with AI Agents

### Claude Desktop Configuration

Create `.claude_config.json`:

```json
{
  "mcpServers": {
    "ghost-detection": {
      "type": "snowflake",
      "account": "<your_account>",
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

### LangChain Integration

```python
from langchain_mcp import MCPClient

client = MCPClient(
    server_url="https://<account>.snowflakecomputing.com/api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER",
    oauth_config={
        "client_id": "<client_id>",
        "client_secret": "<client_secret>",
        "token_url": "https://<account>.snowflakecomputing.com/oauth/token"
    }
)

# List tools
tools = client.list_tools()

# Call a tool
result = client.call_tool("ghost-search", {"query": "shadow entity", "limit": 5})
```

---

## 🚨 Troubleshooting

### Issue: "Invalid consent request"

**Solution:** Modify the OAuth scope in the authorization URL from `session:role:all` to `session:role:GHOSTBUSTER`

### Issue: "Tool not found"

**Solution:** 
1. Verify Cortex Search services exist: `SHOW CORTEX SEARCH SERVICES;`
2. Check tool names in MCP server: `DESCRIBE MCP SERVER GHOST_DETECTION_MCP_SERVER;`

### Issue: "Insufficient privileges"

**Solution:**
```sql
-- Grant necessary privileges
GRANT USAGE ON MCP SERVER GHOST_DETECTION_MCP_SERVER TO ROLE <role>;
GRANT USAGE ON CORTEX SEARCH SERVICE GHOST_SEARCH_SERVICE TO ROLE <role>;
```

### Issue: OAuth token expired

**Solution:** MCP client should automatically refresh the token using the refresh token flow.

---

## 📚 Additional Resources

- [Snowflake MCP Server Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Cortex Search Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search)
- [Cortex Analyst Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
- [Snowflake OAuth Documentation](https://docs.snowflake.com/en/user-guide/oauth)

---

## ✅ Benefits vs. Custom MCP Server

| Feature | Snowflake Native | Custom Python Server |
|---------|-----------------|---------------------|
| **Infrastructure** | Zero maintenance | Deploy & manage |
| **Security** | Built-in Snowflake | Custom implementation |
| **Authentication** | Native OAuth 2.0 | Custom auth |
| **Scalability** | Auto-scales | Manual scaling |
| **Cost** | Pay per query | Server hosting costs |
| **Latency** | Direct data access | Network hop |
| **Governance** | Native RBAC | Custom RBAC |

---

## 🎉 Summary

The Snowflake-managed MCP server provides:

✅ **4 powerful AI tools** (search + analytics)  
✅ **Zero infrastructure** to deploy or maintain  
✅ **Enterprise security** with OAuth 2.0  
✅ **Native governance** with Snowflake RBAC  
✅ **Direct data access** for lowest latency  
✅ **Auto-scaling** with Snowflake compute  

**Ready to use with any MCP-compatible AI agent!** 🚀

---

**Setup Script:** `sql/10_snowflake_native_mcp_server.sql`  
**Protocol Version:** MCP 2025-06-18  
**Status:** Production Ready ✅

