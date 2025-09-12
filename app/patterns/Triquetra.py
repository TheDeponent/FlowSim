import numpy as np

def generate_Triquetra(arm_length, poi_length, num_points, start_side='left', rotation_direction='clockwise'):

    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_dir = rotation_multiplier.get(rotation_direction, -1)
    theta_handle = np.linspace(start_theta, start_theta + rotation_dir * 2 * np.pi, num_points)
    poi_handle_x = arm_length * np.cos(theta_handle)
    poi_handle_y = arm_length * np.sin(theta_handle)
    normalized_handle_excursion = (theta_handle - start_theta) 
    phi = (-2 * normalized_handle_excursion) - (np.pi / 2)
    poi_head_x = poi_handle_x + poi_length * np.cos(phi)
    poi_head_y = poi_handle_y + poi_length * np.sin(phi)
    
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y

