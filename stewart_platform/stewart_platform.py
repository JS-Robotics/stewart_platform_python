from math import pi, sin, cos

from matplotlib import pyplot as plt
from matplotlib import animation


from stochastic_waves.wave_generators import irregular_surface_propagation, body_displacement
from kinematic_tools.euler_rotation import vector_3d_rotation


class StewartPlatform:

    # def __init__(self, fixed_long, fixed_short, dynamic_long, dynamic_short, home_height=2, fixed_rotation_shift=0,
    #              dynamic_rotation_shift=(60*3.1415/180)):
    def __init__(self, fixed_long, fixed_short, dynamic_long, dynamic_short, home_height=2, fixed_rotation_shift=(60*3.1415/180),
                 dynamic_rotation_shift=0):

        self._fixed_platform_color = 'red'
        self._dynamic_platform_color = 'blue'

        self._fixed_platform_points = self._generate_platform_points(long_side=fixed_long,
                                                                     short_side=fixed_short,
                                                                     height=0,
                                                                     rotation_shift=fixed_rotation_shift,
                                                                     debug=False)

        self._dynamic_platform_points = self._generate_platform_points(long_side=dynamic_long,
                                                                       short_side=dynamic_short,
                                                                       height=home_height,
                                                                       rotation_shift=dynamic_rotation_shift,
                                                                       debug=False)

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

        # TODO Should this appending be moved somewhere else?
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
        # fig = plt.figure()  # TODO is this one necessary ?
        ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))  # TODO round up to larges integer of defined platform lengths
        if plot_dynamic_platform:
            ax.plot(self._dynamic_platform_points[0], self._dynamic_platform_points[1], label='Dynamic Platform',
                    color=self._dynamic_platform_color, marker='o')
        if plot_fixed_platform:
            ax.plot(self._fixed_platform_points[0], self._fixed_platform_points[1], label='Fixed platform',
                    color=self._fixed_platform_color, marker='o')
        ax.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0)
        ax.grid(color='black', linestyle='-', linewidth=0.5)
        plt.show()

