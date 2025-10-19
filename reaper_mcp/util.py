from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Top-level imports for performance/simplicity
import reapy
# Mandatory configuration per python-reapy docs; must run before importing reascript_api
reapy.configure_reaper()
from reapy import reascript_api as RPR

# ----------------------
# Utilities & constants
# ----------------------
PACKAGE_DIR = Path(__file__).parent
SAMPLE_DIRS_FILE = PACKAGE_DIR / "sample_dirs.json"


def _load_sample_dirs() -> List[str]:
    try:
        if SAMPLE_DIRS_FILE.exists():
            with SAMPLE_DIRS_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [d for d in data if isinstance(d, str)]
    except Exception:
        # Be forgiving; return empty on any parse/read error
        pass
    return []


def _save_sample_dirs(dirs: List[str]) -> None:
    with SAMPLE_DIRS_FILE.open("w", encoding="utf-8") as f:
        json.dump(sorted(list(set(dirs))), f, indent=2)


@dataclass
class Note:
    start: float  # seconds
    end: float  # seconds
    pitch: int  # 0-127
    velocity: int = 100  # 1-127
    channel: int = 0  # 0-15


__all__ = [
    "RPR",
    "PACKAGE_DIR",
    "SAMPLE_DIRS_FILE",
    "_load_sample_dirs",
    "_save_sample_dirs",
    "Note",
]
