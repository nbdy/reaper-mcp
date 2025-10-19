from __future__ import annotations

import logging
from typing import Any, Dict

import reapy

from reaper_mcp.mcp_core import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
def play() -> Dict[str, Any]:
    """Start playback in REAPER.
    
    Returns:
        Dict with ok status on success or error message
    """
    logger.info("play called")
    try:
        project = reapy.Project()
        project.play()
        logger.info("Playback started")
        return {"ok": True, "action": "play"}
    except Exception as e:
        error_msg = f"Failed to start playback: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def pause() -> Dict[str, Any]:
    """Pause playback in REAPER.
    
    Returns:
        Dict with ok status on success or error message
    """
    logger.info("pause called")
    try:
        project = reapy.Project()
        project.pause()
        logger.info("Playback paused")
        return {"ok": True, "action": "pause"}
    except Exception as e:
        error_msg = f"Failed to pause playback: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def stop() -> Dict[str, Any]:
    """Stop playback in REAPER.
    
    Returns:
        Dict with ok status on success or error message
    """
    logger.info("stop called")
    try:
        project = reapy.Project()
        project.stop()
        logger.info("Playback stopped")
        return {"ok": True, "action": "stop"}
    except Exception as e:
        error_msg = f"Failed to stop playback: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def record() -> Dict[str, Any]:
    """Start recording in REAPER.
    
    Returns:
        Dict with ok status on success or error message
    """
    logger.info("record called")
    try:
        project = reapy.Project()
        project.record()
        logger.info("Recording started")
        return {"ok": True, "action": "record"}
    except Exception as e:
        error_msg = f"Failed to start recording: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def set_cursor_position(position: float) -> Dict[str, Any]:
    """Set the edit cursor position in seconds.
    
    Args:
        position: Time position in seconds
    
    Returns:
        Dict with cursor position on success or error message
    """
    logger.info(f"set_cursor_position called with position={position}")
    try:
        project = reapy.Project()
        project.cursor_position = float(position)
        logger.info(f"Cursor position set to {position}")
        return {"ok": True, "position": position}
    except Exception as e:
        error_msg = f"Failed to set cursor position: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def get_cursor_position() -> Dict[str, Any]:
    """Get the current edit cursor position in seconds.
    
    Returns:
        Dict with cursor position or error message
    """
    logger.info("get_cursor_position called")
    try:
        project = reapy.Project()
        position = project.cursor_position
        logger.info(f"Cursor position: {position}")
        return {"position": position}
    except Exception as e:
        error_msg = f"Failed to get cursor position: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def set_time_selection(start: float, end: float) -> Dict[str, Any]:
    """Set the time selection in REAPER.
    
    Args:
        start: Start time in seconds
        end: End time in seconds
    
    Returns:
        Dict with selection range on success or error message
    """
    logger.info(f"set_time_selection called with start={start}, end={end}")
    try:
        project = reapy.Project()
        project.select(start=float(start), end=float(end))
        logger.info(f"Time selection set from {start} to {end}")
        return {"ok": True, "start": start, "end": end, "length": end - start}
    except Exception as e:
        error_msg = f"Failed to set time selection: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def get_time_selection() -> Dict[str, Any]:
    """Get the current time selection in REAPER.
    
    Returns:
        Dict with start, end, and length of time selection or error message
    """
    logger.info("get_time_selection called")
    try:
        project = reapy.Project()
        time_sel = project.time_selection
        result = {
            "start": time_sel.start,
            "end": time_sel.end,
            "length": time_sel.length
        }
        logger.info(f"Time selection: {result}")
        return result
    except Exception as e:
        error_msg = f"Failed to get time selection: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
