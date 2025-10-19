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


@mcp.tool()
def mute_track(index: int) -> Dict[str, Any]:
    """Mute a track by index.
    
    Args:
        index: Track index (0-based).
    """
    logger.info(f"mute_track called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        tracks[index].mute()
        logger.info(f"Successfully muted track {index}")
        return {"ok": True, "index": index, "muted": True}
    except Exception as e:
        error_msg = f"Failed to mute track: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def unmute_track(index: int) -> Dict[str, Any]:
    """Unmute a track by index.
    
    Args:
        index: Track index (0-based).
    """
    logger.info(f"unmute_track called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        tracks[index].unmute()
        logger.info(f"Successfully unmuted track {index}")
        return {"ok": True, "index": index, "muted": False}
    except Exception as e:
        error_msg = f"Failed to unmute track: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def solo_track(index: int) -> Dict[str, Any]:
    """Solo a track by index.
    
    Args:
        index: Track index (0-based).
    """
    logger.info(f"solo_track called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        tracks[index].solo()
        logger.info(f"Successfully soloed track {index}")
        return {"ok": True, "index": index, "solo": True}
    except Exception as e:
        error_msg = f"Failed to solo track: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def unsolo_track(index: int) -> Dict[str, Any]:
    """Unsolo a track by index.
    
    Args:
        index: Track index (0-based).
    """
    logger.info(f"unsolo_track called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        tracks[index].unsolo()
        logger.info(f"Successfully unsoloed track {index}")
        return {"ok": True, "index": index, "solo": False}
    except Exception as e:
        error_msg = f"Failed to unsolo track: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def get_track_volume(index: int) -> Dict[str, Any]:
    """Get the volume of a track by index.
    
    Args:
        index: Track index (0-based).
    
    Returns:
        Dict with volume (0.0 to 2.0+, where 1.0 = 0dB)
    """
    logger.info(f"get_track_volume called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        volume = tracks[index].get_info_value("D_VOL")
        logger.info(f"Track {index} volume: {volume}")
        return {"index": index, "volume": volume}
    except Exception as e:
        error_msg = f"Failed to get track volume: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def set_track_volume(index: int, volume: float) -> Dict[str, Any]:
    """Set the volume of a track by index.
    
    Args:
        index: Track index (0-based).
        volume: Volume value (0.0 to 2.0+, where 1.0 = 0dB, 0.0 = -inf dB).
    """
    logger.info(f"set_track_volume called with index={index}, volume={volume}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        tracks[index].set_info_value("D_VOL", float(volume))
        logger.info(f"Successfully set track {index} volume to {volume}")
        return {"ok": True, "index": index, "volume": volume}
    except Exception as e:
        error_msg = f"Failed to set track volume: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def get_track_pan(index: int) -> Dict[str, Any]:
    """Get the pan of a track by index.
    
    Args:
        index: Track index (0-based).
    
    Returns:
        Dict with pan (-1.0 = left, 0.0 = center, 1.0 = right)
    """
    logger.info(f"get_track_pan called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        pan = tracks[index].get_info_value("D_PAN")
        logger.info(f"Track {index} pan: {pan}")
        return {"index": index, "pan": pan}
    except Exception as e:
        error_msg = f"Failed to get track pan: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def set_track_pan(index: int, pan: float) -> Dict[str, Any]:
    """Set the pan of a track by index.
    
    Args:
        index: Track index (0-based).
        pan: Pan value (-1.0 = full left, 0.0 = center, 1.0 = full right).
    """
    logger.info(f"set_track_pan called with index={index}, pan={pan}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        # Clamp pan to valid range
        pan_value = max(-1.0, min(1.0, float(pan)))
        tracks[index].set_info_value("D_PAN", pan_value)
        logger.info(f"Successfully set track {index} pan to {pan_value}")
        return {"ok": True, "index": index, "pan": pan_value}
    except Exception as e:
        error_msg = f"Failed to set track pan: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def select_track(index: int) -> Dict[str, Any]:
    """Select a track by index.
    
    Args:
        index: Track index (0-based).
    """
    logger.info(f"select_track called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        tracks[index].select()
        logger.info(f"Successfully selected track {index}")
        return {"ok": True, "index": index, "selected": True}
    except Exception as e:
        error_msg = f"Failed to select track: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def unselect_track(index: int) -> Dict[str, Any]:
    """Unselect a track by index.
    
    Args:
        index: Track index (0-based).
    """
    logger.info(f"unselect_track called with index={index}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            error_msg = f"Track index out of range: {index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        tracks[index].unselect()
        logger.info(f"Successfully unselected track {index}")
        return {"ok": True, "index": index, "selected": False}
    except Exception as e:
        error_msg = f"Failed to unselect track: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
