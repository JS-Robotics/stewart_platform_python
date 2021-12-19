# import numpy as np
from math import pi, sin, cos, sqrt
from quaternion_tools import quaternion_rotation, quaternion_to_euler
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# https://gamedev.stackexchange.com/questions/28395/rotating-vector3-by-a-quaternion
# https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion/535223 - Real good link


def eq_test(ss, sl):
    r_1 = (2*ss + sl)/sqrt(3) - sqrt(3)*ss/2
    r_2 = (2*sl + ss) /(2*sqrt(3))
    round(r_2, 4)
    round(r_1, 4)
    if r_2 == r_1:
        print("r_1 and r_2 are equal")
    print(round(r_1, 4), round(r_2, 4))


def distance_calc(ry, ss, counter):
    counter = counter + 1  # Function is 1 indexed in order to work with documentation
    gamma = 120 * pi / 180
    if counter % 2 == 0:
        print(f"counter = {counter} - applied gamma factor: {counter/2-1}")
        gamma = gamma * counter/2 - 1
    elif counter % 2 != 0:
        print(f"counter = {counter} - applied gamma factor: {(counter-1)/2}")
        gamma = gamma * (counter-1)/2

    x_dist = ry*cos(gamma) + ss * cos(gamma - (-1)**counter * pi/2)
    y_dist = ry*sin(gamma) + ss * sin(gamma - (-1)**counter * pi/2)
    return [x_dist, y_dist]


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlim3d(-100, 100)
ax.set_ylim3d(-100, 100)
ax.set_zlim3d(0, 3)
ax.view_init(elev=25, azim=100)
ax.set_xlabel('$X$', fontsize=10, rotation=0)
ax.set_ylabel('$Y$', fontsize=10, rotation=0)
ax.set_zlabel(r'$z$', fontsize=10, rotation=0)

r_g = 90
s_s = 30

a_1 = (6.78)*pi/180
a_2 = (-30)*pi/180

a_3 = 120*pi/180
a_4 = 120*pi/180

a_5 = (240 - 30)*pi/180
a_6 = (240 + 30)*pi/180

r = sqrt(r_g**2 + s_s**2)
print(r)

x_p = [0]*6
y_p = [0]*6
z_p = [0]*6
theta = 120/180*pi
for i in range(6):
    x_p[i], y_p[i] = distance_calc(r_g, s_s, i)
    # if i == 0 or i == 2 or i == 4:
    #     if i == 0:
    #         print(i)
    #         p_1_x = r_g*cos(theta*0) + s_s*cos(-90*pi/180)
    #         p_1_y = r_g * sin(theta * 0) + s_s * sin(-90 * pi / 180)
    #     if i == 2:
    #         print(i)
    #         p_1_x = r_g * cos(theta * 1) + s_s * cos(theta-90 * pi / 180)
    #         p_1_y = r_g * sin(theta * 1) + s_s * sin(theta-90 * pi / 180)
    #     if i == 4:
    #         print(i)
    #         p_1_x = r_g * cos(theta * 2) + s_s * cos(theta*2-90 * pi / 180)
    #         p_1_y = r_g * sin(theta * 2) + s_s * sin(theta*2-90 * pi / 180)
    # if i == 1 or i == 3 or i == 5:
    #     if i == 1:
    #         print(i)
    #         p_1_x = r_g*cos(theta*0) + s_s*cos(90*pi/180)
    #         p_1_y = r_g*sin(theta*0) + s_s*sin(90*pi/180)
    #     if i == 3:
    #         print(i)
    #         p_1_x = r_g * cos(theta * 1) + s_s * cos(theta +90 * pi / 180)
    #         p_1_y = r_g * sin(theta * 1) + s_s * sin(theta +90 * pi / 180)
    #     if i == 5:
    #         print(i)
    #         p_1_x = r_g * cos(theta * 2) + s_s * cos(theta*2 + 90 * pi / 180)
    #         p_1_y = r_g * sin(theta * 2) + s_s * sin(theta*2 + 90 * pi / 180)
    # x_p[i] = p_1_x
    # y_p[i] = p_1_y

    # x_p[i] = r_g*cos(theta*(i+1)) + s_s*cos(theta - (-1)**(i+1)*90*pi/180)
    # y_p[i] = r_g*sin(theta*(i+1)) + s_s*sin(theta - (-1)**(i+1)*90*pi/180)


x_p.append(x_p[0])
y_p.append(y_p[0])
z_p.append(z_p[0])
print(x_p)
print(y_p)
print(z_p)

p_1 = [r*cos(a_1), r*sin(a_1)]
p_1_a = [r_g*cos(0) + s_s*cos(90*pi/180), r_g*sin(0) + s_s*sin(90*pi/180)]



line1, = ax.plot(x_p, y_p, z_p, color='red', marker='o', label='Quaternion rotation 90deg')

ax.legend(handles=[line1])
plt.show()
