import os
import moviepy as mpy
from manim_mobject_svg import VGroup

def export_gif(last_video_path, last_combine_args):
	if not last_combine_args:
		return None
	args = last_combine_args.copy()
	left_visible = args['show_left_head'] or args['show_left_handle']
	right_visible = args['show_right_head'] or args['show_right_handle']
	if left_visible and right_visible:
		safe_title = f"{args['left_pattern']}_vs_{args['right_pattern']}"
	elif left_visible:
		safe_title = f"{args['left_pattern']}"
	elif right_visible:
		safe_title = f"{args['right_pattern']}"
	else:
		safe_title = "flowsim_export"
	gif_dir = os.path.join(os.getcwd(), "GIFs")
	os.makedirs(gif_dir, exist_ok=True)
	gif_path = os.path.join(gif_dir, f"{safe_title}.gif")
	clip = mpy.VideoFileClip(last_video_path)
	clip.write_gif(gif_path, fps=24)
	clip.close()
	return gif_path

def export_svg(last_combine_args, get_final_frame_objects):
	if not last_combine_args:
		return None
	args = last_combine_args.copy()
	left_visible = args['show_left_head'] or args['show_left_handle']
	right_visible = args['show_right_head'] or args['show_right_handle']
	if left_visible and right_visible:
		safe_title = f"{args['left_pattern']}_vs_{args['right_pattern']}"
	elif left_visible:
		safe_title = f"{args['left_pattern']}"
	elif right_visible:
		safe_title = f"{args['right_pattern']}"
	else:
		safe_title = "flowsim_export"
	svg_dir = os.path.join(os.getcwd(), "SVGs")
	os.makedirs(svg_dir, exist_ok=True)
	svg_path = os.path.join(svg_dir, f"{safe_title}.svg")
	required_keys = [
		'left_x', 'left_y', 'left_handle_x', 'left_handle_y',
		'right_x', 'right_y', 'right_handle_x', 'right_handle_y',
		'left_head_color', 'left_handle_color', 'right_head_color', 'right_handle_color',
		'show_left_head', 'show_left_handle', 'show_right_head', 'show_right_handle',
		'show_left_path_only', 'show_right_path_only',
		'scene_title', 'axis_label', 'left_result', 'right_result'
	]
	missing = [k for k in required_keys if k not in args]
	if missing:
		return None
	objects = get_final_frame_objects(
		args['left_x'], args['left_y'], args['left_handle_x'], args['left_handle_y'],
		args['right_x'], args['right_y'], args['right_handle_x'], args['right_handle_y'],
		args['left_head_color'], args['left_handle_color'], args['right_head_color'], args['right_handle_color'],
		args['show_left_head'], args['show_left_handle'], args['show_right_head'], args['show_right_handle'],
		args['show_left_path_only'], args['show_right_path_only'],
		args['scene_title'], args['axis_label'],
		args['left_result'], args['right_result']
	)
	group = VGroup(*objects)
	svg_file = group.to_svg(svg_path)
	return str(svg_file)
