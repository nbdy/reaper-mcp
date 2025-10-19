from fastmcp import FastMCP
from reaper_mcp.instructions import INSTRUCTIONS

# Central MCP instance used by all tool modules
mcp = FastMCP("Reaper MCP Server", INSTRUCTIONS)

__all__ = ["mcp"]
