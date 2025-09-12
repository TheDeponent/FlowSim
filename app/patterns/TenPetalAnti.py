import numpy as np

def generate_TenPetalAnti(
    arm_length, poi_length, num_points, start_side='left', rotation_direction='clockwise'
):
    petals = 8
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_direction_multiplier = rotation_multiplier.get(rotation_direction, -1)

    theta_1 = np.linspace(start_theta, start_theta + rotation_direction_multiplier * 2 * np.pi, num_points)
    theta_2 = np.linspace(0, rotation_direction_multiplier * -petals * np.pi, num_points)

    rotation_center_x = arm_length * np.cos(theta_1)
    rotation_center_y = arm_length * np.sin(theta_1)
    poi_head_x = rotation_center_x + (poi_length / 2) * np.cos(theta_2 + np.pi/2)
    poi_head_y = rotation_center_y + (poi_length / 2) * np.sin(theta_2 + np.pi/2)
    poi_handle_x = rotation_center_x - (poi_length / 2) * np.cos(theta_2 + np.pi/2)
    poi_handle_y = rotation_center_y - (poi_length / 2) * np.sin(theta_2 + np.pi/2)

    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
