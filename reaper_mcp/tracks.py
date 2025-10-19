from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import reapy

from reaper_mcp.mcp_core import mcp
from reaper_mcp.project import get_project_details

logger = logging.getLogger(__name__)


@mcp.tool()
def create_track(name: Optional[str] = None, index: Optional[int] = None) -> Dict[str, Any]:
    """Create a new track at optional index; returns its index.
    
    Args:
        name: Optional track name
        index: Optional position index (0-based). If out of range, will be clamped.
    
    Note: If you receive a 422 error, ensure 'index' is sent as a number if provided.
    """
    logger.info(f"create_track called with name={name}, index={index} (type: {type(index).__name__})")
    try:
        project = reapy.Project()
        n = len(project.tracks)
        idx = max(0, min(index if isinstance(index, int) else n, n))
        track = project.add_track(index=idx)
        if name:
            track.name = str(name)
        logger.info(f"Successfully created track at index {idx} with name '{name or ''}'")
        return {"index": idx, "name": name or ""}
    except Exception as e:
        error_msg = f"Failed to create track: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def delete_track(index: int) -> Dict[str, Any]:
    """Delete track by index.
    
    Args:
        index: Track index (0-based) to delete.
    
    Note: If you receive a 422 error, ensure 'index' is sent as a number,
          not a string (e.g., {"index": 0} not {"index": "0"}).
    """
    logger.info(f"delete_track called with index={index} (type: {type(index).__name__})")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        tracks[index].delete()
        logger.info(f"Successfully deleted track at index {index}")
        return {"ok": True}
    except Exception as e:
        error_msg = f"Failed to delete track: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def list_tracks() -> Dict[str, Any]:
    """List tracks with indices and names."""
    return get_project_details()


@mcp.tool()
def get_track_name(index: int) -> Dict[str, Any]:
    """Get the name of a track by index.
    
    Args:
        index: Track index (0-based).
    """
    logger.info(f"get_track_name called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        name = tracks[index].name
        logger.info(f"Track {index} name: '{name}'")
        return {"index": index, "name": name}
    except Exception as e:
        error_msg = f"Failed to get track name: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def get_track_item_count(index: int) -> Dict[str, Any]:
    """Get the number of items on a track by index.
    
    Args:
        index: Track index (0-based).
    """
    logger.info(f"get_track_item_count called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        item_count = tracks[index].n_items
        logger.info(f"Track {index} has {item_count} items")
        return {"index": index, "item_count": item_count}
    except Exception as e:
        error_msg = f"Failed to get track item count: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def set_track_color(index: int, color: tuple) -> Dict[str, Any]:
    """Set the color of a track by index.
    
    Args:
        index: Track index (0-based).
        color: RGB color tuple (e.g., [255, 0, 0] for red). Each value 0-255.
    """
    logger.info(f"set_track_color called with index={index}, color={color}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        # Convert color to tuple if it's a list
        if isinstance(color, list):
            color = tuple(color)
        tracks[index].color = color
        logger.info(f"Successfully set track {index} color to {color}")
        return {"ok": True, "index": index, "color": color}
    except Exception as e:
        error_msg = f"Failed to set track color: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
