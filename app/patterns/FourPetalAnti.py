import numpy as np

def generate_FourPetalAnti(arm_length, poi_length, num_points, start_side='left', rotation_direction='clockwise'):
    petals = 6  # For 4 visible antispin petals
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_direction_multiplier = rotation_multiplier.get(rotation_direction, -1)

    theta_1 = np.linspace(start_theta, start_theta + rotation_direction_multiplier * 2 * np.pi, num_points)
    theta_2 = np.linspace(0, -rotation_direction_multiplier * petals * np.pi, num_points)

    # Handle does a single circle
    poi_handle_x = poi_length * np.cos(theta_1)
    poi_handle_y = poi_length * np.sin(theta_1)
    # Head creates antispin petals
    poi_head_x = poi_length * np.cos(theta_1) + arm_length * np.cos(theta_2)
    poi_head_y = poi_length * np.sin(theta_1) + arm_length * np.sin(theta_2)

    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
