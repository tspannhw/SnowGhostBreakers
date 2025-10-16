# 🔌 Model Context Protocol (MCP) Integration Guide

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables AI models and agents to securely connect to data sources and tools. It provides a standardized way for AI systems to:

- Access data from various sources
- Execute tools and functions
- Retrieve contextual information
- Maintain security and permissions

For Ghost Detection, MCP enables AI agents (like Claude, ChatGPT, or custom agents) to directly interact with the Snowflake database.

## Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│   AI Agent      │         │   MCP Server     │         │    Snowflake     │
│  (Claude, etc.) │◄───────►│  (Ghost Detect)  │◄───────►│   (Database)     │
└─────────────────┘         └──────────────────┘         └──────────────────┘
     Client                      Server                        Data Source
```

## Setup

### 1. Prerequisites

```bash
# Install MCP Python package
pip install mcp anthropic-mcp

# Install Snowflake connector
pip install snowflake-connector-python snowflake-snowpark-python
```

### 2. Configure Environment Variables

Create `.env` file:

```bash
# Snowflake credentials
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=GHOSTBUSTER
```

### 3. Start MCP Server

```bash
# Navigate to MCP directory
cd mcp/

# Run the server
python mcp_server.py
```

The server will start and listen for MCP client connections.

### 4. Configure MCP Client

Add to your MCP client configuration (e.g., Claude Desktop config):

```json
{
  "mcpServers": {
    "ghost-detection": {
      "command": "python",
      "args": ["/path/to/SnowGhostBreakers/mcp/mcp_server.py"],
      "env": {
        "SNOWFLAKE_ACCOUNT": "your_account",
        "SNOWFLAKE_USER": "your_user",
        "SNOWFLAKE_PASSWORD": "your_password",
        "SNOWFLAKE_ROLE": "GHOSTBUSTER"
      }
    }
  }
}
```

## Available Resources

MCP provides access to these data resources:

### 1. Ghost Registry
```
URI: snowflake://ghost-detection/ghosts
```
Complete ghost registry with all detected entities

### 2. Ghost Sightings
```
URI: snowflake://ghost-detection/sightings
```
All ghost sighting and encounter data

### 3. Evidence
```
URI: snowflake://ghost-detection/evidence
```
Multimedia evidence and analysis results

### 4. Investigations
```
URI: snowflake://ghost-detection/investigations
```
Active and historical investigation cases

### 5. Activity Summary
```
URI: snowflake://ghost-detection/analytics/activity-summary
```
Ghost activity metrics and analytics

### 6. Paranormal Hotspots
```
URI: snowflake://ghost-detection/analytics/hotspots
```
Geographic hotspot analysis

### 7. Business Vocabulary
```
URI: snowflake://ghost-detection/vocabulary
```
Ghost ontology and taxonomy definitions

### 8. AI Agents
```
URI: snowflake://ghost-detection/agents
```
AI agent definitions and performance

## Available Tools

AI agents can call these tools via MCP:

### 1. query_ghosts

Query ghost registry with filters:

```python
result = await client.call_tool("query_ghosts", {
    "threat_level": "Extreme",
    "status": "Active",
    "limit": 10
})
```

### 2. analyze_sighting

Analyze a ghost sighting using Cortex AI:

```python
result = await client.call_tool("analyze_sighting", {
    "sighting_id": "SIGHT001"
})
```

### 3. generate_ghost_report

Generate comprehensive AI report for a ghost:

```python
result = await client.call_tool("generate_ghost_report", {
    "ghost_id": "GH001"
})
```

### 4. classify_description

Classify ghost type from description:

```python
result = await client.call_tool("classify_description", {
    "description": "Translucent figure floating through walls"
})
```

### 5. search_vocabulary

Search business vocabulary and taxonomy:

```python
result = await client.call_tool("search_vocabulary", {
    "search_term": "poltergeist"
})
```

### 6. find_similar_sightings

Find similar sightings using semantic search:

```python
result = await client.call_tool("find_similar_sightings", {
    "description": "Cold spots and floating objects",
    "limit": 5
})
```

### 7. ask_database

Ask natural language questions:

```python
result = await client.call_tool("ask_database", {
    "question": "Which ghost is most dangerous right now?"
})
```

### 8. run_agent

Execute an AI agent action:

```python
result = await client.call_tool("run_agent", {
    "agent_id": "AGENT_001",
    "action": "monitor_threats"
})
```

## Available Prompts

Pre-configured prompt templates:

### 1. analyze_threat

Analyze ghost threat and provide recommendations:

```python
prompt = await client.get_prompt("analyze_threat", {
    "ghost_id": "GH002"
})
```

Returns comprehensive threat analysis including:
- Current threat level
- Behavioral patterns
- Risk factors
- Recommended actions
- Resource requirements

### 2. investigation_brief

Generate investigation briefing:

```python
prompt = await client.get_prompt("investigation_brief", {
    "investigation_id": "CASE001"
})
```

### 3. hotspot_report

Generate hotspot analysis:

```python
prompt = await client.get_prompt("hotspot_report", {
    "location": "New York Public Library"
})
```

## Example Usage with Claude

### Example 1: Check Active Threats

**User**: "Show me all active extreme-threat ghosts"

**Claude** (using MCP):
```python
# Claude internally calls:
result = await call_tool("query_ghosts", {
    "threat_level": "Extreme",
    "status": "Active"
})
```

**Response**: "I found 2 extreme-threat ghosts currently active:
1. Shadow Walker - High activity in subway tunnels
2. The Collector - Aggressive behavior at Metropolitan Museum"

### Example 2: Analyze New Sighting

**User**: "Analyze sighting SIGHT003"

**Claude** (using MCP):
```python
result = await call_tool("analyze_sighting", {
    "sighting_id": "SIGHT003"
})
```

**Response**: "Analysis complete. This is a Class V Shadow Entity with:
- Threat Level: High
- Electronic disruption capabilities
- Recommend immediate containment with hardened equipment"

### Example 3: Natural Language Query

**User**: "Which location has had the most ghost activity this week?"

**Claude** (using MCP):
```python
result = await call_tool("ask_database", {
    "question": "Which location has had the most ghost activity this week?"
})
```

**Response**: "Based on the data, the Metropolitan Museum has had the most activity with 7 sightings in the past week, involving 3 different ghosts including The Collector (extreme threat)."

## Security

### Authentication

MCP server uses Snowflake authentication:
- Username/password credentials
- Role-based access control (RBAC)
- Environment variable management

### Authorization

Tools respect Snowflake permissions:
- Users can only access data their Snowflake role permits
- Agent actions follow authority level restrictions
- Audit trail tracks all MCP requests

### Best Practices

1. **Use environment variables** for credentials
2. **Limit MCP server permissions** - use dedicated service account
3. **Enable audit logging** - track all MCP requests
4. **Implement rate limiting** - prevent abuse
5. **Use HTTPS/TLS** for production deployments

## Monitoring

### View MCP Request Log

```sql
-- See all agent actions (including MCP-triggered)
SELECT * FROM APP.AGENT_ACTIONS
WHERE action_description LIKE '%MCP%'
ORDER BY created_date DESC;
```

### Performance Metrics

```sql
-- Agent performance via MCP
SELECT * FROM APP.VW_AGENT_PERFORMANCE;
```

## Troubleshooting

### Connection Issues

1. **Check credentials**:
```bash
# Test Snowflake connection
python -c "import snowflake.connector; conn = snowflake.connector.connect(
    account='YOUR_ACCOUNT',
    user='YOUR_USER',
    password='YOUR_PASSWORD'
); print('Connected!')"
```

2. **Verify environment variables**:
```bash
echo $SNOWFLAKE_ACCOUNT
echo $SNOWFLAKE_USER
```

3. **Check network access**:
```bash
# Test connectivity to Snowflake
ping your_account.snowflakecomputing.com
```

### Tool Execution Errors

1. **Check tool logs**:
```python
# Add logging to MCP server
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Verify permissions**:
```sql
-- Check role permissions
SHOW GRANTS TO ROLE GHOSTBUSTER;
```

