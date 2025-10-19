from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import reapy

from reaper_mcp.mcp_core import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
def add_marker(position: float, name: str = "", color: int = 0) -> Dict[str, Any]:
    """Add a marker to the project at the specified time position.
    
    Args:
        position: Time position in seconds
        name: Optional marker name
        color: Optional color as integer (0 for default)
    
    Returns:
        Dict with marker index on success or error message
    """
    logger.info(f"add_marker called with position={position}, name='{name}', color={color}")
    try:
        project = reapy.Project()
        index = project.add_marker(position=float(position), name=name, color=int(color))
        logger.info(f"Successfully added marker at position {position}")
        return {"ok": True, "index": index, "position": position, "name": name}
    except Exception as e:
        error_msg = f"Failed to add marker: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def add_region(start: float, end: float, name: str = "", color: int = 0) -> Dict[str, Any]:
    """Add a region to the project between start and end time positions.
    
    Args:
        start: Start time position in seconds
        end: End time position in seconds
        name: Optional region name
        color: Optional color as integer (0 for default)
    
    Returns:
        Dict with region index on success or error message
    """
    logger.info(f"add_region called with start={start}, end={end}, name='{name}', color={color}")
    try:
        project = reapy.Project()
        index = project.add_region(start=float(start), end=float(end), name=name, color=int(color))
        logger.info(f"Successfully added region from {start} to {end}")
        return {"ok": True, "index": index, "start": start, "end": end, "name": name}
    except Exception as e:
        error_msg = f"Failed to add region: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def list_markers() -> Dict[str, Any]:
    """List all markers in the project.
    
    Returns:
        Dict with list of markers, each containing index, position, and name
    """
    logger.info("list_markers called")
    try:
        project = reapy.Project()
        markers_list = []
        for marker in project.markers:
            markers_list.append({
                "index": marker.index,
                "position": marker.position,
                "name": marker.name,
                "color": marker.color
            })
        logger.info(f"Found {len(markers_list)} markers")
        return {"markers": markers_list, "count": len(markers_list)}
    except Exception as e:
        error_msg = f"Failed to list markers: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def list_regions() -> Dict[str, Any]:
    """List all regions in the project.
    
    Returns:
        Dict with list of regions, each containing index, start, end, and name
    """
    logger.info("list_regions called")
    try:
        project = reapy.Project()
        regions_list = []
        for region in project.regions:
            regions_list.append({
                "index": region.index,
                "start": region.start,
                "end": region.end,
                "name": region.name,
                "color": region.color
            })
        logger.info(f"Found {len(regions_list)} regions")
        return {"regions": regions_list, "count": len(regions_list)}
    except Exception as e:
        error_msg = f"Failed to list regions: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@mcp.tool()
def get_marker_count() -> Dict[str, Any]:
    """Get the number of markers in the project.
    
    Returns:
        Dict with marker count
    """
    try:
        project = reapy.Project()
        count = project.n_markers
        return {"count": count}
    except Exception as e:
        return {"error": f"Failed to get marker count: {e}"}


@mcp.tool()
def get_region_count() -> Dict[str, Any]:
    """Get the number of regions in the project.
    
    Returns:
        Dict with region count
    """
    try:
        project = reapy.Project()
        count = project.n_regions
        return {"count": count}
    except Exception as e:
        return {"error": f"Failed to get region count: {e}"}
