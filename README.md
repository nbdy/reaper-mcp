# REAPER MCP Server

A Model Context Protocol (MCP) server that provides programmatic control over [REAPER DAW](https://www.reaper.fm/) through a clean, tool-based interface. Built with [FastMCP](https://github.com/jlowin/fastmcp) and [python-reapy](https://github.com/RomeoDespres/reapy), this server enables AI assistants and automation tools to interact with REAPER projects.

## Features

### 🎵 Project Management
- Get project details (BPM, track count, track names)
- Initialize new projects with optional track clearing
- Get project length in seconds
- Save the current project
- Get playback state (playing, paused, stopped, recording)
- Get current play position in seconds
- Get current playback rate

### 🎚️ Track Operations
- Create tracks at specific indices
- Delete tracks by index
- List all tracks with names
- Get track name by index
- Get track item count by index
- Set track color by index (RGB values)

### ⏱️ Tempo Control
- Get current project BPM
- Set project BPM (1-960 range)

### 🎹 MIDI Generation & Import
- Add MIDI notes to tracks as new MIDI items
- Generate step-sequenced MIDI patterns
- Create MIDI files with pretty_midi
- Import MIDI files (base64-encoded) onto tracks

### 🎛️ FX & VST Plugins
- List available VST plugins from REAPER configuration
- Add FX/VST plugins to tracks
- List FX on specific tracks
- Get/set FX parameter values (normalized 0-1)

### 🎧 Audio Sample Management
- Configure and manage sample directories (persistent)
- Search for audio samples across directories (WAV, AIFF, FLAC, MP3, OGG)
- Import audio samples to tracks
- Time-stretch samples via playback rate control

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

### Run with Default Settings (stdio transport)

```bash
python -m reaper_mcp
```

### Run with MCP Proxy (stdio)

```bash
uv tool run mcpo --port 8000 -- uv run reaper_mcp
```

### Run with MCP Proxy (HTTP/SSE)

```bash
uv tool run mcpo --port 8000 -- uv run python -m reaper_mcp --transport sse --port 8001
```

### Command-Line Options

```bash
python -m reaper_mcp [OPTIONS]
```

**Available Options:**

- `--transport {stdio,sse,http,ws,websocket}` - Transport protocol (default: `stdio`)
- `--host HOST` - Bind host for network transports (default: `127.0.0.1`)
- `--port PORT` - Bind port for network transports (default: `8000`)
- `--path PATH` - URL path for HTTP/SSE/WebSocket transports
- `--allow-origin ORIGIN` - Allowed CORS origin (can be specified multiple times)

### Examples

**WebSocket server on port 9000:**
```bash
python -m reaper_mcp --transport ws --port 9000
```

**SSE server with custom host:**
```bash
python -m reaper_mcp --transport sse --host 0.0.0.0 --port 8080
```

**stdio mode (for Claude Desktop or other MCP clients):**
```bash
python -m reaper_mcp
```

## Integration with MCP Clients

### Claude Desktop Configuration

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

Or with uv:

```json
{
  "mcpServers": {
    "reaper": {
      "command": "uv",
      "args": ["run", "python", "-m", "reaper_mcp"]
    }
  }
}
```

## Development

### Project Structure

```
reaper_mcp/
├── __main__.py         # Entry point and CLI
├── mcp_core.py         # FastMCP server initialization
├── project.py          # Project management tools
├── tracks.py           # Track operations
├── tempo.py            # Tempo/BPM control
├── midi.py             # MIDI generation and import
├── fx.py               # FX/VST plugin management
├── samples.py          # Audio sample management
└── util.py             # Utility functions
```

### Dependencies

- `fastmcp>=2.12.5` - MCP server framework
- `python-reapy>=0.10.0` - REAPER Python API
- `pretty-midi>=0.2.10` - MIDI file generation

## Notes

- Tools are designed to be small and focused - prefer calling multiple tools over complex combined actions
- File paths must be accessible from the REAPER host machine
- Some operations depend on REAPER configuration, OS, and installed plugins
- Tools return helpful error messages when operations are unavailable

## License

See project repository for license information.

## Links

- [REAPER DAW](https://www.reaper.fm/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [python-reapy](https://github.com/RomeoDespres/reapy)
- [Model Context Protocol](https://modelcontextprotocol.io/)
