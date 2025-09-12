import numpy as np
from app.patterns.constants import ARM_LENGTH, POI_LENGTH, NUM_POINTS

def generate_CatEye(arm_length=ARM_LENGTH, poi_length=POI_LENGTH, num_points=NUM_POINTS, start_side='left', rotation_direction='clockwise'):
    # Parameters
    handle_radius = poi_length / 2  # diameter = arm length
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position[start_side]
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_direction_multiplier = rotation_multiplier[rotation_direction]
    theta = np.linspace(start_theta, start_theta + rotation_direction_multiplier * 2 * np.pi, num_points)
    # Handle: perfect circle
    poi_handle_x = handle_radius * np.cos(theta)
    poi_handle_y = handle_radius * np.sin(theta)
    # Head: ellipse
    # Vertical extent: arm_length + poi_length
    # Horizontal extent: arm_length
    ellipse_a = poi_length / 2
    ellipse_b = (poi_length / 2 + arm_length)
    # Offset ellipse so head is always poi_length away from handle at opposite angle
    # Reverse spin direction for head
    theta_head = -theta + np.pi  # Opposite angle and reversed direction
    poi_head_x = ellipse_a * np.cos(theta_head)
    poi_head_y = ellipse_b * np.sin(theta_head)
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
