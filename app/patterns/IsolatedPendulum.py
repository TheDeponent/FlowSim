import numpy as np
from app.patterns.constants import ARM_LENGTH, POI_LENGTH, NUM_POINTS

def generate_IsolatedPendulum(start_side='left', rotation_direction='clockwise'):
    """
    Generates coordinates for the 'isolated pendulum' move.
    Combines a circular handle path with a pendulum motion for the head.
    """
    # Parameters
    arm_length = ARM_LENGTH
    poi_length = POI_LENGTH
    num_points = NUM_POINTS

    # --- 1. Handle Motion: Circle with diameter = poi_length ---
    start_position_handle = {'left': np.pi, 'right': 0}
    start_theta_handle = start_position_handle.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_dir = rotation_multiplier.get(rotation_direction, -1)
    theta_handle_circle = np.linspace(start_theta_handle, start_theta_handle + rotation_dir * 2 * np.pi, num_points)
    handle_radius = poi_length / 2
    poi_handle_x = handle_radius * np.cos(theta_handle_circle)
    poi_handle_y = handle_radius * np.sin(theta_handle_circle)

    # --- 2. Head Motion: Pendulum swing centered at origin ---
    start_position_pendulum = {'right': -np.pi / 2, 'left': np.pi / 2}
    start_theta_pendulum = start_position_pendulum.get(start_side, np.pi / 2)
    swing_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    swing_direction_multiplier = swing_multiplier.get(rotation_direction, -1)
    time = np.linspace(0, num_points / 30, num_points)  # Assuming 30 frames per second
    period = num_points / 30
    omega = 2 * np.pi / period
    amplitude = start_theta_pendulum
    theta_head = np.pi / 2 + amplitude * np.cos(omega * time * swing_direction_multiplier)
    # Head pendulum centered on moving handle, max radius = poi_length
    poi_head_x = poi_handle_x + poi_length * np.cos(theta_head)
    poi_head_y = poi_handle_y - poi_length * np.sin(theta_head)

    # --- 3. Return coordinates ---
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y

