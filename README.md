# FlowSim

FlowSim is a modular poi spinning pattern visualizer and animation tool built with Python, Gradio, and Manim. It allows users to select, preview, and export a wide variety of physically accurate poi patterns, including inspin, antispin, box, gunslinger, and more. Patterns are fully modular and hot-reloadable for rapid development and experimentation.

## Features
- Modular pattern architecture (easy to add new patterns)
- Physically accurate math for all patterns
- Gradio GUI for pattern selection, color picking, and animation preview
- Export animations to GIF and MP4
- Automatic scene titling and file naming
- Hot-reload support for pattern development
- Apache 2.0 licensed

## Getting Started
1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd FlowSim
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Launch the app:
   ```sh
   python main.py
   ```
4. Open your browser to `http://localhost:7860` (or the specified port) to use the GUI.

## Usage
- Select patterns for left and right poi from the dropdowns
- Adjust colors, arm/poi lengths, and other options
- Click "Combine Patterns" to preview the animation
- Click "Export GIF" to download the animation as a GIF
- Use "Refresh Patterns" to hot-reload pattern files during development

## Contributing
Contributions are welcome! Please submit pull requests or open issues for new patterns, bug fixes, or feature requests.

## License
This project is licensed under the Apache License 2.0. See `LICENSE` for details.# FlowSim

A simulation and visualization tool for complex poi spinning patterns, including gunslinger poi. Features a Gradio UI and Manim-based animation output.
>>>>>>> 3a11803 (Initial commit for v2.0 update)