3. **Test stored procedures directly**:
```sql
-- Test procedure that MCP calls
CALL APP.GENERATE_GHOST_REPORT('GH001');
```

### Performance Issues

1. **Optimize queries** in MCP server
2. **Use result caching** for frequent queries
3. **Increase warehouse size** if needed
4. **Add indexes** to frequently queried columns

## Advanced Configuration

### Custom Tools

Add custom tools to MCP server:

```python
@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    # Add your custom tool
    if name == "custom_analysis":
        result = session.sql(arguments["query"]).to_pandas()
        return [TextContent(type="text", text=result.to_json())]
```

### Custom Resources

Add custom data resources:

```python
@app.list_resources()
async def list_resources() -> List[Resource]:
    return [
        # Add custom resource
        Resource(
            uri="snowflake://ghost-detection/custom-report",
            name="Custom Report",
            mimeType="application/json",
            description="Your custom data resource"
        )
    ]
```

### Webhook Integration

Trigger MCP tools via webhooks:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/webhook/analyze-sighting")
async def webhook_analyze(sighting_id: str):
    result = await mcp_client.call_tool("analyze_sighting", {
        "sighting_id": sighting_id
    })
    return {"result": result}
```

## MCP + Agentic AI

Combine MCP with Agentic AI for powerful automation:

```python
# AI Agent uses MCP to access data and take actions
async def autonomous_threat_response():
    # 1. Query for threats via MCP
    threats = await mcp_client.call_tool("query_ghosts", {
        "threat_level": "Extreme",
        "status": "Active"
    })
    
    # 2. Analyze each threat
    for threat in threats:
        analysis = await mcp_client.call_tool("generate_ghost_report", {
            "ghost_id": threat["ghost_id"]
        })
        
        # 3. Run agent response
        await mcp_client.call_tool("run_agent", {
            "agent_id": "AGENT_003",
            "action": "assign_investigators"
        })
```

## Deployment

### Production Deployment

1. **Use managed service** (Snowflake managed MCP when available)
2. **Deploy as container**:
```dockerfile
FROM python:3.11
COPY mcp/ /app/
RUN pip install -r requirements.txt
CMD ["python", "/app/mcp_server.py"]
```

3. **Set up monitoring**:
```python
# Add application monitoring
from prometheus_client import start_http_server, Counter

requests_counter = Counter('mcp_requests_total', 'Total MCP requests')
```

### Scaling

- Use connection pooling for Snowflake
- Implement request queuing
- Add load balancing for multiple MCP servers
- Cache frequent queries

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Snowflake Python Connector](https://docs.snowflake.com/en/user-guide/python-connector)
- [Anthropic MCP Documentation](https://docs.anthropic.com/mcp)

---

**Connect your AI agents to ghost data with MCP!** 🔌👻

