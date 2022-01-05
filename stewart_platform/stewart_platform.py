from math import pi, sin, cos

from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

from stochastic_waves.wave_generators import body_displacement
from kinematic_tools.euler_rotation import vector_3d_rotation


class StewartPlatform:
    def __init__(self, fixed_long, fixed_short, dynamic_long, dynamic_short, T_p, H_s, wave_angle, home_height=2,
                 fixed_rotation_shift=(60*3.1415/180), dynamic_rotation_shift=0):

        self._fixed_platform_color = 'red'
        self._dynamic_platform_color = 'blue'

        self._fixed_platform_points = self._generate_platform_points(long_side=fixed_long,
                                                                     short_side=fixed_short,
                                                                     height=0,
                                                                     rotation_shift=fixed_rotation_shift,
                                                                     debug=False)

        self._dynamic_platform_points = self._generate_platform_points(long_side=dynamic_long,
                                                                       short_side=dynamic_short,
                                                                       height=0,
                                                                       rotation_shift=dynamic_rotation_shift,
                                                                       debug=False)
        self._rotation_correction_factor = dynamic_long
        self._wave_angle = wave_angle
        self._home_height = home_height
        self._significant_wave_height = H_s
        self._wave_period = T_p
        scaling = 0.225
        if fixed_long > dynamic_long:
            self._plot_limits = self._round_up(fixed_long + scaling*fixed_long)
        else:
            self._plot_limits = self._round_up(dynamic_long + scaling*dynamic_long)
        self._plot_height = self._round_up(home_height + (scaling+0.025)*home_height)

    @staticmethod
    def _generate_platform_points(long_side: float, short_side: float, height: float = 0,
                                  rotation_shift: float = 0, debug: bool = False):

        counter = 1  # Functions are 1 indexed in order to work with documentation
        short_side = short_side / 2  # Getting half the length of short_side, explained in documentation
        gamma = 120 * pi / 180  # The angle between each short-side
        edges = 6
        x_point = [0, 0, 0, 0, 0, 0]
        y_point = [0, 0, 0, 0, 0, 0]
        z_point = [height] * edges
        for edge in range(edges):  # The platform has 6 corners
            if counter % 2 == 0:
                applied_gamma = gamma * (counter / 2 - 1)
                if debug:
                    print(f"counter par = {counter} - applied gamma factor: {counter / 2 - 1}, "
                          f"applied gamma = {applied_gamma}, sign: {(-1) ** edge}")
            elif counter % 2 != 0:
                applied_gamma = gamma * ((counter - 1) / 2)
                if debug:
                    print(f"counter odd = {counter} - applied gamma factor: {(counter - 1) / 2}, "
                          f"applied gamma = {applied_gamma}, sign: {(-1) ** edge}")
            else:
                raise ValueError
            x_point[edge] = long_side * cos(applied_gamma + rotation_shift) + short_side * cos(
                applied_gamma + (-1) ** counter * pi / 2 + rotation_shift)
            y_point[edge] = long_side * sin(applied_gamma + rotation_shift) + short_side * sin(
                applied_gamma + (-1) ** counter * pi / 2 + rotation_shift)
            counter = counter + 1

        x_point.append(x_point[0])  # Append the start point as the last to plot all lines with matplotlib
        y_point.append(y_point[0])  # Append the start point as the last to plot all lines with matplotlib
        z_point.append(z_point[0])  # Append the start point as the last to plot all lines with matplotlib
        return [x_point, y_point, z_point]

    @staticmethod
    def platform_points_3d(p_i, t_t, roll, pitch, yaw):  # Figure out how to improve this one
        q_i_x = [0, 0, 0, 0, 0, 0, 0]
        q_i_y = [0, 0, 0, 0, 0, 0, 0]
        q_i_z = [0, 0, 0, 0, 0, 0, 0]
        for i in range(len(q_i_x) - 1):
            p_i_rot = vector_3d_rotation([p_i[0][i], p_i[1][i], p_i[2][i]], roll, pitch, yaw)
            q_i_x[i] = t_t[0] + p_i_rot[0]
            q_i_y[i] = t_t[1] + p_i_rot[1]
            q_i_z[i] = t_t[2] + p_i_rot[2]
        q_i_x[-1] = (q_i_x[0])
        q_i_y[-1] = (q_i_y[0])
        q_i_z[-1] = (q_i_z[0])
        return q_i_x, q_i_y, q_i_z

    def get_dynamic_platform_points(self):
        return self._dynamic_platform_points

    def get_fixed_platform_points(self):
        return self._fixed_platform_points

    def plot_platforms(self, plot_fixed_platform: bool = True, plot_dynamic_platform: bool = True):
        fig = plt.figure()
        ax = plt.axes(xlim=(-self._plot_limits, self._plot_limits), ylim=(-self._plot_limits, self._plot_limits))
        if plot_dynamic_platform:
            ax.plot(self._dynamic_platform_points[0], self._dynamic_platform_points[1], label='Dynamic Platform',
                    color=self._dynamic_platform_color, marker='o')
        if plot_fixed_platform:
            ax.plot(self._fixed_platform_points[0], self._fixed_platform_points[1], label='Fixed platform',
                    color=self._fixed_platform_color, marker='o')
        ax.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0)
        ax.grid(color='black', linestyle='-', linewidth=0.5)
        plt.show()

    def animate(self, plot_wave_data: bool = True):
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

        start = self._plot_limits
        end = self._plot_limits
        ax.set_xlim3d(-end, start)
        ax.set_ylim3d(-end, start)
        ax.set_zlim3d(0, self._plot_height)
        ax.view_init(elev=25, azim=100)
        ax.set_xlabel('$X$', fontsize=10, rotation=0)
        ax.set_ylabel('$Y$', fontsize=10, rotation=0)
        ax.set_zlabel(r'$z$', fontsize=10, rotation=0)

        x_f, y_f, z_f = self.get_fixed_platform_points()
        line2, = ax.plot(x_f, y_f, z_f, color='red', marker='o', label='Quaternion rotation 90deg')

        frames_ = 900  # TODO make dynamic
        resolution = frames_
        Tp = self._wave_period
        Hs = self._significant_wave_height
        wave_angle = self._wave_angle
        wave_frequencies = []
        for n_step in range(resolution):
            wave_frequencies.append(2 * (n_step + 0.001) / resolution)

        heave, surge, sway, roll, pitch, yaw, t_time = body_displacement(wave_frequencies, Hs, Tp, wave_angle)

        if plot_wave_data:
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

        x_points, y_points, z_points = self.get_dynamic_platform_points()
        home_height = self._home_height
        rot_cor = self._rotation_correction_factor

        def animate(i):
            x_p, y_p, z_p = self.platform_points_3d([x_points, y_points, z_points], [surge[i], sway[i],
                                                    heave[i] + home_height],
                                                    roll[i] / rot_cor, pitch[i] / rot_cor, yaw[i] / rot_cor)

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

    @staticmethod
    def _round_up(number):
        return int(number) + (number % 1 > 0)
