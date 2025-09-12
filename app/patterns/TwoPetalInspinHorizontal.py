import numpy as np
from app.patterns.constants import POI_LENGTH, NUM_POINTS, ARM_LENGTH

def generate_TwoPetalInspinHorizontal(arm_length=ARM_LENGTH, poi_length=POI_LENGTH, num_points=NUM_POINTS, start_side='left', rotation_direction='clockwise'):
    # Parameters
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_direction_multiplier = rotation_multiplier.get(rotation_direction, -1)
    theta_1 = np.linspace(start_theta, start_theta + rotation_direction_multiplier * 2 * np.pi, num_points)
    # Offset so poi head starts directly down from handle
    theta_2 = 3 * theta_1 - np.pi  # 2 petals: 3x frequency, offset by -pi/2
    # Center of rotation (arm)
    rotation_center_x = arm_length * np.cos(theta_1)
    rotation_center_y = arm_length * np.sin(theta_1)
    # Head: inspin petals, radius = arm_length/2
    petal_radius = poi_length
    poi_head_x = rotation_center_x + petal_radius * np.cos(theta_2)
    poi_head_y = rotation_center_y + petal_radius * np.sin(theta_2)
    # Handle: always at center of rotation
    poi_handle_x = rotation_center_x
    poi_handle_y = rotation_center_y
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
