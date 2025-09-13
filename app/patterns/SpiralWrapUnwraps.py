import numpy as np

def generate_SpiralWrapUnwraps(
    arm_length, poi_length, num_points, start_side='left', rotation_direction='clockwise'
):
    # Spiral parameters
    turns = 1.5  # Number of spiral wraps
    start_radius = poi_length
    end_radius = 0.1 * poi_length
    start_position = {'left': np.pi, 'right': 0}
    start_theta = start_position.get(start_side, np.pi)
    rotation_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    rotation_dir = rotation_multiplier.get(rotation_direction, -1)
    # Forward spiral (wrap)
    radii_fwd = np.linspace(start_radius, end_radius, num_points)
    angles_fwd = np.linspace(0, rotation_dir * 2 * np.pi * turns, num_points)
    # Backward spiral (unwrap)
    radii_bwd = np.linspace(end_radius, start_radius, num_points)
    angles_bwd = np.linspace(rotation_dir * 2 * np.pi * turns, 0, num_points)
    # Concatenate
    radii = np.concatenate([radii_fwd, radii_bwd])
    angles = np.concatenate([angles_fwd, angles_bwd])
    total_frames = 2 * num_points
    # Rotation matrix for head and handle
    cos_t = np.cos(start_theta)
    sin_t = np.sin(start_theta)
    def rotate(x, y):
        return x * cos_t - y * sin_t, x * sin_t + y * cos_t
    # Handle is at origin before rotation
    handle_x = np.zeros(total_frames)
    handle_y = np.zeros(total_frames)
    # Head positions
    head_x = radii * np.cos(angles)
    head_y = radii * np.sin(angles)
    head_x_rot, head_y_rot = rotate(head_x, head_y)
    # Handle is at origin
    # String bends and bunches: interpolate points along the spiral from handle to head
    string_points = []
    for i in range(total_frames):
        n_bends = 20
        bends = []
        for j in range(n_bends + 1):
            frac = j / n_bends
            r = frac * radii[i]
            a = frac * angles[i]
            bx = r * np.cos(a)
            by = r * np.sin(a)
            bx_rot, by_rot = rotate(bx, by)
            bends.append([bx_rot, by_rot])
        string_points.append(bends)
    return head_x_rot, head_y_rot, handle_x, handle_y, string_points
