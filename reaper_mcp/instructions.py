INSTRUCTIONS = f"""
Reaper MCP Server

This server exposes small, focused tools to automate common REAPER tasks via reapy / ReaScript.

Notes
- You must run REAPER with ReaScript enabled and have the `python-reapy` bridge configured for out-of-process control.
- Tools are designed to be small and encapsulated. Prefer calling multiple small tools over one large combined action.
- Paths must be accessible from the REAPER host machine.

Key capabilities
- Project: create/initialize a project, query project details.
- Tracks: create/delete/list tracks.
- Transport/tempo: get/set BPM.
- MIDI: add MIDI to a track from note data; generate basic MIDI patterns using pretty_midi.
- Plugins/FX: list available VST plugins from REAPER resource files; add FX/VST to a track; get/set FX parameters.
- Samples: manage multiple sample directories; search and import samples; optionally time-scale via item/take playrate.

Caveats
- Some operations depend on REAPER configuration, OS, and installed plugins. Tools return helpful error messages when unavailable.
"""