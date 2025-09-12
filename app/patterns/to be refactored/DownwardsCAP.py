import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D


def generate_CAP(fig, ax, head_color, handle_color, start_side='left', rotation_direction='clockwise'):
    # Parameters
    num_frames = 360
    armspan_inches = 5 * 12 + 9  # 5'9" in inches
    armspan_meters = armspan_inches * 0.0254  # Convert to meters
    tether_length = 0.45  # poi tether length in meters
    max_length = armspan_meters / 2  # maximum length of the pendulum
    trail_length = num_frames  # Length of the trail in frames

    # Set start position
    start_position = {'right': -np.pi / 2, 'left': np.pi / 2}
    start_theta = start_position[start_side]

    # Set swing direction
    swing_multiplier = {'clockwise': -1, 'anticlockwise': 1}
    swing_direction_multiplier = swing_multiplier[rotation_direction]

    # Calculate time for pendulum motion
    time = np.linspace(0, num_frames / 30, num_frames)  # Assuming 30 frames per second

    # Calculate angles for pendulum motion
    period = num_frames / 30  # The period is equal to the total duration of the animation
    omega = 2 * np.pi / period  # angular velocity adjusted to complete one oscillation during the animation

    # Calculate angles for handle (match the path of the head in generate_Pendulum)
    amplitude = start_theta
    theta_handle = np.pi / 2 + amplitude * np.cos(omega * time * swing_direction_multiplier)  # handle angle

    # Calculate coordinates for handle
    poi_handle_x = max_length * np.cos(theta_handle)
    poi_handle_y = -max_length * np.sin(theta_handle)  # Ensure poi handle stays at or below center level

    # Calculate coordinates for head
    theta_1 = np.linspace(start_theta, start_theta - 2 * (swing_direction_multiplier * np.pi), num_frames)
    theta_2 = -2 * theta_1 + (np.pi / 2) + -0.5 * np.sin(2 * omega * time * swing_direction_multiplier)
    poi_head_x = poi_handle_x + tether_length * np.cos(theta_2)
    poi_head_y = poi_handle_y - tether_length * np.sin(theta_2)

    # Set up the plot
    ax.set_xlim(-armspan_meters, armspan_meters)
    ax.set_ylim(-armspan_meters, armspan_meters)
    ax.set_aspect('equal', adjustable='box')
    title = "Downwards CAP"
    xlabel= "Head Leading"
    ax.set_xticks([])
    ax.set_yticks([])

    # Poi elements
    poi_head, = ax.plot([], [], 'go', markersize=10, alpha=1, color=head_color)
    poi_head_trail, = ax.plot([], [], linewidth=1.5, alpha=0.5, color=head_color)
    poi_handle, = ax.plot([], [], 'yo', markersize=10, alpha=1, color=handle_color)
    poi_handle_trail, = ax.plot([], [], linewidth=1.5, alpha=0.0, color=handle_color)
    poi_tether = Line2D([], [], color='k', linewidth=0.5)

    ax.add_line(poi_tether)

    # Initialize trails
    poi_head_trail_x = []
    poi_head_trail_y = []
    poi_handle_trail_x = []
    poi_handle_trail_y = []

    # Update function for the animation

    def update(frame):
        poi_head.set_data(poi_head_x[frame], poi_head_y[frame])
        poi_handle.set_data(poi_handle_x[frame], poi_handle_y[frame])

        poi_head_trail_x.append(poi_head_x[frame])
        poi_head_trail_y.append(poi_head_y[frame])
        poi_handle_trail_x.append(poi_handle_x[frame])
        poi_handle_trail_y.append(poi_handle_y[frame])

        if frame == 0:
            poi_head_trail_x.clear()
            poi_head_trail_y.clear()
            poi_handle_trail_x.clear()
            poi_handle_trail_y.clear()

        poi_head_trail.set_data(poi_head_trail_x[-trail_length:], poi_head_trail_y[-trail_length:])
        poi_handle_trail.set_data(poi_handle_trail_x[-trail_length:], poi_handle_trail_y[-trail_length:])

        poi_tether.set_data([poi_head_x[frame], poi_handle_x[frame]],
                            [poi_head_y[frame], poi_handle_y[frame]])

        return (poi_head, poi_head_trail, poi_handle, poi_handle_trail, poi_tether)

    # Create the animation
    ani = FuncAnimation(fig, update, frames=num_frames, interval=20, blit=True)

    return ax, update, (poi_head, poi_head_trail, poi_handle, poi_handle_trail, poi_tether), title, xlabel, start_side, rotation_direction
