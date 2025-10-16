"""
Ghost Detection MCP Server
Model Context Protocol server for AI agent access to Snowflake
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import snowflake.connector
from snowflake.snowpark import Session
from snowflake.snowpark import functions as F
import os

# Initialize MCP Server
app = Server("ghost-detection-snowflake")

# Snowflake connection configuration
SNOWFLAKE_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "warehouse": "GHOST_DETECTION_WH",
    "database": "GHOST_DETECTION",
    "schema": "APP",
    "role": os.getenv("SNOWFLAKE_ROLE", "GHOSTBUSTER")
}

# Global session
_session: Optional[Session] = None

def get_session() -> Session:
    """Get or create Snowflake session"""
    global _session
    if _session is None:
        _session = Session.builder.configs(SNOWFLAKE_CONFIG).create()
    return _session

@app.list_resources()
async def list_resources() -> List[Resource]:
    """List available data resources"""
    return [
        Resource(
            uri="snowflake://ghost-detection/ghosts",
            name="Ghost Registry",
            mimeType="application/json",
            description="Complete ghost registry with all detected entities"
        ),
        Resource(
            uri="snowflake://ghost-detection/sightings",
            name="Ghost Sightings",
            mimeType="application/json",
            description="All ghost sighting and encounter data"
        ),
        Resource(
            uri="snowflake://ghost-detection/evidence",
            name="Ghost Evidence",
            mimeType="application/json",
            description="Multimedia evidence and analysis results"
        ),
        Resource(
            uri="snowflake://ghost-detection/investigations",
            name="Investigations",
            mimeType="application/json",
            description="Active and historical investigation cases"
        ),
        Resource(
            uri="snowflake://ghost-detection/analytics/activity-summary",
            name="Activity Summary",
            mimeType="application/json",
            description="Ghost activity metrics and analytics"
        ),
        Resource(
            uri="snowflake://ghost-detection/analytics/hotspots",
            name="Paranormal Hotspots",
            mimeType="application/json",
            description="Geographic hotspot analysis"
        ),
        Resource(
            uri="snowflake://ghost-detection/vocabulary",
            name="Business Vocabulary",
            mimeType="application/json",
            description="Ghost ontology and taxonomy definitions"
        ),
        Resource(
            uri="snowflake://ghost-detection/agents",
            name="AI Agents",
            mimeType="application/json",
            description="AI agent definitions and performance"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read data from a resource"""
    session = get_session()
    
    # Parse URI and fetch data
    resource_map = {
        "snowflake://ghost-detection/ghosts": "SELECT * FROM APP.GHOSTS",
        "snowflake://ghost-detection/sightings": "SELECT * FROM APP.GHOST_SIGHTINGS ORDER BY sighting_datetime DESC LIMIT 100",
        "snowflake://ghost-detection/evidence": "SELECT * FROM APP.GHOST_EVIDENCE LIMIT 100",
        "snowflake://ghost-detection/investigations": "SELECT * FROM APP.INVESTIGATIONS",
        "snowflake://ghost-detection/analytics/activity-summary": "SELECT * FROM ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY",
        "snowflake://ghost-detection/analytics/hotspots": "SELECT * FROM ANALYTICS.VW_PARANORMAL_HOTSPOTS",
        "snowflake://ghost-detection/vocabulary": "SELECT * FROM APP.BUSINESS_VOCABULARY",
        "snowflake://ghost-detection/agents": "SELECT * FROM APP.AI_AGENTS WHERE is_active = TRUE"
    }
    
    query = resource_map.get(uri)
    if not query:
        raise ValueError(f"Unknown resource: {uri}")
    
    result = session.sql(query).to_pandas()
    return result.to_json(orient="records", date_format="iso")

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="query_ghosts",
            description="Query ghost registry with filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "threat_level": {"type": "string"},
                    "ghost_type": {"type": "string"},
                    "status": {"type": "string"},
                    "limit": {"type": "integer", "default": 100}
                }
            }
        ),
        Tool(
            name="analyze_sighting",
            description="Analyze a ghost sighting using Cortex AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "sighting_id": {"type": "string"}
                },
                "required": ["sighting_id"]
            }
        ),
        Tool(
            name="generate_ghost_report",
            description="Generate AI report for a ghost",
            inputSchema={
                "type": "object",
                "properties": {
                    "ghost_id": {"type": "string"}
                },
                "required": ["ghost_id"]
            }
        ),
        Tool(
            name="classify_description",
            description="Classify ghost type from description",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string"}
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="search_vocabulary",
            description="Search business vocabulary",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {"type": "string"}
                },
                "required": ["search_term"]
            }
        ),
        Tool(
            name="find_similar_sightings",
            description="Find similar sightings using semantic search",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="ask_database",
            description="Ask natural language question",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"}
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="run_agent",
            description="Execute an AI agent action",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "action": {"type": "string"}
                },
                "required": ["agent_id", "action"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute a tool"""
    session = get_session()
    
    try:
        if name == "query_ghosts":
            query = "SELECT * FROM APP.GHOSTS WHERE 1=1"
            if arguments.get("threat_level"):
                query += f" AND threat_level = '{arguments['threat_level']}'"
            if arguments.get("ghost_type"):
                query += f" AND ghost_type = '{arguments['ghost_type']}'"
            if arguments.get("status"):
                query += f" AND status = '{arguments['status']}'"
            query += f" LIMIT {arguments.get('limit', 100)}"
            
            result = session.sql(query).to_pandas()
            return [TextContent(
                type="text",
                text=result.to_json(orient="records", date_format="iso")
            )]
        
        elif name == "analyze_sighting":
            sighting_id = arguments["sighting_id"]
            result = session.call("APP.ANALYZE_SIGHTING_WITH_AI", sighting_id)
            return [TextContent(type="text", text=str(result))]
        
        elif name == "generate_ghost_report":
            ghost_id = arguments["ghost_id"]
            result = session.call("APP.GENERATE_GHOST_REPORT", ghost_id)
            return [TextContent(type="text", text=str(result))]
        
        elif name == "classify_description":
            description = arguments["description"]
            result = session.call("APP.CLASSIFY_GHOST_TYPE", description)
            return [TextContent(type="text", text=str(result))]
        
        elif name == "search_vocabulary":
            search_term = arguments["search_term"]
            query = f"SELECT * FROM TABLE(APP.SEARCH_VOCABULARY('{search_term}'))"
            result = session.sql(query).to_pandas()
            return [TextContent(
                type="text",
                text=result.to_json(orient="records", date_format="iso")
            )]
        
        elif name == "find_similar_sightings":
            description = arguments["description"]
            limit = arguments.get("limit", 5)
            query = f"""
                SELECT * FROM TABLE(
                    APP.FIND_SIMILAR_INCIDENTS('{description}', {limit})
                )
            """
            result = session.sql(query).to_pandas()
            return [TextContent(
                type="text",
                text=result.to_json(orient="records", date_format="iso")
            )]
        
        elif name == "ask_database":
            question = arguments["question"]
            result = session.call("APP.ASK_GHOST_DATABASE", question)
            return [TextContent(type="text", text=str(result))]
        
        elif name == "run_agent":
            agent_id = arguments["agent_id"]
            action = arguments["action"]
            
            action_map = {
                "monitor_threats": "AGENT_MONITOR_THREATS",
                "analyze_sightings": "AGENT_ANALYZE_NEW_SIGHTINGS",
                "assign_investigators": "AGENT_ASSIGN_INVESTIGATORS",
                "generate_predictions": "AGENT_GENERATE_PREDICTIONS",
                "daily_summary": "AGENT_DAILY_SUMMARY"
            }
            
            procedure = action_map.get(action)
            if procedure:
                result = session.call(f"APP.{procedure}")
                return [TextContent(type="text", text=str(result))]
            else:
                return [TextContent(type="text", text=f"Unknown action: {action}")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

@app.list_prompts()
async def list_prompts() -> List[Dict[str, Any]]:
    """List available prompts"""
    return [
        {
            "name": "analyze_threat",
            "description": "Analyze ghost threat level and provide recommendations",
            "arguments": [
                {"name": "ghost_id", "description": "Ghost to analyze", "required": True}
            ]
        },
        {
            "name": "investigation_brief",
            "description": "Generate investigation briefing",
            "arguments": [
                {"name": "investigation_id", "description": "Investigation ID", "required": True}
            ]
        },
        {
            "name": "hotspot_report",
            "description": "Generate hotspot analysis report",
            "arguments": [
                {"name": "location", "description": "Location to analyze", "required": True}
            ]
        }
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: Dict[str, str]) -> str:
    """Get a prompt template"""
    session = get_session()
    
    if name == "analyze_threat":
        ghost_id = arguments["ghost_id"]
        ghost_data = session.sql(f"SELECT * FROM APP.GHOSTS WHERE ghost_id = '{ghost_id}'").to_pandas()
        sightings = session.sql(f"SELECT * FROM APP.GHOST_SIGHTINGS WHERE ghost_id = '{ghost_id}' ORDER BY sighting_datetime DESC LIMIT 10").to_pandas()
        
        prompt = f"""Analyze the following ghost and provide a comprehensive threat assessment:

Ghost: {ghost_data.to_dict('records')[0] if not ghost_data.empty else 'Not found'}

Recent Sightings (last 10):
{sightings.to_json(orient='records', date_format='iso')}

Provide:
1. Current threat level assessment
2. Behavioral patterns
3. Risk factors
4. Recommended actions
5. Resource requirements
"""
        return prompt
    
    elif name == "investigation_brief":
        investigation_id = arguments["investigation_id"]
        result = session.call("APP.GENERATE_INVESTIGATION_SUMMARY", investigation_id)
        return str(result)
    
    elif name == "hotspot_report":
        location = arguments["location"]
        hotspot_data = session.sql(f"""
            SELECT * FROM ANALYTICS.VW_PARANORMAL_HOTSPOTS 
            WHERE location_name LIKE '%{location}%'
        """).to_pandas()
        
        prompt = f"""Analyze this paranormal hotspot:

Location Data:
{hotspot_data.to_json(orient='records', date_format='iso')}

Provide:
1. Activity assessment
2. Historical patterns
3. Ghost types present
4. Risk evaluation
5. Monitoring recommendations
"""
        return prompt
    
    return "Prompt not found"

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())

