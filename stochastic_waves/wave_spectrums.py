# The calculated wave spectrum utilizing the equations in accordance with DNVGL-CG-0130
# https://rules.dnv.com/docs/pdf/DNV/CG/2018-01/DNVGL-CG-0130.pdf

from math import exp, pi, log, sqrt
import numpy as np

# Pierson–Moskowitz (PM) wave spectrum
def pierson_moskowitz_wave_spectrum(w, H_s, T_p):
    """
    :param w : The wave frequency [rad/s]
    :param T_p: Significant/mean wave height [m]
    :param H_s: Significant/mean wave period [s]
    :return: S_PM energy at the given wave frequency [m^2s]
    """
    w_p = 2 * pi / T_p  # spectral peak frequency = 2π/Tp [rad/s]
    s_pm = 5 / 16 * H_s ** 2 * w_p ** 4 * w ** (-5) * exp(-5 / 4 * (w / w_p) ** (-4))
    return s_pm


# Jonswap (J) wave spectrum
def jonswap_wave_spectrum(w, H_s, T_p, y=None):
    """
    :param w: The wave frequency [rad/s]
    :param T_p: Significant/mean wave height [m]
    :param H_s:  Significant/mean wave period [s]
    :param y:  Wave peak shape parameter [-]
    :return: S_J energy at the given frequency [m^2s]
    """
    peak_shape_parameter_selector = T_p / sqrt(H_s)
    if y is None:
        if peak_shape_parameter_selector <= 3.6:
            y = 5
        elif peak_shape_parameter_selector >= 5.0:
            y = 1
        else:
            y = exp(5.75 - 1.15 * T_p/sqrt(H_s))

    # Determine the spectral width parameter (sigma)
    w_p = 2 * pi / T_p  # spectral peak frequency = 2π/Tp [rad/s]
    if w <= w_p:
        sigma = 0.07
    else:
        sigma = 0.09
    a_y = 1 - 0.287 * log(y)  # Which is a normalizing factor
    s_jonswap = a_y * y**exp(-0.5*((w-w_p)/(sigma*w_p))**2) * pierson_moskowitz_wave_spectrum(w, H_s, T_p)
    return s_jonswap


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from matplotlib import animation
    test = 1

    if test == 0:
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 2), ylim=(0, 10))

        freq = []
        s_list = []
        Hs = 8
        Tp = 10
        resolution = 1000

        for n in range(resolution):
            freq.append(2 * (n + 0.001) / resolution)

        for i in freq:
            s_list.append(pierson_moskowitz_wave_spectrum(i, Tp, Hs))
        line = ax.plot(freq, s_list)
        plt.show()

    if test == 1:
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 3), ylim=(0, 6))

        freq = []
        s_list_1 = []
        s_list_2 = []
        s_list_5 = []
        Hs = 4
        Tp = 8
        resolution = 1000

        for n in range(resolution):
            freq.append(3 * (n + 0.001) / resolution)

        for i in freq:
            s_list_1.append(jonswap_wave_spectrum(i, Tp, Hs, 1))
            s_list_2.append(jonswap_wave_spectrum(i, Tp, Hs, 2))
            s_list_5.append(jonswap_wave_spectrum(i, Tp, Hs, 5))

        line1 = ax.plot(freq, s_list_1)
        line2 = ax.plot(freq, s_list_2)
        line3 = ax.plot(freq, s_list_5)
        plt.grid(color='black', linestyle='-', linewidth=0.5)
        plt.show()

    if test == 2:
        a = np.array([[1, 2], [2, 4], [3, 6], [5, 8], [8, 0]])
        omega = a[:, 0]
        print(f"Omega = {omega}")
        period = 2*pi/omega
        print(f"period = {period}")
        delta_omega = np.zeros(len(omega))
        print(f"delta_omega = {delta_omega}")
        delta_omega[:-1] = np.diff(omega)
        print(f"delta_omega = {delta_omega}")
        delta_omega[-1] = delta_omega[-2]
        print(f"delta_omega = {delta_omega}")
        # omega = a[:]



