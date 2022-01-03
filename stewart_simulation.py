
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from stochastic_waves.wave_generators import irregular_surface_propagation, body_displacement
from stewart_platform_tools import platform_points_2d, platform_points_3d

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(projection='3d')
line, = ax.plot([], [], lw=2, marker='o')

leg1, = ax.plot([], [], lw=2, color='black')
leg2, = ax.plot([], [], lw=2, color='black')
leg3, = ax.plot([], [], lw=2, color='black')
leg4, = ax.plot([], [], lw=2, color='black')
leg5, = ax.plot([], [], lw=2, color='black')
leg6, = ax.plot([], [], lw=2, color='black')

# leg1, = ax.plot([], [], lw=2, marker='o', color='black')
# leg2, = ax.plot([], [], lw=2, marker='o', color='black')
# leg3, = ax.plot([], [], lw=2, marker='o', color='black')
# leg4, = ax.plot([], [], lw=2, marker='o', color='black')
# leg5, = ax.plot([], [], lw=2, marker='o', color='black')
# leg6, = ax.plot([], [], lw=2, marker='o', color='black')

start = 100
end = 100
ax.set_xlim3d(-end, start)
ax.set_ylim3d(-end, start)
ax.set_zlim3d(0, 15)
ax.view_init(elev=25, azim=100)
ax.set_xlabel('$X$', fontsize=10, rotation=0)
ax.set_ylabel('$Y$', fontsize=10, rotation=0)
ax.set_zlabel(r'$z$', fontsize=10, rotation=0)

l_s = 70
s_s = 30
l_f = 90
s_f = 40

x_f, y_f, z_f = platform_points_2d(l_f, s_f, height=0, rotation_shift=60*3.1415/180)
line2, = ax.plot(x_f, y_f, z_f, color='red', marker='o', label='Quaternion rotation 90deg')

frames_ = 900
resolution = frames_
Tp = 8
Hs = 4  # 4
wave_frequencies = []
for n_step in range(resolution):
    wave_frequencies.append(2 * (n_step + 0.001) / resolution)
# t_time, wave_surface = irregular_surface_propagation(wave_frequencies, Hs, Tp)
heave, surge, sway, roll, pitch, yaw, t_time = body_displacement(wave_frequencies, Hs, Tp, 50)
rot_scale = 1/100
pos_scale = 1/5

figs, (ax1, ax2) = plt.subplots(2)
line1 = ax1.plot(t_time, heave, label='heave [m]')
line2 = ax1.plot(t_time, surge, label='surge [m]')
line3 = ax1.plot(t_time, sway, label='sway [m]')
line4 = ax2.plot(t_time, roll, label='roll [rad]')
line5 = ax2.plot(t_time, pitch, label='pitch [rad]')
line6 = ax2.plot(t_time, yaw, label='yaw [rad]')
ax1.grid(color='black', linestyle='-', linewidth=0.5)
ax2.grid(color='black', linestyle='-', linewidth=0.5)
ax1.legend()
ax2.legend()


def animate(i):

    x_p, y_p, z_p = platform_points_2d(l_s, s_s, height=0, rotation_shift=0)
    # x_p, y_p, z_p = platform_points_3d([x_p, y_p, z_p], [wave_surface[i]*pos_scale, -wave_surface[i]*pos_scale,
    #                                                      wave_surface[i]+12], -wave_surface[i]*rot_scale/3,
    #                                                      wave_surface[i]*rot_scale/3, wave_surface[i]*rot_scale*5)

    x_p, y_p, z_p = platform_points_3d([x_p, y_p, z_p], [surge[i]/2, sway[i]/2, heave[i]/2 + 10], roll[i]/100, pitch[i]/100, yaw[i]/100)

    line.set_data(x_p, y_p)
    line.set_3d_properties(z_p)

    leg1.set_data([x_f[0], x_p[1]], [y_f[0], y_p[1]])
    leg1.set_3d_properties([z_f[0], z_p[1]])

    leg2.set_data([x_f[1], x_p[2]], [y_f[1], y_p[2]])
    leg2.set_3d_properties([z_f[1], z_p[2]])

    leg3.set_data([x_f[2], x_p[3]], [y_f[2], y_p[3]])
    leg3.set_3d_properties([z_f[2], z_p[3]])

    leg4.set_data([x_f[3], x_p[4]], [y_f[3], y_p[4]])
    leg4.set_3d_properties([z_f[3], z_p[4]])

    leg5.set_data([x_f[4], x_p[5]], [y_f[4], y_p[5]])
    leg5.set_3d_properties([z_f[4], z_p[5]])

    leg6.set_data([x_f[5], x_p[0]], [y_f[5], y_p[0]])
    leg6.set_3d_properties([z_f[5], z_p[0]])

    return line, leg1, leg2, leg3, leg4, leg5, leg6


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, frames=frames_, interval=20, blit=True)

# anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
