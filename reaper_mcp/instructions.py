INSTRUCTIONS = f"""
Reaper MCP Server

This server exposes small, focused tools to automate common REAPER tasks via reapy / ReaScript.

Available Tools

Project:
- get_project_details: Get basic project details (bpm, track count, track names)
- new_project: Initialize the current project (optionally clearing all tracks)
- get_project_length: Get the project length in seconds
- save_project: Save the current project
- get_play_state: Get the current playback state (playing, paused, stopped, recording)
- get_play_position: Get the current play position in seconds
- get_play_rate: Get the current playback rate (1.0 is normal speed)

Tracks:
- create_track: Create a new track at optional index; returns its index
- delete_track: Delete track by index
- list_tracks: List tracks with indices and names
- get_track_name: Get the name of a track by index
- get_track_item_count: Get the number of items on a track by index
- set_track_color: Set the color of a track by index (RGB tuple, 0-255)

Tempo:
- get_bpm: Get current project BPM
- set_bpm: Set current project BPM (must be between 1 and 960)

MIDI:
- add_midi_to_track: Add a list of MIDI notes to a track as a new MIDI item
- generate_midi_pattern: Generate a simple step-sequenced MIDI pattern (returns note data for add_midi_to_track)
- generate_pretty_midi: Generate a MIDI file (base64) using pretty_midi following a simple step sequence
- add_midi_file_to_track: Import a MIDI file (base64-encoded .mid data) onto a track at time position

FX/Plugins:
- list_vst_plugins: List available VST plugins by parsing REAPER resource files (vstplugins*.ini)
- add_fx_to_track: Add an FX/VST by name to a track (fx_name must match REAPER's FX browser name)
- list_fx_on_track: List FX names on a given track
- set_fx_param: Set an FX parameter (normalized 0..1)
- get_fx_param: Get an FX parameter value and name

Samples:
- list_sample_dirs: List configured sample directories
- add_sample_dir: Add a sample directory (persisted)
- remove_sample_dir: Remove a sample directory
- search_samples: Search for audio samples across configured directories (supports query filter, extension filter, and limit)
- import_sample_to_track: Import a sample onto a track at time position (optionally set take playrate for time-stretching)

Caveats
- Some operations depend on REAPER configuration, OS, and installed plugins. Tools return helpful error messages when unavailable.
"""