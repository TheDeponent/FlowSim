import gradio as gr
import importlib
from app.renderer import combine_patterns

PATTERN_OPTIONS = [
    "10 Petal Antispin (Gunslinger)",
    "12 Petal Antispin (Gunslinger)",
    "10 Petal Inspin (Gunslinger)",
    "8 Petal Inspin (Gunslinger)",
    "5 Petal Antispin",
    "5 Petal Antispin (Box)",
    "4 Petal Antispin",
    "4 Petal Antispin (Box)",
    "3 Petal Antispin (Triquetra)",
    "3 Petal Antispin (Box Triquetra)",
    "4 Petal Inspin",
    "2 Petal Inspin (Vertical)",
    "2 Petal Inspin (Horizontal)",
    "1 Petal Inspin (Horizontal)",
    "1 Petal Inspin (Vertical)",
    "Triquetra vs Extension (Gunslinger)",
    "Extension",
    "Half Extension",
    "Pendulum",
    "Extended Pendulum",
    "Isolated Pendulum",
    "Static Spin",
    "Horizontal Cateye",
    "Vertical Cateye",
    "Isolation",
    "CAP (Vertical)",
    "CAP (Horizontal)",
    "Spiral Wrap",
    "Spiral Wrap (Unwraps)",
]

with gr.Blocks() as demo:
    gr.Markdown("# FlowSim")
    with gr.Row(equal_height=True):
        with gr.Column(scale=1, min_width=320):
            refresh_btn = gr.Button("Refresh Patterns", size="sm")
            with gr.Group():
                left_pattern = gr.Dropdown(PATTERN_OPTIONS, label="Left Pattern", value="Extension")
                with gr.Row():
                    left_head_color = gr.ColorPicker(label="Head", value="#000000")
                    left_handle_color = gr.ColorPicker(label="Handle", value="#000000")
                with gr.Row():
                    show_left_head = gr.Checkbox(label="Show Head", value=True)
                    show_left_handle = gr.Checkbox(label="Show Handle", value=True)
                with gr.Row():
                    left_start_side = gr.Dropdown(["Left", "Right"], label="Start Side", value="Right")
                    left_direction = gr.Dropdown(["Clockwise", "Anti-Clockwise"], label="Direction", value="Anti-Clockwise")
            with gr.Group():
                right_pattern = gr.Dropdown(PATTERN_OPTIONS, label="Right Pattern", value="10 Petal Antispin (Gunslinger)")
                with gr.Row():
                    right_head_color = gr.ColorPicker(label="Head", value="#CA1600")
                    right_handle_color = gr.ColorPicker(label="Handle", value="#CA1600")
                with gr.Row():
                    show_right_head = gr.Checkbox(label="Show Head", value=True)
                    show_right_handle = gr.Checkbox(label="Show Handle", value=True)
                with gr.Row():
                    right_start_side = gr.Dropdown(["Left", "Right"], label="Start Side", value="Right")
                    right_direction = gr.Dropdown(["Clockwise", "Anti-Clockwise"], label="Direction", value="Anti-Clockwise")
            combine_btn = gr.Button("Combine Patterns")
            export_gif_btn = gr.Button("Export GIF", size="sm")
            with gr.Row():
                gif_file = gr.File(label=None, visible=False)
        with gr.Column(scale=2, min_width=1100):
            output = gr.Video(label="Combined Pattern Animation", height=700, width=1100, autoplay=True)

    def color_to_hex(c):
        if isinstance(c, str):
            if c.startswith("rgba"):
                parts = c[5:-1].split(',')
                r, g, b = [max(0, min(255, int(float(x)))) for x in parts[:3]]
                return '#{:02x}{:02x}{:02x}'.format(r, g, b)
            if c.startswith("#") and len(c) == 7:
                return c
            named_colors = {
                'white': '#FFFFFF',
                'black': '#000000',
                'red': '#FF0000',
                'green': '#00FF00',
                'blue': '#0000FF',
                'yellow': '#FFFF00',
                'cyan': '#00FFFF',
                'magenta': '#FF00FF',
            }
            if c.lower() in named_colors:
                return named_colors[c.lower()]
        return "#FF0000"

    def combine_patterns_gui(
        left_pattern, left_head_color, left_handle_color, left_arm_length, left_poi_length, left_start_side, left_direction,
        right_pattern, right_head_color, right_handle_color, right_arm_length, right_poi_length, right_start_side, right_direction,
        show_left_head, show_left_handle, show_right_head, show_right_handle,
        frame_idx=0, preview_mode=False
    ):
        return combine_patterns(
            left_pattern,
            color_to_hex(left_head_color),
            color_to_hex(left_handle_color),
            left_arm_length, left_poi_length, left_start_side, left_direction,
            right_pattern,
            color_to_hex(right_head_color),
            color_to_hex(right_handle_color),
            right_arm_length, right_poi_length, right_start_side, right_direction,
            show_left_head, show_left_handle, show_right_head, show_right_handle,
            frame_idx, preview_mode
        )

    combine_btn.click(
        combine_patterns_gui,
        inputs=[
            left_pattern, left_head_color, left_handle_color, gr.State(0.7), gr.State(0.45), left_start_side, left_direction,
            right_pattern, right_head_color, right_handle_color, gr.State(0.7), gr.State(0.45), right_start_side, right_direction,
            show_left_head, show_left_handle, show_right_head, show_right_handle,
            gr.State(0), gr.State(False)
        ],
        outputs=output
    )
    def export_gif_gui():
        from app.renderer import export_gif
        return export_gif()

    export_gif_btn.click(export_gif_gui, outputs=gif_file)
    export_gif_btn.click(lambda: gr.update(visible=True), outputs=gif_file)

    def refresh_patterns():
        import sys
        # Reload all submodules in app.patterns
            # Collect all submodule names first to avoid RuntimeError
        module_names = [name for name in sys.modules if name.startswith("app.patterns.") and sys.modules[name] is not None]
        for name in module_names:
            importlib.reload(sys.modules[name])


    refresh_btn.click(refresh_patterns, outputs=None)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")

