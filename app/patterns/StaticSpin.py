import numpy as np
from app.patterns.constants import POI_LENGTH, NUM_POINTS, ARM_LENGTH

def generate_StaticSpin(arm_length=None, poi_length=POI_LENGTH, num_points=NUM_POINTS, start_side='left', rotation_direction='clockwise'):
    # Handle always at center
    poi_handle_x = np.zeros(num_points)
    poi_handle_y = np.zeros(num_points)
    # Head does a circle of radius ARM_LENGTH (to match pendulum)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    direction = rotation_multiplier.get(rotation_direction, -1)
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    theta = np.linspace(start_theta, start_theta + direction * 2 * np.pi, num_points)
    poi_head_x = POI_LENGTH * np.cos(theta)
    poi_head_y = POI_LENGTH * np.sin(theta)
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
