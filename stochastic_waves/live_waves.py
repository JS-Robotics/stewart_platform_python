import time

import numpy as np

from stochastic_waves import wave_spectrums
import random
from math import pi, sqrt, cos, sin, exp, log
from matplotlib import pyplot as plt
from matplotlib import animation

# Pierson–Moskowitz (PM) wave spectrum
def _pierson_moskowitz_wave_spectrum(w, H_s, T_p):
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
def _jonswap_wave_spectrum(w, H_s, T_p, y=None):
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
    s_jonswap = a_y * y**exp(-0.5*((w-w_p)/(sigma*w_p))**2) * _pierson_moskowitz_wave_spectrum(w, H_s, T_p)
    return s_jonswap


def live_irregular_wave(t, w, H_s, T_p, y=None, x=None):
    wave_frequencies_length = len(w)
    surface_elevation = 0
    for wave_frequency in range(wave_frequencies_length):
        if wave_frequency < (wave_frequencies_length - 1):
            delta_omega = w[wave_frequency + 1] - w[wave_frequency]
        else:
            delta_omega = w[wave_frequency] - w[wave_frequency-1]
        s_j = (wave_spectrums.jonswap_wave_spectrum(w[wave_frequency], H_s, T_p, y))
        amplitude = (sqrt(2 * s_j * delta_omega))
        random.seed((wave_frequency*1 + 6))
        phase = w[wave_frequency]*t + (random.uniform(0, 2*pi))
        # phase = w[wave_frequency]*t

        surface_elevation += amplitude*cos(phase)

    return surface_elevation


def _absolute_value(value):
    if value < 0:
        value = -1 * value
        return value
    else:
        return value


class ElapsedTimer:
    def __init__(self):
        self._start_time = time.time()
        self._elapsed_time = 0

    def _update_time(self):
        self._elapsed_time = time.time() - self._start_time

    def get_elapsed_time(self):
        self._update_time()
        return self._elapsed_time


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    test = 0
    wave_frequencies = []
    Hs = 4
    Tp = 8
    resolution = 20

    for n_step in range(resolution):
        wave_frequencies.append(2 * (n_step + 0.001) / resolution)

    if test == 0:
        timer = ElapsedTimer()
        fig = plt.figure()
        ax = plt.axes(xlim=(-10,10), ylim=(-10,10))
        line, = ax.plot([], [], marker = 'o')
        x_0 = 0
        y_0 = 0

        def init():
            line.set_data([], [])
            return line,

        def animate(i):
            t = timer.get_elapsed_time()
            a = live_irregular_wave(t, wave_frequencies, Tp, Hs)
            print(f"a: {a}, time: {t}")
            x = 0
            y = a
            x = [x-0.001, x]
            y = [y-0.001, y]
            line.set_data(x, y)
            return line,

        plt.grid(color='black', linestyle='-', linewidth=0.5)
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)
        plt.show()

    if test == 1:
        t = 0
        print(_jonswap_wave_spectrum(1, 8, 10, 1))
        a, phi = live_irregular_wave(t, wave_frequencies, Tp, Hs)
        print(f"a: {a}, phi: {phi}")
        # time.sleep(0.1)

    if test == 2:
        timer = ElapsedTimer()
        run = True
        while run:
            try:
                print(timer.get_elapsed_time())
                time.sleep(0.25)
            except KeyboardInterrupt:
                print("Keyboard interrupt detecting: stopping...")
                run = False

    if test == 3:
        fig = plt.figure()

        sim_time = []  # TODO make dynamic
        elev = []
        time_resolution = 3000  # TODO make a better method of adding a simulation time
        for n in range(time_resolution):
            sim_time.append(60 * n / time_resolution)

        for time in sim_time:
                elev.append(live_irregular_wave(time, wave_frequencies, 4, 8))  # HS, TP

        ax = plt.axes(xlim=(0, 60), ylim=(-Hs, Hs))
        line, = ax.plot(sim_time, elev)
        plt.grid(color='black', linestyle='-', linewidth=0.5)
        plt.show()


