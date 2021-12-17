# import numpy as np
from math import pi, sin, cos
from quaternion_tools import quaternion_rotation, quaternion_to_euler
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# https://gamedev.stackexchange.com/questions/28395/rotating-vector3-by-a-quaternion
# https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion/535223 - Real good link


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlim3d(-3, 3)
ax.set_ylim3d(-3, 3)
ax.set_zlim3d(0, 3)
ax.view_init(elev=25, azim=100)
ax.set_xlabel('$X$', fontsize=10, rotation=0)
ax.set_ylabel('$Y$', fontsize=10, rotation=0)
ax.set_zlabel(r'$z$', fontsize=10, rotation=0)

length = 1
arm = 2
degree = 120
theta = degree/180*pi

x_pos = length*sin(theta)
z_pos = length*cos(theta)

x = [0, 0, x_pos]
y = [1, 1, 1]
z = [0, arm, arm-z_pos]
line1, = ax.plot(x, y, z, color='green', marker='o', label='Euler rotation 90deg')
print(x[-1])
x = length
y = 0
z = arm

q0 = cos(theta/2)
q1 = 0
q2 = sin(theta/2)
q3 = 0
q = [q0, q1, q2, q3]
q_conj = [q0, -q1, -q2, -q3]

p = [length, 0, 0]
qp = quaternion_rotation(q, p)

xq = [0, 0, qp[0]]
yq = [0, 0, qp[1]]
zq = [0, arm, arm-qp[2]]

print(f"p = [{xq[-1]}, {yq[-1]}, {zq[-1]}]")
print(f"q = [{round(q[0],4)}, {round(q[1],4)}, {round(q[2],4)}, {round(q[3],4)}]")
print(f"q' = [{round(q_conj[0],4)}, {round(q_conj[1],4)}, {round(q_conj[2],4)}, {round(q_conj[3],4)}]")

# Calculating the Hamilton product of the quaternions
print(f"Calculating: qpq' = {qp}")

line2, = ax.plot(xq, yq, zq, color='red', marker='o', label='Quaternion rotation 90deg')
line3, = ax.plot([0, 0, 0], [-1, -1, -1], [0, 2, 3], color='blue', marker='o', label='No-rotation')
ax.legend(handles=[line1, line2, line3])
plt.show()
