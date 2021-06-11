import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.special import jv, jn_zeros
from tqdm.auto import tqdm
from functools import lru_cache

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


@lru_cache()
def lambda_mn(m, n, radius):
    return BESSEL_ROOTS[m][n - 1] / radius


@lru_cache()
def get_vmin_vmax(m, n):
    vmax = np.max(jv(m, np.linspace(0, BESSEL_ROOTS[m][n], 100)))
    return -vmax, vmax


def circular_membrane(r, theta, t, m, n, radius, speed_of_sound):
    l = lambda_mn(m, n, radius)

    T = np.sin(speed_of_sound * l * t)
    R = jv(m, l * r)
    Theta = np.cos(m * theta)

    return R * T * Theta


r = np.linspace(0, RADIUS, 100)
theta = np.linspace(0, 2 * np.pi, 100)

m, n = MODES[0]
r, theta = np.meshgrid(r, theta)
x = np.cos(theta) * r
y = np.sin(theta) * r
z = circular_membrane(r, theta, 0, m, n, RADIUS, SPEED_OF_SOUND)
vmin, vmax = get_vmin_vmax(m, n)

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.set_axis_off()
plot = ax.plot_surface(
    x,
    y,
    z,
    linewidth=0,
    cmap='Spectral',
    vmin=vmin,
    vmax=vmax,
    rcount=100,
    ccount=100,
)

omega = SPEED_OF_SOUND * lambda_mn(m, n, RADIUS)
text = ax.text2D(
    0.5, 0.95,
    f'Circular membrane, m = {m}, n = {n}, ω={omega:.2f}',
    size=36, weight='bold', family='Fira Sans',
    va='top', ha='center',
    transform=ax.transAxes,
)


def init():
    pass


def update(i, bar=None):
    global plot

    if bar is not None:
        bar.update()

    t = i / FPS
    m, n = MODES[int(t // TIME_PER_MODE)]

    z = circular_membrane(r, theta, t, m, n, RADIUS, SPEED_OF_SOUND)

    vmin, vmax = get_vmin_vmax(m, n)
    plot.remove()
    plot = ax.plot_surface(
        x,
        y,
        z,
        linewidth=0,
        cmap='Spectral',
        vmin=vmin,
        vmax=vmax,
        rcount=100,
        ccount=100,
    )
    ax.set_zlim(-1.1, 1.1)
    ax.set_xlim(-0.75, 0.75)
    ax.set_ylim(-0.75, 0.75)
    omega = SPEED_OF_SOUND * lambda_mn(m, n, RADIUS)
    text.set_text(f'Circular membrane, m = {m}, n = {n}, ω={omega:.2f}')


bar = tqdm(total=FRAMES)
ani = FuncAnimation(fig, update, init_func=init, frames=FRAMES, interval=1000/FPS, repeat=False, fargs=(bar, ))
ani.save(
    f'membrane.mp4',
    writer='ffmpeg',
    extra_args=['-vcodec', 'libx264', '-preset', 'slower', "-pix_fmt", "yuv420p", "-crf", "24", "-threads", "0", "-bf", "0"]
)
