import argparse
import inspect
from reaper_mcp.mcp_core import mcp

# Import tool modules so their @mcp.tool functions register
from reaper_mcp import project as _project  # noqa: F401
from reaper_mcp import tracks as _tracks  # noqa: F401
from reaper_mcp import tempo as _tempo  # noqa: F401
from reaper_mcp import midi as _midi  # noqa: F401
from reaper_mcp import fx as _fx  # noqa: F401
from reaper_mcp import samples as _samples  # noqa: F401


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Reaper MCP server with selectable transport")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "http", "ws", "websocket"],
        default="stdio",
        help="Transport to use for MCP server (default: stdio)",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host for network transports")
    parser.add_argument("--port", type=int, default=8000, help="Bind port for network transports")
    parser.add_argument(
        "--path",
        default=None,
        help="URL path for HTTP/SSE/Websocket transports (only passed if supported)",
    )
    parser.add_argument(
        "--allow-origin",
        dest="allow_origins",
        action="append",
        default=None,
        help="Allowed CORS origin (can be specified multiple times). Only passed if supported.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    # Build kwargs for mcp.run based on its accepted signature to avoid incompatibility
    sig = inspect.signature(mcp.run)
    accepted = set(sig.parameters.keys())
    kw = {}

    # Normalize some transport aliases
    transport = args.transport
    if transport == "http":
        # Many MCP servers implement HTTP via SSE; prefer 'sse' if supported
        transport = "sse"
    if transport == "websocket":
        transport = "ws"

    if "transport" in accepted:
        kw["transport"] = transport

    # Only add networking options if the run() signature supports them
    if transport != "stdio":
        if "host" in accepted:
            kw["host"] = args.host
        if "port" in accepted:
            kw["port"] = args.port
        if args.path is not None and "path" in accepted:
            kw["path"] = args.path
        if args.allow_origins is not None and "allow_origins" in accepted:
            kw["allow_origins"] = args.allow_origins

    # Start the MCP server
    mcp.run(**kw)
