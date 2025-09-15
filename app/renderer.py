import os
import importlib
from manim import config, tempconfig, Scene, Dot, Text, VMobject, Line, UP, DOWN, UpdateFromAlphaFunc, always_redraw
from app.patterns.constants import ARM_LENGTH, POI_LENGTH, NUM_POINTS
import moviepy as mpy


def combine_patterns(
    left_pattern, left_head_color, left_handle_color, left_arm_length, left_poi_length, left_start_side, left_direction,
    right_pattern, right_head_color, right_handle_color, right_arm_length, right_poi_length, right_start_side, right_direction,
    show_left_head, show_left_handle, show_right_head, show_right_handle,
    frame_idx=0, preview_mode=False
):
    config.pixel_height = 1200
    config.pixel_width = 1200
    config.frame_height = 4.0
    config.frame_width = 4.0
    config.background_color = "#222222"
    config.disable_caching = True  # Disable Manim cache to force fresh render

    # Map GUI names to (module, function) pairs
    pattern_lookup = {
        "Triquetra vs Extension (Gunslinger)": ("TriquetraVsExtensionGunslinger", "generate_TriquetraVsExtensionGunslinger"),
        "Half Extension": ("HalfExtension", "generate_HalfExtension"),
        "Extension": ("Extension", "generate_Extension"),
        "10 Petal Antispin (Gunslinger)": ("TenPetalAnti", "generate_TenPetalAnti"),
        "12 Petal Antispin (Gunslinger)": ("TwelvePetalAnti", "generate_TwelvePetalAnti"),
        "10 Petal Inspin (Gunslinger)": ("TenPetalInspin", "generate_TenPetalInspin"),
        "8 Petal Inspin (Gunslinger)": ("EightPetalInspin", "generate_EightPetalInspin"),
        "5 Petal Antispin": ("FivePetalAntispin", "generate_FivePetalAntispin"),
        "5 Petal Antispin (Box)": ("FivePetalAntispinBox", "generate_FivePetalAntispinBox"),
        "4 Petal Antispin": ("FourPetalAnti", "generate_FourPetalAnti"),
        "4 Petal Antispin (Box)": ("FourPetalAntiBox", "generate_FourPetalAntiBox"),
        "3 Petal Antispin (Triquetra)": ("Triquetra", "generate_Triquetra"),
        "3 Petal Antispin (Box Triquetra)": ("TriquetraBox", "generate_TriquetraBox"),
        "4 Petal Inspin": ("FourPetalInspin", "generate_FourPetalInspin"),
        "2 Petal Inspin (Vertical)": ("TwoPetalInspin", "generate_TwoPetalInspin"),
        "2 Petal Inspin (Horizontal)": ("TwoPetalInspinHorizontal", "generate_TwoPetalInspinHorizontal"),
        "1 Petal Inspin (Horizontal)": ("OnePetalInspin", "generate_OnePetalInspin"),
        "1 Petal Inspin (Vertical)": ("OnePetalInspinVertical", "generate_OnePetalInspinVertical"),
        "Pendulum": ("Pendulum", "generate_Pendulum"),
        "Extended Pendulum": ("ExtendedPendulum", "generate_ExtendedPendulum"),
        "Isolated Pendulum": ("IsolatedPendulum", "generate_IsolatedPendulum"),
        "Static Spin": ("StaticSpin", "generate_StaticSpin"),
        "Horizontal Cateye": ("HorizontalCateye", "generate_HorizontalCateye"),
        "Vertical Cateye": ("CatEye", "generate_CatEye"),
        "Isolation": ("Isolation", "generate_Isolation"),
        "CAP (Vertical)": ("CAPAntispin", "generate_CAPAntispin"),
        "CAP (Horizontal)": ("CAPHorizontal", "generate_CAPHorizontal"),
        "Spiral Wrap": ("Spiral", "generate_Spiral"),
        "Spiral Wrap (Unwraps)": ("SpiralWrapUnwraps", "generate_SpiralWrapUnwraps"),
    }

    pattern_map = {}
    for gui_name, (mod_name, func_name) in pattern_lookup.items():
        mod = importlib.import_module(f"app.patterns.{mod_name}")
        pattern_map[gui_name] = getattr(mod, func_name)

    fallback_func = next(iter(pattern_map.values()))
    left_func = pattern_map.get(left_pattern, fallback_func)
    right_func = pattern_map.get(right_pattern, fallback_func)

    left_args = dict(
        arm_length=ARM_LENGTH,
        poi_length=POI_LENGTH,
        num_points=NUM_POINTS,
        head_color=left_head_color,
        handle_color=left_handle_color,
        start_side=str(left_start_side).lower(),
        rotation_direction=str(left_direction).lower().replace("-", "")
    )
    right_args = dict(
        arm_length=ARM_LENGTH,
        poi_length=POI_LENGTH,
        num_points=NUM_POINTS,
        head_color=right_head_color,
        handle_color=right_handle_color,
        start_side=str(right_start_side).lower(),
        rotation_direction=str(right_direction).lower().replace("-", "")
    )

    import inspect
    left_params = inspect.signature(left_func).parameters
    right_params = inspect.signature(right_func).parameters
    left_call_args = {k: v for k, v in left_args.items() if k in left_params}
    right_call_args = {k: v for k, v in right_args.items() if k in right_params}
    left_result = left_func(**left_call_args)
    right_result = right_func(**right_call_args)

    def get_string_points(result):
        # If pattern returns intermediate string points, use them
        if len(result) == 5:
            head_x, head_y, handle_x, handle_y, string_points = result
            def points(idx):
                # string_points[idx] is a list of control points for this frame
                return [ [handle_x[idx], handle_y[idx], 0], *[ [p[0], p[1], 0] for p in string_points[idx] ], [head_x[idx], head_y[idx], 0] ]
            return points
        else:
            head_x, head_y, handle_x, handle_y = result
            return lambda idx: [ [handle_x[idx], handle_y[idx], 0], [head_x[idx], head_y[idx], 0] ]

    left_x, left_y, left_handle_x, left_handle_y = left_result[:4]
    right_x, right_y, right_handle_x, right_handle_y = right_result[:4]

    # Determine scene title based on visible poi
    if (not show_left_head and not show_left_handle) and (show_right_head or show_right_handle):
        scene_title = f"{right_pattern}"
    elif (not show_right_head and not show_right_handle) and (show_left_head or show_left_handle):
        scene_title = f"{left_pattern}"
    elif (not show_left_head and not show_left_handle) and (not show_right_head and not show_right_handle):
        scene_title = ""
    else:
        scene_title = f"{left_pattern} vs {right_pattern}"

    # Split scene title over two lines if too long
    max_title_chars = 35
    if len(scene_title) > max_title_chars and " vs " in scene_title:
        parts = scene_title.split(" vs ")
        # Put the longer string on top
        if len(parts[0]) >= len(parts[1]):
            scene_title = f"{parts[0]}\nvs {parts[1]}"
        else:
            scene_title = f"{parts[1]}\nvs {parts[0]}"

    # Axis label for timing/direction
    left_start = str(left_start_side).lower()
    right_start = str(right_start_side).lower()
    left_dir = str(left_direction).lower()
    right_dir = str(right_direction).lower()
    if left_start == right_start and left_dir == right_dir:
        axis_label = "Same Time Same Direction"
    elif left_start == right_start and left_dir != right_dir:
        axis_label = "Same Time Opposite Direction"
    elif left_start != right_start and left_dir == right_dir:
        axis_label = "Split Time Same Direction"
    else:
        axis_label = "Split Time Opposite Direction"

    class CombinedPatternScene(Scene):
        def construct(self):
            # Dynamically size title to fit frame width
            max_title_width = config.frame_width * 0.9
            base_font_size = 24
            min_font_size = 14
            est_font_size = max(min_font_size, min(base_font_size, int(base_font_size * max_title_width / (len(scene_title.replace('\n', '')) + 8))))
            if "\n" in scene_title:
                title_lines = scene_title.split("\n")
                title_objs = [Text(line, font_size=est_font_size) for line in title_lines]
                # Stack the lines vertically with a small buffer
                title_objs[0].to_edge(UP, buff=0.04)
                title_objs[1].next_to(title_objs[0], DOWN, buff=0.08)
                for t in title_objs:
                    self.add(t)
            else:
                title = Text(scene_title, font_size=est_font_size).to_edge(UP, buff=0.04)
                self.add(title)
            # Hide axis label if both head and handle of one poi are unticked
            hide_axis = (not show_left_head and not show_left_handle) or (not show_right_head and not show_right_handle)
            if not hide_axis:
                label = Text(axis_label, font_size=14).to_edge(DOWN, buff=0.12)
                self.add(label)
            from manim import ValueTracker, always_redraw, Line
            dot_radius = 0.05
            progress = ValueTracker(0)

            # Position history lists for trails
            left_head_history = []
            left_handle_history = []
            right_head_history = []
            right_handle_history = []

            # Dots
            left_dot_head = Dot(color=left_head_color, radius=dot_radius) if show_left_head else None
            left_dot_handle = Dot(color=left_handle_color, radius=dot_radius) if show_left_handle else None
            right_dot_head = Dot(color=right_head_color, radius=dot_radius) if show_right_head else None
            right_dot_handle = Dot(color=right_handle_color, radius=dot_radius) if show_right_handle else None

            # Updaters for dots: update position and append to history
            def dot_updater_factory(x, y, history):
                def updater(mob):
                    idx = int(progress.get_value() * (len(x) - 1))
                    idx = min(idx, len(x) - 1)  # Clamp to last index
                    pos = [x[idx], y[idx], 0]
                    mob.move_to(pos)
                    if len(history) == 0 or history[-1] != pos:
                        history.append(pos)
                return updater

            if left_dot_head:
                left_dot_head.add_updater(dot_updater_factory(left_x, left_y, left_head_history))
            if left_dot_handle:
                left_dot_handle.add_updater(dot_updater_factory(left_handle_x, left_handle_y, left_handle_history))
            if right_dot_head:
                right_dot_head.add_updater(dot_updater_factory(right_x, right_y, right_head_history))
            if right_dot_handle:
                right_dot_handle.add_updater(dot_updater_factory(right_handle_x, right_handle_y, right_handle_history))

            # Helper for safe trail rendering
            def safe_trail(history, color):
                if len(history) > 1:
                    pts = history
                elif len(history) == 1:
                    pts = [history[0], history[0]]
                else:
                    pts = [[0,0,0],[0,0,0]]
                return VMobject().set_points_as_corners(pts).set_color(color).set_stroke(width=4)

            # Trails using always_redraw and history
            left_head_trail = always_redraw(lambda: safe_trail(left_head_history, left_head_color)) if show_left_head else None
            left_handle_trail = always_redraw(lambda: safe_trail(left_handle_history, left_handle_color)) if show_left_handle else None
            right_head_trail = always_redraw(lambda: safe_trail(right_head_history, right_head_color)) if show_right_head else None
            right_handle_trail = always_redraw(lambda: safe_trail(right_handle_history, right_handle_color)) if show_right_handle else None

            # Add trails before dots
            for trail in [left_head_trail, left_handle_trail, right_head_trail, right_handle_trail]:
                if trail:
                    self.add(trail)
            def make_string_bendable(idx, get_points):
                pts = get_points(idx)
                if len(pts) == 3:
                    mob = VMobject().set_points_as_corners(pts).set_color("#FFFFFF").set_stroke(width=1.5)
                elif len(pts) > 3:
                    mob = VMobject().set_points_smoothly(pts).set_color("#FFFFFF").set_stroke(width=1.5)
                else:
                    mob = Line(pts[0], pts[1], color="#FFFFFF", stroke_width=1.5)
                return mob

            # Create and add bendable string objects with updaters
            if left_dot_handle and left_dot_head:
                left_string = make_string_bendable(0, get_string_points(left_result))
                def left_string_updater(mob):
                    idx = int(progress.get_value() * (len(left_x) - 1))
                    idx = min(idx, len(left_x) - 1)
                    pts = get_string_points(left_result)(idx)
                    if len(pts) > 2:
                        mob.set_points_smoothly(pts)
                    else:
                        mob.put_start_and_end_on(pts[0], pts[1])
                left_string.add_updater(left_string_updater)
                self.add(left_string)
            if right_dot_handle and right_dot_head:
                right_string = make_string_bendable(0, get_string_points(right_result))
                def right_string_updater(mob):
                    idx = int(progress.get_value() * (len(right_x) - 1))
                    idx = min(idx, len(right_x) - 1)
                    pts = get_string_points(right_result)(idx)
                    if len(pts) > 2:
                        mob.set_points_smoothly(pts)
                    else:
                        mob.put_start_and_end_on(pts[0], pts[1])
                right_string.add_updater(right_string_updater)
                self.add(right_string)
            for dot in [left_dot_head, left_dot_handle, right_dot_head, right_dot_handle]:
                if dot:
                    self.add(dot)

            # Animate the ValueTracker slightly past 1 to guarantee last frame
            n_frames = len(left_x)
            overshoot = 1 + 10/(n_frames - 1)
            self.play(progress.animate.set_value(overshoot), run_time=4, rate_func=lambda t: t)

    if preview_mode:
        img_path = os.path.join(os.getcwd(), f"preview_frame_{frame_idx}.png")
        with tempconfig({"output_file": img_path, "format": "png"}):
            scene = CombinedPatternScene()
            scene.render()
        return img_path
    else:
        video_path = os.path.join(os.getcwd(), "combined_pattern.mp4")
        # Ensure any existing video file is deleted before rendering
        if os.path.exists(video_path):
            os.remove(video_path)
        with tempconfig({"output_file": video_path, "format": "mp4"}):
            scene = CombinedPatternScene()
            scene.render()
    global last_video_path, last_scene_title
    last_video_path = video_path
    last_scene_title = scene_title
    return video_path

def export_gif():
    try:
        scene_title = last_scene_title
    except Exception:
        scene_title = "combined_pattern"
    # Sanitize filename
    safe_title = scene_title.replace(" ", "_").replace("/", "-").replace("\\", "-")
    gif_path = os.path.join(os.getcwd(), f"{safe_title}.gif")
    clip = mpy.VideoFileClip(last_video_path)
    clip.write_gif(gif_path, fps=24)
    clip.close()  # Ensure file handle is released
    return gif_path
