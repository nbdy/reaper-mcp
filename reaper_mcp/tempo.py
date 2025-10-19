from __future__ import annotations

from typing import Any, Dict

import reapy

from reaper_mcp.mcp_core import mcp


@mcp.tool()
def get_bpm() -> Dict[str, Any]:
    """Get current project BPM."""
    try:
        project = reapy.Project()
        bpm = project.bpm
        return {"bpm": bpm}
    except Exception as e:
        return {"error": f"Failed to get BPM: {e}"}


@mcp.tool()
def set_bpm(bpm: float) -> Dict[str, Any]:
    """Set current project BPM."""
    try:
        project = reapy.Project()
        project.bpm = float(bpm)
        return {"bpm": float(bpm)}
    except Exception as e:
        return {"error": f"Failed to set BPM: {e}"}
