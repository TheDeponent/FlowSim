import numpy as np
from app.patterns.constants import POI_LENGTH, NUM_POINTS, ARM_LENGTH

def generate_OnePetalInspinVertical(arm_length=ARM_LENGTH, poi_length=POI_LENGTH, num_points=NUM_POINTS, start_side='left', rotation_direction='clockwise'):
    # Parameters
    # Always start with poi at left or right, but rotate pattern for vertical
    if start_side == 'left':
        start_theta = np.pi
        offset = 0
    else:
        start_theta = 0
        offset = np.pi / 2  # 90 degrees offset for right start
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_direction_multiplier = rotation_multiplier.get(rotation_direction, -1)
    theta_1 = np.linspace(start_theta, start_theta + rotation_direction_multiplier * 2 * np.pi, num_points) + offset
    theta_2 = 2 * theta_1  # 1 petal inspin
    # Center of rotation (arm)
    rotation_center_x = poi_length * np.cos(theta_1)
    rotation_center_y = poi_length * np.sin(theta_1)
    # Head: inspin petals, radius = poi_length
    petal_radius = poi_length
    poi_head_x = rotation_center_x + petal_radius * np.cos(theta_2)
    poi_head_y = rotation_center_y + petal_radius * np.sin(theta_2)
    # Handle: always at center of rotation
    poi_handle_x = rotation_center_x
    poi_handle_y = rotation_center_y
    # Rotate 90 degrees to make pattern vertical (up/down)
    poi_head_x, poi_head_y = poi_head_y, -poi_head_x
    poi_handle_x, poi_handle_y = poi_handle_y, -poi_handle_x
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
