import os
from manim import config, tempconfig, Scene, Dot, Text, VMobject, Line, UP, DOWN, UpdateFromAlphaFunc, always_redraw


def combine_patterns(
    left_pattern, left_head_color, left_handle_color, left_arm_length, left_poi_length, left_start_side, left_direction,
    right_pattern, right_head_color, right_handle_color, right_arm_length, right_poi_length, right_start_side, right_direction,
    show_left_head, show_left_handle, show_right_head, show_right_handle,
    frame_idx=0, preview_mode=False
):
    from app.patterns.HorizontalCateye import generate_HorizontalCateye
    from app.patterns.TwelvePetalAnti import generate_TwelvePetalAnti
    from app.patterns.TenPetalAnti import generate_TenPetalAnti
    from app.patterns.Extension import generate_Extension
    from app.patterns.FourPetalAnti import generate_FourPetalAnti
    from app.patterns.FivePetalAntispin import generate_FivePetalAntispin
    from app.patterns.FourPetalAntiBox import generate_FourPetalAntiBox
    from app.patterns.ExtendedPendulum import generate_ExtendedPendulum
    from app.patterns.Pendulum import generate_Pendulum
    from app.patterns.Triquetra import generate_Triquetra
    from app.patterns.CatEye import generate_CatEye
    from app.patterns.StaticSpin import generate_StaticSpin
    from app.patterns.Isolation import generate_Isolation
    from app.patterns.IsolatedPendulum import generate_IsolatedPendulum
    from app.patterns.TwoPetalInspin import generate_TwoPetalInspin
    from app.patterns.TwoPetalInspinHorizontal import generate_TwoPetalInspinHorizontal
    from app.patterns.FourPetalInspin import generate_FourPetalInspin
    from app.patterns.TriquetraBox import generate_TriquetraBox
    from app.patterns.FivePetalAntispinBox import generate_FivePetalAntispinBox
    from app.patterns.EightPetalInspin import generate_EightPetalInspin
    from app.patterns.TenPetalInspin import generate_TenPetalInspin
    
    config.pixel_height = 1200
    config.pixel_width = 1200
    config.frame_height = 4.0
    config.frame_width = 4.0
    config.background_color = "#222222"
    config.disable_caching = True  # Disable Manim cache to force fresh render

    pattern_map = {
        "Extension": generate_Extension,
        "12 Petal Antispin (Gunslinger)": generate_TwelvePetalAnti,
        "10 Petal Antispin (Gunslinger)": generate_TenPetalAnti,
        "8 Petal Inspin (Gunslinger)": generate_EightPetalInspin,
        "10 Petal Inspin (Gunslinger)": generate_TenPetalInspin,
        "Horizontal Cateye": generate_HorizontalCateye,
        "Vertical Cateye": generate_CatEye,
        "4 Petal Antispin": generate_FourPetalAnti,
        "5 Petal Antispin": generate_FivePetalAntispin,
        "5 Petal Antispin (Box)": generate_FivePetalAntispinBox,
        "4 Petal Antispin (Box)": generate_FourPetalAntiBox,
        "Static Spin": generate_StaticSpin,
        "Pendulum": generate_Pendulum,
        "Extended Pendulum": generate_ExtendedPendulum,
        "3 Petal Antispin (Triquetra)": generate_Triquetra,
        "3 Petal Antispin (Box Triquetra)": generate_TriquetraBox,
        "5 Petal Antispin (Box)": generate_FivePetalAntispinBox,
        "Isolation": generate_Isolation,
        "Isolated Pendulum": generate_IsolatedPendulum,
        "2 Petal Inspin (Vertical)": generate_TwoPetalInspin,
        "2 Petal Inspin (Horizontal)": generate_TwoPetalInspinHorizontal,
        "4 Petal Inspin": generate_FourPetalInspin,
    }

    left_func = pattern_map.get(left_pattern, generate_HorizontalCateye)
    right_func = pattern_map.get(right_pattern, generate_HorizontalCateye)

    from app.patterns.constants import ARM_LENGTH, POI_LENGTH, NUM_POINTS
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
    left_x, left_y, left_handle_x, left_handle_y = left_func(**left_call_args)
    right_x, right_y, right_handle_x, right_handle_y = right_func(**right_call_args)

    axis_label = ""
    # Determine scene title based on visible poi
    if (not show_left_head and not show_left_handle) and (show_right_head or show_right_handle):
        scene_title = f"{right_pattern}"
    elif (not show_right_head and not show_right_handle) and (show_left_head or show_left_handle):
        scene_title = f"{left_pattern}"
    elif (not show_left_head and not show_left_handle) and (not show_right_head and not show_right_handle):
        scene_title = ""
    else:
        scene_title = f"{left_pattern} vs {right_pattern}"

    class CombinedPatternScene(Scene):
        def construct(self):
            # Dynamically size title to fit frame width
            max_title_width = config.frame_width * 0.9
            base_font_size = 24
            min_font_size = 14
            est_font_size = max(min_font_size, min(base_font_size, int(base_font_size * max_title_width / (len(scene_title) + 8))))
            title = Text(scene_title, font_size=est_font_size).to_edge(UP, buff=0.04)
            label = Text(axis_label, font_size=18).to_edge(DOWN)
            self.add(title, label)
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
            def make_string(dot_handle, dot_head):
                if dot_handle and dot_head:
                    line = Line(dot_handle.get_center(), dot_head.get_center(), color="#FFFFFF", stroke_width=1.5)
                    def updater(mob):
                        mob.put_start_and_end_on(dot_handle.get_center(), dot_head.get_center())
                    line.add_updater(updater)
                    self.add(line)
            make_string(left_dot_handle, left_dot_head)
            make_string(right_dot_handle, right_dot_head)
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
    import moviepy as mpy
    try:
        scene_title = last_scene_title
    except Exception:
        scene_title = "combined_pattern"
    # Sanitize filename
    safe_title = scene_title.replace(" ", "_").replace("/", "-").replace("\\", "-")
    gif_path = os.path.join(os.getcwd(), f"{safe_title}.gif")
    clip = mpy.VideoFileClip(last_video_path)
    clip.write_gif(gif_path, fps=24)
    return gif_path
