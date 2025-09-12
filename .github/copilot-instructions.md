# Copilot Instructions for FlowSim

## Project Overview
FlowSim is a modular poi spinning pattern visualizer and animation tool built with Python, Gradio, and Manim. It enables users to select, preview, and export physically accurate poi patterns, supporting inspin, antispin, box, gunslinger, and more. The architecture is designed for rapid pattern development and hot-reloading.

## Architecture & Key Files
- `app/patterns/`: Contains all modular pattern implementations. Each pattern is a separate file with a `generate_*` function. Patterns use shared constants from `app/patterns/constants.py`.
- `app/renderer.py`: Central animation logic. Imports all patterns, maps pattern names to functions, and manages scene title, animation, and export (GIF/MP4). Handles ValueTracker logic for frame completion.
- `app/__GUI.py`: Gradio-based user interface. Dropdowns for pattern selection, color pickers, export buttons, and refresh logic for hot-reloading patterns. Integrates with renderer and exposes export/download options.
- `main.py`: Entry point for launching the Gradio app.
- `requirements.txt`: Lists all dependencies (gradio, manim, numpy, matplotlib, imageio, moviepy).
- `CHANGELOG.md`, `LICENSE`, `.gitignore`: Standard project files.

## Developer Workflows
- **Run the app:** `python main.py` (launches Gradio UI)
- **Hot-reload patterns:** Use the "Refresh Patterns" button in the UI to reload all pattern modules without restarting the app.
- **Export animation:** Use "Export GIF" to generate a GIF with the scene title as filename; download via the UI.
- **Add new patterns:** Create a new file in `app/patterns/` with a `generate_*` function. Update `renderer.py` and `__GUI.py` to register the new pattern.
- **Dependencies:** Install with `pip install -r requirements.txt`.

## Project-Specific Conventions
- **Pattern Functions:** Each pattern file must define a `generate_*` function with the signature `(arm_length, poi_length, num_points, start_side, rotation_direction)`.
- **Scene Title:** Scene titles are auto-generated in `renderer.py` and used for GIF/MP4 filenames.
- **File Naming:** Exported GIFs/MP4s use the scene title for easy identification.
- **Media Folder:** The `media/` folder is kept for structure but all files inside are gitignored.
- **No Preview for GIF Download:** The GIF download box in the UI is minimal and only appears after export.

## Integration Points
- **Gradio <-> Renderer:** The UI calls `combine_patterns` and `export_gif` in `renderer.py`.
- **Pattern Hot-Reload:** Uses `importlib.reload` on all `app.patterns.*` modules.
- **MoviePy:** Used for GIF export and file handling.

## Examples
- To add a new pattern, copy an existing file in `app/patterns/`, implement the math, and register it in both `renderer.py` (pattern_map) and `__GUI.py` (PATTERN_OPTIONS).
- To ensure animation completes, ValueTracker in `renderer.py` overshoots slightly and clamps indices.

## Notes
- All code should follow the modular pattern structure for easy hot-reloading and extension.
- Scene title logic is critical for file naming and UI clarity.
- For debugging, check the UI refresh logic and ValueTracker frame completion in `renderer.py`.

---

Please review and suggest any additions or clarifications for your team's workflow or conventions.
