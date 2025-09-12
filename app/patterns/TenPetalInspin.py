import numpy as np
from app.patterns.constants import POI_LENGTH, NUM_POINTS, ARM_LENGTH

def generate_TenPetalInspin(arm_length=ARM_LENGTH, poi_length=POI_LENGTH, num_points=NUM_POINTS, start_side='left', rotation_direction='clockwise'):
    # Parameters
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_direction_multiplier = rotation_multiplier.get(rotation_direction, -1)
    theta_1 = np.linspace(start_theta, start_theta + rotation_direction_multiplier * 2 * np.pi, num_points)
    # 10 petals: 6.25x frequency, no offset
    theta_2 = 6.25 * theta_1
    # Midpoint (center of rotation) traces arm circle
    midpoint_x = arm_length * np.cos(theta_1)
    midpoint_y = arm_length * np.sin(theta_1)
    # Head traces inspin petals around midpoint
    petal_radius = poi_length / 2
    poi_head_x = midpoint_x + petal_radius * np.cos(theta_2)
    poi_head_y = midpoint_y + petal_radius * np.sin(theta_2)
    # Handle is always poi_length away from head, on the opposite side of the midpoint
    dx = poi_head_x - midpoint_x
    dy = poi_head_y - midpoint_y
    poi_handle_x = midpoint_x - dx
    poi_handle_y = midpoint_y - dy
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
