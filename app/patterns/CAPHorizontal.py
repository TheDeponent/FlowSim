import numpy as np

def generate_CAPHorizontal(arm_length, poi_length, num_points, start_side='right', rotation_direction='clockwise'):
    """
    CAP (Horizontal): Generates a horizontal pattern.
    'right' starts on the right, 'left' mirrors it to the left.
    """
    spin = 1  # 1 for inspin, -1 for antispin
    direction = 1 if rotation_direction == 'clockwise' else -1
    beats = 4
    points_per_beat = num_points // beats
    orient = 0

    # Set the start offset based on the start_side parameter.
    if start_side == 'left':
        start_offset_fraction = 0.25
    else:  # 'right'
        start_offset_fraction = 0.75

    # Angular velocities (slowed by half)
    hand_va = [0.5*spin*direction, -0.5*spin*direction, -0.5*spin*direction, 0.5*spin*direction]
    head_va = [0.5*spin*direction, 1.5*spin*direction, 1.5*spin*direction, 0.5*spin*direction]

    # Offset Logic
    offset_beats = int(start_offset_fraction * beats)
    if offset_beats > 0:
        hand_va = np.roll(hand_va, -offset_beats)
        head_va = np.roll(head_va, -offset_beats)

    # Segment starting angles
    hand_angles = [orient]
    head_angles = [orient]
    for i in range(beats):
        hand_angles.append(hand_angles[-1] + hand_va[i] * np.pi)
        head_angles.append(head_angles[-1] + head_va[i] * np.pi)

    # Build segments
    poi_handle_x = []
    poi_handle_y = []
    poi_head_x = []
    poi_head_y = []
    for i in range(beats):
        t = np.linspace(0, 1, points_per_beat, endpoint=False)
        hand_theta = hand_angles[i] + hand_va[i] * np.pi * t
        head_theta = head_angles[i] + head_va[i] * np.pi * t
        hx = arm_length * np.cos(hand_theta)
        hy = arm_length * np.sin(hand_theta)
        px = hx + poi_length * np.cos(head_theta)
        py = hy + poi_length * np.sin(head_theta)
        # MODIFICATION: Removed rotation to make the pattern horizontal
        poi_handle_x.append(hx)
        poi_handle_y.append(hy)
        poi_head_x.append(px)
        poi_head_y.append(py)

    # Concatenate segments
    poi_handle_x = np.concatenate(poi_handle_x)
    poi_handle_y = np.concatenate(poi_handle_y)
    poi_head_x = np.concatenate(poi_head_x)
    poi_head_y = np.concatenate(poi_head_y)

    # MODIFICATION: Horizontal flip for 'left' side
    if start_side == 'left':
        poi_handle_x *= -1
        poi_head_x *= -1

    return poi_head_x, poi_head_y, poi_handle_x, poi_handle_y
