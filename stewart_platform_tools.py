from math import sin, cos, pi, sqrt
from kinematic_tools.quaternion_rotation import quaternion_rotation
from kinematic_tools.euler_rotation import vector_3d_rotation


def platform_points_2d(long_side: float, short_side: float, height: float = 0,
                       rotation_shift: float = 0, debug: bool = False):
    counter = 1  # Functions are 1 indexed in order to work with documentation
    short_side = short_side / 2  # Getting half the length of short_side, explained in documentation
    gamma = 120 * pi / 180  # The angle between each short-side
    edges = 6
    x_point = [0, 0, 0, 0, 0, 0]
    y_point = [0, 0, 0, 0, 0, 0]
    z_point = [height]*edges
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
        else:
            raise ValueError
        x_point[edge] = long_side*cos(applied_gamma + rotation_shift) + short_side * cos(applied_gamma + (-1)**counter * pi/2 + rotation_shift)
        y_point[edge] = long_side*sin(applied_gamma + rotation_shift) + short_side * sin(applied_gamma + (-1)**counter * pi/2 + rotation_shift)
        counter = counter + 1
    x_point.append(x_point[0])
    y_point.append(y_point[0])
    z_point.append(z_point[0])
    return [x_point, y_point, z_point]


def platform_points_3d(p_i, t_t, roll, pitch, yaw):
    q_i_x = [0, 0, 0, 0, 0, 0, 0]
    q_i_y = [0, 0, 0, 0, 0, 0, 0]
    q_i_z = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(q_i_x)-1):
        p_i_rot = vector_3d_rotation([p_i[0][i], p_i[1][i], p_i[2][i]], roll, pitch, yaw)
        q_i_x[i] = t_t[0] + p_i_rot[0]
        q_i_y[i] = t_t[1] + p_i_rot[1]
        q_i_z[i] = t_t[2] + p_i_rot[2]
    q_i_x[-1] = (q_i_x[0])
    q_i_y[-1] = (q_i_y[0])
    q_i_z[-1] = (q_i_z[0])
    return q_i_x, q_i_y, q_i_z


def cylinder_length_quat(t_s, p_k, b_k, theta) :
    # https://www.youtube.com/watch?v=5wCK6XGC3ig&t=253s
    theta = theta * pi / 180
    q_r = [cos(theta/2), 0, sin(theta/2), 0]
    p_k = quaternion_rotation(q_r, p_k)
    print(f"p_k_quat = {p_k}")
    i_k = [0, 0, 0]
    i_k[0] = t_s[0] + p_k[0] - b_k[0]
    i_k[1] = t_s[1] + p_k[1] - b_k[1]
    i_k[2] = t_s[2] + p_k[2] - b_k[2]

    # print(i_k)
    # print(f"Leg length = {sqrt(i_k[0]**2 + i_k[1]**2 + i_k[2]**2)}")


def cylinder_length_euler(t_s, p_k, b_k, theta):
    theta = theta * pi / 180

    p_k = vector_3d_rotation(p_k, gamma=0, beta=theta, alpha=0)
    print(f"p_k_euler = {p_k}")

    i_k = [0, 0, 0]
    # print(i_k)
    # print(f"Leg length = {sqrt(i_k[0] ** 2 + i_k[1] ** 2 + i_k[2] ** 2)}")


if __name__ == '__main__':
    print(f"Running stewart_platform_tools for debug")
    l_s = 70
    s_s = 30
    l_f = 90
    s_f = 40
    x_p, y_p, z_p = platform_points_2d(l_s, s_s, height=12)
    x_f, y_f, z_f = platform_points_2d(l_f, s_f, height=0, rotation_shift=60 * pi / 180)

    t_test = [0, 0, 10]
    ba_k = [x_f[0], y_f[0], z_f[0]]
    pa_k = [x_p[0], y_p[0], z_p[0]]
    print(ba_k)
    print(pa_k)
    rot = 45
    cylinder_length_quat(t_test, ba_k, pa_k, 30)
    cylinder_length_euler(t_test, ba_k, pa_k, 30)
