import numpy as np
from app.patterns.constants import POI_LENGTH, NUM_POINTS

def generate_Isolation(POI_LENGTH=POI_LENGTH, num_points=NUM_POINTS, start_side='left', rotation_direction='clockwise'):
    # Both handle and head trace a circle of radius ARM_LENGTH
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    direction = rotation_multiplier.get(rotation_direction, -1)
    theta = np.linspace(0, direction * 2 * np.pi, num_points)
    # Both handle and head trace a circle of radius POI_LENGTH/2, always opposite
    radius = POI_LENGTH / 2
    # Use start_side to reverse initial position
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    theta = np.linspace(start_theta, start_theta + direction * 2 * np.pi, num_points)
    poi_handle_x = radius * np.cos(theta)
    poi_handle_y = radius * np.sin(theta)
    theta_head = theta + np.pi  # Always diametrically opposite
    poi_head_x = radius * np.cos(theta_head)
    poi_head_y = radius * np.sin(theta_head)
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
