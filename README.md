
Reaper MCP Server

Small, focused Model Context Protocol (MCP) server for REAPER DAW automation using python-reapy / ReaScript.

Requirements
- REAPER installed and running
- ReaScript enabled and python-reapy bridge configured if running outside REAPER
- Python >= 3.13

Install
- Clone repo and install dependencies
  - Using uv: uv sync
  - Or pip: pip install -e .

Run
- Start the MCP server (stdio transport by default):
  python -m reaper_mcp
- Run over SSE/HTTP (if supported by fastmcp):
  python -m reaper_mcp --transport sse --host 127.0.0.1 --port 8765
- Allow specific CORS origins (can be repeated):
  python -m reaper_mcp --transport sse --allow-origin http://localhost:3000 --allow-origin https://your.app

Notes
- Tools are small and composable. Prefer multiple simple calls over one giant action.
- Some tools depend on OS-specific REAPER resource files.
- Paths must be accessible to the machine running REAPER.

Tools Overview
- Project
  - new_project(clear_tracks=True) -> {ok}
  - get_project_details() -> {bpm, track_count, tracks}
- Tracks
  - create_track(name=None, index=None) -> {index, name}
  - delete_track(index) -> {ok}
  - list_tracks() -> {bpm, track_count, tracks}
- Tempo
  - get_bpm() -> {bpm}
  - set_bpm(bpm) -> {bpm}
- MIDI
  - generate_midi_pattern(root_midi_note=60, scale="major", bars=1, steps_per_bar=16, velocity=96) -> {notes[]}
  - add_midi_to_track(track_index, notes[], start_time=0.0) -> {ok}
  - generate_pretty_midi(...) -> {midi_base64, bpm}
  - add_midi_file_to_track(track_index, midi_base64, insert_time=0.0) -> {ok}
- Plugins / FX
  - list_vst_plugins() -> {plugins[]}
  - add_fx_to_track(track_index, fx_name, record_fx_chain=False) -> {track_index, fx_index}
  - list_fx_on_track(track_index) -> {fx[]}
  - set_fx_param(track_index, fx_index, param_index, value_normalized) -> {ok}
  - get_fx_param(track_index, fx_index, param_index) -> {value_normalized, name}
- Samples
  - list_sample_dirs() -> {sample_dirs[]}
  - add_sample_dir(path) -> {sample_dirs[]}
  - remove_sample_dir(path) -> {sample_dirs[]}
  - search_samples(query=None, exts=None, limit=100) -> {files[]}
  - import_sample_to_track(track_index, file_path, insert_time=0.0, time_stretch_playrate=None) -> {ok}

Using with Open WebUI on a different machine (and remote Ollama)
- Scenario: REAPER + this MCP server run on your local PC. Open WebUI and Ollama run on another machine or server. You want Open WebUI to call these MCP tools over the network.

1) Start the MCP server on the REAPER PC (SSE over the network)
- Find your REAPER PC's LAN IP (e.g., 192.168.1.50).
- Start with SSE transport and listen on all interfaces. Add your Open WebUI origin for CORS:
  python -m reaper_mcp --transport sse --host 0.0.0.0 --port 8765 --allow-origin http://OPENWEBUI_HOST:3000
  - Replace OPENWEBUI_HOST:3000 with the exact origin you open in your browser when using Open WebUI (scheme://host:port). Examples:
    - http://openwebui.local:3000
    - http://10.0.0.12:8080
    - https://your-domain.example
  - You can repeat --allow-origin multiple times if needed.
- Open the firewall on the REAPER PC for TCP port 8765, or change --port to an allowed port.

2) Connect from Open WebUI
- In Open WebUI, add this MCP server as an external MCP/Tools server (wording may vary by version):
  - Name: Reaper MCP
  - Server URL: http://REAPER_PC_IP:8765
  - Transport/Type: SSE or HTTP (if the UI asks)
  - Path: leave empty unless you started the server with --path
- Save, then test connection. You should see tools like Project, Tracks, Tempo, MIDI, FX, Samples become available.

3) Remote Ollama note
- Ollama can run anywhere reachable by Open WebUI; it is independent from this MCP server. Set your model/provider in Open WebUI as usual. The MCP server only needs to be reachable from wherever the Open WebUI client makes requests (often your browser).

4) Tunneling options (if machines can't reach each other directly)
- SSH local forward (connect from your browser/Open WebUI machine to the REAPER PC):
  ssh -N -L 8765:127.0.0.1:8765 user@REAPER_PC
  - Then use Server URL: http://127.0.0.1:8765 in Open WebUI.
- SSH reverse forward (REAPER PC exposes to a stable host your Open WebUI can reach):
  ssh -N -R 18765:127.0.0.1:8765 user@STABLE_HOST
  - Then use Server URL: http://STABLE_HOST:18765 in Open WebUI and start the MCP server on the REAPER PC as before.

Troubleshooting
- CORS error in browser dev tools: The origin in your --allow-origin does not match exactly the Open WebUI page origin you loaded. Fix and restart the MCP server.
- Connection refused/timeout: Check the REAPER PC firewall and IP/port. Verify the server is running: python -m reaper_mcp --transport sse --host 0.0.0.0 --port 8765
- 404 or unexpected path: Leave Path empty in Open WebUI unless you started the server with --path. If you did, supply the same path there.
- Tools show but fail at runtime: Ensure REAPER is running and python-reapy is configured. Many operations require an open project or valid tracks.

Caveats
- REAPER actions are executed via ReaScript API; some behaviors depend on your settings.
- The server returns helpful error messages if REAPER bridge is unavailable.
