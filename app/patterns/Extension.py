import numpy as np

def generate_Extension(
    arm_length, poi_length, num_points, start_side='left', rotation_direction='clockwise'
):
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_direction_multiplier = rotation_multiplier.get(rotation_direction, -1)

    theta_1 = np.linspace(start_theta, start_theta + rotation_direction_multiplier * 2 * np.pi, num_points)

    # Handle moves in a circle of radius arm_length
    poi_handle_x = poi_length * np.cos(theta_1)
    poi_handle_y = poi_length * np.sin(theta_1)
    # Head moves in a circle of radius arm_length + poi_length
    poi_head_x = (arm_length + poi_length) * np.cos(theta_1)
    poi_head_y = (arm_length + poi_length) * np.sin(theta_1)

    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
