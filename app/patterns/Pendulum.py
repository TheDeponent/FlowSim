import numpy as np
from app.patterns.constants import ARM_LENGTH, POI_LENGTH, NUM_POINTS

def generate_Pendulum(start_side='left', rotation_direction='clockwise'):
    # Parameters
    armspan_meters = ARM_LENGTH
    radius = POI_LENGTH
    num_frames = NUM_POINTS

    # Set start position
    start_position = {'right': -np.pi / 2, 'left': np.pi / 2}
    start_theta = start_position[start_side]

    # Set swing direction
    swing_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    swing_direction_multiplier = swing_multiplier[rotation_direction]

    # Calculate time for pendulum motion
    time = np.linspace(0, num_frames / 30, num_frames)

    # Calculate angles for pendulum motion
    period = num_frames / 30
    omega = 2 * np.pi / period
    amplitude = start_theta
    theta_head = np.pi / 2 + amplitude * np.cos(omega * time * swing_direction_multiplier)

    # Head coordinates
    poi_head_x = radius * np.cos(theta_head)
    poi_head_y = -radius * np.sin(theta_head)

    # Handle fixed at center
    poi_handle_x = np.zeros_like(poi_head_x)
    poi_handle_y = np.zeros_like(poi_head_y)

    # Return coordinates for renderer (arrays only)
    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
