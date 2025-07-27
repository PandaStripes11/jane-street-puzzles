import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = np.zeros((100,100))

def simulate_highway(density: float = 0.00000001, trip_length: float = 100000, road_length = 100000000, simulation_time: int = 1000):
    expected_num_cars = int(density*road_length*simulation_time)
    spawn_time = np.random.uniform(0, simulation_time, expected_num_cars)
    spawn_location = np.random.uniform(0, road_length, expected_num_cars)
    speeds = np.random.uniform(1, 2, expected_num_cars)

    exit_time = spawn_time + trip_length / speeds
    exit_location = spawn_location + trip_length

    sorted_indices = np.argsort(spawn_location)
    spawn_time = spawn_time[sorted_indices]
    spawn_location = spawn_location[sorted_indices]
    speeds = speeds[sorted_indices]
    exit_time = exit_time[sorted_indices]
    exit_location = exit_location[sorted_indices]

    for i in range(expected_num_cars):
        for j in range(i+1, expected_num_cars):
            # First car must be faster
            if speeds[i] <= speeds[j]:
                continue

            # Solve for time 't' when Y catches up to X
            # pos_X(t) = spawn_X + speed_X*(t - spawn_time_X)
            # pos_Y(t) = spawn_Y + speed_Y*(t - spawn_time_Y)
            # Solve: pos_X(t) == pos_Y(t)
            numerator = spawn_location[i] - spawn_location[j] - (speeds[i]*spawn_time[i]) + (speeds[j]*spawn_time[j])
            denominator = speeds[j]-speeds[i]
            pass_time = numerator/denominator

            if (pass_time < max(spawn_time[i], spawn_time[j])):
                continue
            if (pass_time > min(exit_time[i], exit_time[j])):
                continue
            
            row = math.floor((speeds[j]-1)*100)
            column = math.floor((speeds[i]-1)*100)

            data[row][column] = data[row][column] + 1
        print(i)
            
"""
def parse_events(events_array, size: int = 100):
    for pair in events_array:
        row = math.floor((pair[0]-1)*size)
        column = math.floor((pair[1]-1)*size)
        data[row][column] += 1
"""

simulation_time = eval(input("Enter a simulation time --> "))
simulate_highway(simulation_time=simulation_time)

# Get dimensions
x_bins, y_bins = data.shape
x_edges = np.linspace(1, 2, x_bins + 1)
y_edges = np.linspace(1, 2, y_bins + 1)

# Create mesh grid of bin positions
xpos, ypos = np.meshgrid(x_edges[:-1], y_edges[:-1], indexing='ij')
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = np.zeros_like(xpos)

# Bar dimensions
dx = dy = (x_edges[1] - x_edges[0])
dz = data.ravel()

# Plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, shade=True, color='royalblue')

# Labeling
ax.set_xlabel('X (slower car speed)')
ax.set_ylabel('Y (faster car speed)')
ax.set_zlabel('Pass count')
ax.set_title('3D Histogram from 2D Matrix')

ax.view_init(elev=30, azim=160)
ax.set_xlim(ax.get_xlim()[::-1])
ax.set_ylim(ax.get_ylim()[::-1])

plt.show()