from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D


from stochastic_waves.wave_generators import body_displacement
from kinematic_tools.euler_rotation import vector_3d_rotation


def platform_points_3d(p_i, t_t, roll, pitch, yaw):  # Figure out how to improve this one

    p_i_rot = vector_3d_rotation([p_i[0], p_i[1], p_i[2]], roll, pitch, yaw)
    q_i_x = t_t[0] + p_i_rot[0]
    q_i_y = t_t[1] + p_i_rot[1]
    q_i_z = t_t[2] + p_i_rot[2]

    return q_i_x, q_i_y, q_i_z


Tp = 4
Hs = 8
wave_angle = 50
wave_frequencies = []
resolution = 300

if __name__ == "__main__":
    for n_step in range(resolution):
        wave_frequencies.append(2 * (n_step + 0.001) / resolution)

    heave, surge, sway, roll, pitch, yaw, t_time = body_displacement(wave_frequencies, Hs, Tp, wave_angle)

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

    data_7 = [7, -1.5, 0]
    data_70 = [70.0, -15.0,  0]
    data_702 = [700.0, -150.0,  0]
    data_700 = [70/2, -15.0/2, 0]
    data_7000 = [70/5, -15.0/5, 0]

    # data_7 = [7-surge[0], -1.5-sway[0], 0-heave[0]]
    # data_70 = [70.0-surge[0], -15.0-sway[0], 0-heave[0]]
    # data_702 = [700.0-surge[0], -150.0-sway[0], 0-heave[0]]
    # data_700 = [(70 / 2)-surge[0], (-15.0 / 2)-sway[0], 0-heave[0]]
    # data_7000 = [(70 / 5)-surge[0], (-15.0 / 5)-sway[0], 0-heave[0]]

    # plt.show()

    index = 0
    rot_7 = platform_points_3d(data_7, [surge[0], sway[0], heave[0]], 0, pitch[index], 0)
    rot_70 = platform_points_3d(data_70, [surge[0], sway[0], heave[0]], 0, pitch[index], 0)
    rot_702 = platform_points_3d(data_702, [surge[0], sway[0], heave[0]], 0, pitch[index], 0)
    rot_700 = platform_points_3d(data_700, [surge[0], sway[0], heave[0]], 0, pitch[index], 0)
    rot_7000 = platform_points_3d(data_7000, [surge[0], sway[0], heave[0]], 0, pitch[index], 0)

    print(rot_7)
    print(rot_70)
    print(rot_702)
    print(rot_700)
    print(rot_7000)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    set = 1

    if set ==0 :
        ax.plot3D([0, surge[0], rot_7[0]+surge[0]], [0,    sway[0], rot_7[1]+sway[0]], [0,    heave[0], rot_7[2]+heave[0]], marker='o',  color='red')
        ax.plot3D([0, surge[0], rot_70[0]+surge[0]], [0,   sway[0], rot_70[1]+sway[0]], [0,   heave[0], rot_70[2]+heave[0]], marker='o')
        ax.plot3D([0, surge[0], rot_700[0]+surge[0]], [0,  sway[0], rot_700[1]+sway[0]], [0,  heave[0], rot_700[2]+heave[0]], marker='o')
        ax.plot3D([0, surge[0], rot_7000[0]+surge[0]], [0, sway[0], rot_7000[1]+sway[0]], [0, heave[0], rot_7000[2]+heave[0]], marker='o')

    if set == 1:
        ax.plot3D([0, rot_7[0]], [0, rot_7[1]], [0, rot_7[2]], marker='o',  color='red')
        # ax.plot3D([0, rot_70[0]], [0, rot_70[1]], [0, rot_70[2]], marker='o')
        ax.plot3D([0, rot_700[0]], [0, rot_700[1]], [0, rot_700[2]], marker='o')
        ax.plot3D([0, rot_7000[0]], [0, rot_7000[1]], [0, rot_7000[2]], marker='o')
        ax.plot3D([0, rot_702[0]], [0, rot_702[1]], [0, rot_702[2]], marker='o')

    plt.show()
