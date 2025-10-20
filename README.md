# REAPER MCP Server

A Model Context Protocol (MCP) server that provides programmatic control over [REAPER DAW](https://www.reaper.fm/) through a clean, tool-based interface. Built with [FastMCP](https://github.com/jlowin/fastmcp) and [python-reapy](https://github.com/RomeoDespres/reapy), this server enables AI assistants and automation tools to interact with REAPER projects.

## Features

- **Project Management** - Project details, initialization, save, playback state, undo/redo, time conversions
- **Playback Control** - Start, pause, stop, record, cursor and time selection management
- **Markers & Regions** - Add, list, and manage markers and regions
- **Track Operations** - Create, delete, configure tracks (volume, pan, mute, solo, color, selection)
- **Tempo Control** - Get/set project BPM
- **MIDI** - Generate and import MIDI notes, patterns, and files
- **FX & Plugins** - List, add, and control VST plugins and parameters
- **Audio Samples** - Manage sample directories, search, import, and time-stretch audio files

## Prerequisites

- **REAPER** installed with ReaScript enabled
- **python-reapy** bridge configured for out-of-process control
- **Python 3.11+**

> **Note:** The server must be able to communicate with REAPER through the reapy bridge. Ensure REAPER is running and reapy is properly configured before starting the server.

## Installation

### Using uv (Recommended)

```bash
# Install with uv
uv pip install reaper-mcp

# Or run directly with uv
uv tool install reaper-mcp
```

### Using pip

```bash
pip install reaper-mcp
```

## Usage

Run the server (default stdio transport for MCP clients):

```bash
python -m reaper_mcp
```

**Run with MCP Proxy (stdio):**
```bash
uv tool run mcpo --port 8000 -- uv run reaper_mcp
```

**Options:**
- `--transport {stdio,sse,http,ws,websocket}` - Transport protocol (default: `stdio`)
- `--host HOST` - Host for network transports (default: `127.0.0.1`)
- `--port PORT` - Port for network transports (default: `8000`)
- `--path PATH` - URL path for HTTP/SSE/WebSocket
- `--allow-origin ORIGIN` - CORS origin (repeatable)

**Example with WebSocket:**
```bash
python -m reaper_mcp --transport ws --port 9000
```

## Claude Desktop Configuration

Add to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "reaper": {
      "command": "python",
      "args": ["-m", "reaper_mcp"]
    }
  }
}
```

For uv, use `"command": "uv"` with `"args": ["run", "python", "-m", "reaper_mcp"]`

## Notes

- Tools are designed to be small and focused - prefer calling multiple tools over complex combined actions
- File paths must be accessible from the REAPER host machine
- Some operations depend on REAPER configuration, OS, and installed plugins
- Tools return helpful error messages when operations are unavailable

## Links

- [REAPER DAW](https://www.reaper.fm/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [python-reapy](https://github.com/RomeoDespres/reapy)
- [Model Context Protocol](https://modelcontextprotocol.io/)
