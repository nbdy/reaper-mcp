from __future__ import annotations

from typing import Any, Dict

from reaper_mcp.mcp_core import mcp
from reaper_mcp.util import RPR


@mcp.tool()
def get_bpm() -> Dict[str, Any]:
    """Get current project BPM."""
    try:
        bpm = float(RPR.TimeMap_GetDividedBpmAtTime(0.0))
        return {"bpm": bpm}
    except Exception as e:
        return {"error": f"Failed to get BPM: {e}"}


@mcp.tool()
def set_bpm(bpm: float) -> Dict[str, Any]:
    """Set current project BPM."""
    try:
        RPR.SetCurrentBPM(0, float(bpm), True)
        return {"bpm": float(bpm)}
    except Exception as e:
        return {"error": f"Failed to set BPM: {e}"}
