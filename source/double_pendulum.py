import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import g
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba


def pendulum_model(t, y):
    """
    The right-hand side of the pendulum ODE
    """
    theta_1, theta_2, p_1, p_2 = y[0], y[1], y[2], y[3]

    f1 = 6.0 / (m * L**2)

    dcos = np.cos(theta_1 - theta_2)
    dsin = np.sin(theta_1 - theta_2)

    denominator = 16 - 9 * dcos**2

    dtheta_1 = f1 * (2 * p_1 - 3 * dcos * p_2) / denominator
    dtheta_2 = f1 * (8 * p_2 - 3 * dcos * p_1) / denominator

    f2 = -0.5 * m * L**2
    dp_1 = f2 * ( dtheta_1 * dtheta_2 * dsin + 3 * (g / L) * np.sin(theta_1))
    dp_4 = f2 * (-dtheta_1 * dtheta_2 * dsin + (g / L) * np.sin(theta_2))

    return [dtheta_1, dtheta_2, dp_1, dp_4]


def coords(theta1, theta2, l1, l2):
    x1 = np.sin(theta1) * l1
    y1 = -np.cos(theta1) * l1

    x2 = x1 + np.sin(theta2) * l2
    y2 = y1 - np.cos(theta2) * l2
    return x1, y1, x2, y2


L = 0.5
m = 0.1
theta1_0 = np.pi / 3
theta2_0 = -np.pi / 4 + 0.1
p1_0 = 0
p2_0 = 0.1
t_start = 0
t_end = 60
FPS = 120
max_points = 2 * FPS
FRAMES = int((t_end - t_start - 10) * FPS) 

solution = solve_ivp(
    pendulum_model,
    (t_start, t_end),
    y0=[theta1_0, theta2_0, p1_0, p2_0],
    t_eval=np.linspace(t_start + 10, t_end, FRAMES),
    method='Radau',
    vectorized=True,
)

x1s, y1s, x2s, y2s = coords(solution.y[0], solution.y[1], L, L)

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()
ax.set_aspect(1)

# colored line segments
points1 = np.column_stack([x1s, y1s]).reshape(-1, 1, 2)
segments1 = np.concatenate([points1[:-1], points1[1:]], axis=1)
lc1 = LineCollection([], lw=7)
colors1 = np.array([to_rgba('C0') for i in range(max_points)])
colors1[:, 3] = np.linspace(0, 0.5, max_points)
lc1.set_color(colors1)
ax.add_collection(lc1)

points2 = np.column_stack([x2s, y2s]).reshape(-1, 1, 2)
segments2 = np.concatenate([points2[:-1], points2[1:]], axis=1)
lc2 = LineCollection([], lw=7)
colors2 = np.array([to_rgba('C1') for i in range(max_points)])
colors2[:, 3] = np.linspace(0, 0.5, max_points)
ax.add_collection(lc2)


m = 1.1 * max(np.abs(x1s).max(), np.abs(x2s).max())
ax.set_xlim(-m, m)
ax.set_ylim(
    1.1 * min(y1s.min(), y2s.min()),
    1.1 * max(y2s.max(), y1s.max())
)

x1, y1, x2, y2 = x1s[0], y1s[0], x2s[0], y2s[0]

upper_line, = ax.plot([0, x1], [0, y1], 'k-', lw=3)
lower_line, = ax.plot([x1, x2], [y1, y2], 'k-', lw=3)

upper_mass, = ax.plot(x1, y1, 'o', ms=30)
lower_mass, = ax.plot(x2, y2, 'o', ms=30)
ax.plot(0, 0, 'ko', ms=20, zorder=3)

def update(i):
    print(f'{i / FRAMES:.2%}', end='\r')
    x1, y1, x2, y2 = x1s[i], y1s[i], x2s[i], y2s[i]
    upper_line.set_data([0, x1], [0, y1])
    lower_line.set_data([x1, x2], [y1, y2])
    upper_mass.set_data(x1, y1)
    lower_mass.set_data(x2, y2)

    if i < max_points:
        lc1.set_segments(segments1[:i])
        lc2.set_segments(segments2[:i])
        lc1.set_color(colors1[max_points - i - 1:])
        lc2.set_color(colors2[max_points - i - 1:])
    else:
        lc1.set_segments(segments1[i - max_points:i])
        lc2.set_segments(segments2[i - max_points:i])
        lc1.set_color(colors1)
        lc2.set_color(colors2)


    return upper_line, lower_line, upper_mass, lower_mass, lc1, lc2


ani = FuncAnimation(fig, update, frames=FRAMES, interval=1000/FPS, repeat=False, blit=True)
ani.save(f'double_pendulum.mp4', writer='ffmpeg')