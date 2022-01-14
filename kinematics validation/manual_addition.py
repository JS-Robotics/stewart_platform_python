from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D


from stochastic_waves.wave_generators import body_displacement
from kinematic_tools.euler_rotation import vector_3d_rotation


def platform_points_3d(p_i, t_t, roll_, pitch_, yaw_):  # Figure out how to improve this one

    p_i_rot = vector_3d_rotation([p_i[0], p_i[1], p_i[2]], roll_, pitch_, yaw_)
    q_i_x = t_t[0] + p_i_rot[0]
    q_i_y = t_t[1] + p_i_rot[1]
    q_i_z = t_t[2] + p_i_rot[2]

    return q_i_x, q_i_y, q_i_z


if __name__ == "__main__":

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('$X$', fontsize=10, rotation=0)
    ax.set_ylabel('$Y$', fontsize=10, rotation=0)
    ax.set_zlabel(r'$z$', fontsize=10, rotation=0)

    roll = 0
    pitch = 1.57075/2
    yaw = 0
    heave = 2
    a_1 = [0, 0, 1]
    a_1 = vector_3d_rotation(a_1, 1.57075/2, 0, 0)
    ax.plot3D([0, 0, a_1[0]], [0, 0, a_1[1]], [0, heave, a_1[2]+heave], marker='o', color='blue')
    a_1[0] = a_1[0] + 0
    a_1[1] = a_1[1] + 0
    a_1[2] = a_1[2] + heave
    ax.plot3D([0, a_1[0]], [0, a_1[1]], [0, a_1[2]], marker='o',  color='blue')

    a_2_shift = 0.25
    a_2 = [a_2_shift, 0, 2]
    a_2 = vector_3d_rotation(a_2, 1.57075 / 2, 0, 0)
    ax.plot3D([a_2_shift, a_2_shift, a_2[0]], [0, 0, a_2[1]], [0, heave, a_2[2]+heave], marker='o', color='purple')
    a_2[0] = a_2[0] + 0
    a_2[1] = a_2[1] + 0
    a_2[2] = a_2[2] + heave
    ax.plot3D([a_2_shift, a_2[0]], [0, a_2[1]], [0, a_2[2]], marker='o', color='purple')

    a_3_shift = 0.5
    a_3 = [a_3_shift, 0, 3]
    a_3 = vector_3d_rotation(a_3, 1.57075 / 2, 0, 0)
    ax.plot3D([a_3_shift, a_3_shift, a_3[0]], [0, 0, a_3[1]], [0, heave, a_3[2]+heave], marker='o', color='red')
    a_3[0] = a_3[0] + 0
    a_3[1] = a_3[1] + 0
    a_3[2] = a_3[2] + heave
    ax.plot3D([a_3_shift, a_3[0]], [0, a_3[1]], [0, a_3[2]], marker='o', color='red')

    plt.show()
