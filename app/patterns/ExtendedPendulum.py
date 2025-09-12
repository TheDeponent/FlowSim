import numpy as np

def generate_ExtendedPendulum(
    arm_length, poi_length, num_points, start_side='left', rotation_direction='clockwise'
):
    # Parameters
    max_length = arm_length
    start_position = {'right': -np.pi / 2, 'left': np.pi / 2}
    start_theta = start_position.get(start_side, np.pi / 2)
    swing_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    swing_direction_multiplier = swing_multiplier.get(rotation_direction, -1)

    time = np.linspace(0, num_points / 30, num_points)  # Assuming 30 frames per second
    period = num_points / 30
    omega = 2 * np.pi / period
    amplitude = start_theta

    theta_handle = np.pi / 2 + amplitude * np.cos(omega * time * swing_direction_multiplier)
    theta_head = np.pi / 2 + amplitude * np.cos(omega * time * swing_direction_multiplier)

    poi_handle_x = max_length * np.cos(theta_handle)
    poi_handle_y = -max_length * np.sin(theta_handle)
    poi_head_x = poi_handle_x + poi_length * np.cos(theta_head)
    poi_head_y = poi_handle_y - poi_length * np.sin(theta_head)

    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
