import numpy as np
from app.patterns.constants import ARM_LENGTH, POI_LENGTH, NUM_POINTS

def generate_HorizontalCateye(arm_length=ARM_LENGTH, poi_length=POI_LENGTH, num_points=NUM_POINTS, start_side='left', rotation_direction='clockwise'):
    # Parameters
    handle_radius = poi_length / 2
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position[start_side]
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_direction_multiplier = rotation_multiplier[rotation_direction]
    theta = np.linspace(start_theta, start_theta + rotation_direction_multiplier * 2 * np.pi, num_points)
    # Handle: perfect circle
    poi_handle_x = handle_radius * np.cos(theta)
    poi_handle_y = handle_radius * np.sin(theta)
    # Head: ellipse
    # Horizontal extent: arm_length / 2 + poi_length (major axis)
    # Vertical extent: arm_length / 2 (minor axis)
    ellipse_a = (poi_length / 2 + arm_length)  # major axis horizontal
    ellipse_b = poi_length / 2  # minor axis vertical
    # Offset ellipse so head starts at same apex as handle
    # Reverse spin direction for head, and align phase
    # At t=0, handle and head both at max horizontal position
    theta_head = -theta  # Reverse direction, no extra offset
    poi_head_x = ellipse_a * np.cos(theta_head)
    poi_head_y = ellipse_b * np.sin(theta_head)
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
