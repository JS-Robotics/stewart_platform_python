from math import pi, sin, cos, sqrt
from quaternion_tools import quaternion_rotation, quaternion_to_euler
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

from stewart_platform_tools import platform_points_2d

# https://gamedev.stackexchange.com/questions/28395/rotating-vector3-by-a-quaternion
# https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion/535223 - Real good link


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlim3d(-100, 100)
ax.set_ylim3d(-100, 100)
ax.set_zlim3d(0, 15)
ax.view_init(elev=25, azim=100)
ax.set_xlabel('$X$', fontsize=10, rotation=0)
ax.set_ylabel('$Y$', fontsize=10, rotation=0)
ax.set_zlabel(r'$z$', fontsize=10, rotation=0)

l_s = 70
s_s = 30

l_f = 90
s_f = 40

x_p, y_p, z_p = platform_points_2d(l_s, s_s, height=12)
x_f, y_f, z_f = platform_points_2d(l_f, s_f, height=0, rotation_shift=60*pi/180)

line1, = ax.plot(x_p, y_p, z_p, color='red', marker='o', label='Quaternion rotation 90deg')
line2, = ax.plot(x_f, y_f, z_f, color='red', marker='o', label='Quaternion rotation 90deg')
line3, = ax.plot(0, 0, 12, color='blue', marker='o', label='Quaternion rotation 90deg')
ax.legend(handles=[line1, line2, line3])

plt.show()
