import numpy as np

def generate_TriquetraVsExtensionGunslinger(
    arm_length, poi_length, num_points, start_side='left', rotation_direction='clockwise'
):
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_dir = rotation_multiplier.get(rotation_direction, -1)
    theta = np.linspace(start_theta, start_theta + rotation_dir * 2 * np.pi, num_points)

    # Midpoint starts at arm_length
    mid_x = arm_length * np.cos(theta)
    mid_y = arm_length * np.sin(theta)
    handle_radius = poi_length / 2
    head_radius = poi_length / 2
    handle_x = mid_x + handle_radius * np.cos(theta)
    handle_y = mid_y + handle_radius * np.sin(theta)
    normalized_excursion = (theta - start_theta)
    phi = (-2 * normalized_excursion) - (np.pi / 2)
    head_x = mid_x + head_radius * np.cos(phi)
    head_y = mid_y + head_radius * np.sin(phi)
    string_points = [ [ [mx, my] ] for mx, my in zip(mid_x, mid_y) ]
    return np.array(head_x), np.array(head_y), np.array(handle_x), np.array(handle_y), string_points