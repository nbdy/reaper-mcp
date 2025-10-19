from __future__ import annotations

import logging
from typing import Any, Dict

import reapy

from reaper_mcp.mcp_core import mcp

logger = logging.getLogger(__name__)


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
    """Set current project BPM.
    
    Args:
        bpm: BPM value (beats per minute). Must be a number between 1 and 960.
             Common range is 60-180 BPM.
    
    Returns:
        Dict with 'bpm' on success or 'error' on failure.
    
    Note: If you receive a 422 error, ensure the 'bpm' parameter is sent as a number,
          not a string (e.g., {"bpm": 120} not {"bpm": "120"}).
    """
    logger.info(f"set_bpm called with bpm={bpm} (type: {type(bpm).__name__})")
    
    # Validate BPM is a valid number
    try:
        bpm_value = float(bpm)
    except (TypeError, ValueError) as e:
        error_msg = f"Invalid BPM value: {bpm}. Must be a number, got {type(bpm).__name__}. Error: {e}"
        logger.error(error_msg)
        return {"error": error_msg}
    
    # Validate BPM range
    if bpm_value < 1 or bpm_value > 960:
        error_msg = f"BPM value {bpm_value} out of valid range (1-960)"
        logger.warning(error_msg)
        return {"error": error_msg}
    
    try:
        project = reapy.Project()
        project.bpm = bpm_value
        logger.info(f"Successfully set BPM to {bpm_value}")
        return {"bpm": bpm_value}
    except Exception as e:
        error_msg = f"Failed to set BPM: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
