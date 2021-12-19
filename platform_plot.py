# import numpy as np
from math import pi, sin, cos, sqrt
from quaternion_tools import quaternion_rotation, quaternion_to_euler
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# https://gamedev.stackexchange.com/questions/28395/rotating-vector3-by-a-quaternion
# https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion/535223 - Real good link


def distance_calc(ry, ss, h: float = 0,  shift: float = 0, debug: bool = False):
    counter = 1  # Function is 1 indexed in order to work with documentation
    ss = ss / 2  # Getting half the length of ss, explained in documentation
    gamma = 120 * pi / 180
    applied_gamma = gamma
    edges = 6
    x_point = [0]*edges
    y_point = [0]*edges
    z_point = [h]*edges
    for edge in range(edges):  # The platform has 6 corners
        if counter % 2 == 0:
            applied_gamma = gamma * (counter/2 - 1)
            if debug:
                print(f"counter par = {counter} - applied gamma factor: {counter / 2 - 1}, "
                      f"applied gamma = {applied_gamma}, sign: {(-1)**edge}")
        elif counter % 2 != 0:
            applied_gamma = gamma * ((counter - 1)/2)
            if debug:
                print(f"counter odd = {counter} - applied gamma factor: {(counter - 1) / 2}, "
                      f"applied gamma = {applied_gamma}, sign: {(-1)**edge}")
        x_point[edge] = ry*cos(applied_gamma + shift) + ss * cos(applied_gamma + (-1)**counter * pi/2 + shift)
        y_point[edge] = ry*sin(applied_gamma + shift) + ss * sin(applied_gamma + (-1)**counter * pi/2 + shift)
        counter = counter + 1
    x_point.append(x_point[0])
    y_point.append(y_point[0])
    z_point.append(z_point[0])
    return [x_point, y_point, z_point]


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlim3d(-100, 100)
ax.set_ylim3d(-100, 100)
ax.set_zlim3d(0, 15)
ax.view_init(elev=25, azim=100)
ax.set_xlabel('$X$', fontsize=10, rotation=0)
ax.set_ylabel('$Y$', fontsize=10, rotation=0)
ax.set_zlabel(r'$z$', fontsize=10, rotation=0)

r_g = 70
s_s = 25

r_f = 90
s_f = 30

x_p, y_p, z_p = distance_calc(r_g, s_s, h=12)
x_f, y_f, z_f = distance_calc(r_f, s_f, shift=60*pi/180)

# print(x_p)
# print(y_p)
# print(z_p)
# print("-----------")
# print(x_f)
# print(y_f)
# print(z_f)


line1, = ax.plot(x_p, y_p, z_p, color='red', marker='o', label='Quaternion rotation 90deg')
line2, = ax.plot(x_f, y_f, z_f, color='red', marker='o', label='Quaternion rotation 90deg')
line3, = ax.plot(0, 0, 12, color='blue', marker='o', label='Quaternion rotation 90deg')
ax.legend(handles=[line1, line2, line3])

plt.show()
