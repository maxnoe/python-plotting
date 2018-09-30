import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.special import jv, jn_zeros

RADIUS = 1
SPEED_OF_SOUND = 0.75
BESSEL_ROOTS = [jn_zeros(m, 10) for m in range(10)]
FPS = 25
TIME_PER_MODE = 10

MODES = (
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 2),
    (2, 3)
)

FRAMES = len(MODES) * TIME_PER_MODE * FPS


def lambda_mn(m, n, radius):
    return BESSEL_ROOTS[m][n - 1] / radius


def circular_membrane(r, theta, t, m, n, radius, speed_of_sound):
    l = lambda_mn(m, n, radius)

    T = np.sin(speed_of_sound * l * t)
    R = jv(m, l * r)
    Theta = np.cos(m * theta)

    return R * T * Theta


r = np.linspace(0, RADIUS, 100)
theta = np.linspace(0, 2 * np.pi, 100)

r, theta = np.meshgrid(r, theta)
x = np.cos(theta) * r
y = np.sin(theta) * r

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.set_axis_off()


def update(i):
    print(f'{i / FRAMES:.2%}', end='\r')
    t = i / FPS
    m, n = MODES[int(t // TIME_PER_MODE)]

    ax.cla()
    ax.set_axis_off()
    z = circular_membrane(r, theta, t, m, n, RADIUS, SPEED_OF_SOUND)
    vmax = np.max(jv(m, np.linspace(0, BESSEL_ROOTS[m][n], 100)))
    ax.plot_surface(
        x,
        y,
        z,
        linewidth=0,
        cmap='Spectral',
        vmin=-vmax,
        vmax=vmax,
        rcount=100,
        ccount=100,
    )
    ax.set_zlim(-1.1, 1.1)
    ax.set_xlim(-0.75, 0.75)
    ax.set_ylim(-0.75, 0.75)
    omega = SPEED_OF_SOUND * lambda_mn(m, n, RADIUS)
    ax.set_title(
        f'Circular membrane, m = {m}, n = {n}, ω={omega:.2f}',
        size=36, weight='bold', family='Fira Sans',
    )


ani = FuncAnimation(fig, update, frames=FRAMES, interval=1000/FPS, repeat=False)
ani.save(f'membrane.mp4', writer='ffmpeg')
