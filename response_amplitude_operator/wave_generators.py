import wave_spectrums
import random
from math import pi, sqrt, cos


def irregular_waves(w, H_s, T_p, y=None, x=None):
    amplitude = []
    phase = []
    spectrum = []
    wave_frequencies_length = len(wave_frequencies)
    for wave_frequency in range(wave_frequencies_length):
        spectrum.append(wave_spectrums.jonswap_wave_spectrum(w[wave_frequency], H_s, T_p, y))
        s_j = spectrum[-1]
        if wave_frequency < (wave_frequencies_length - 1):
            delta_omega = w[wave_frequency + 1] - w[wave_frequency]
        else:
            delta_omega = w[wave_frequency] - w[wave_frequency-1]

        amplitude.append(sqrt(2 * s_j * delta_omega))
        random.seed((wave_frequency*2 + 4))
        phase.append(random.uniform(0, 2*pi))
        # print(random.uniform(0, 2*pi))

    return spectrum, amplitude, phase


def irregular_surface_propagation(w, H_s, T_p, y=None, x=None):

    s_list_sp, amps, phases = irregular_waves(w, H_s, T_p, y, x)
    sim_time = []
    time_resolution = 3000
    for n in range(time_resolution):
        sim_time.append(60*n/time_resolution)

    rao = []
    surface = 0
    for i in range(len(sim_time)):
        # surface = 0
        for freq in range(len(wave_frequencies)):
            surface = surface + (amps[freq] * cos(wave_frequencies[freq]*sim_time[i] * phases[freq]))
        rao.append(surface)
    return sim_time, rao


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    wave_frequencies = []
    Hs = 4
    Tp = 8
    resolution = 100

    for n_step in range(resolution):
        wave_frequencies.append(2 * (n_step + 0.001) / resolution)
    t_time, wave_surface = irregular_surface_propagation(wave_frequencies, Tp, Hs)

    fig = plt.figure()
    ax = plt.axes()
    line2 = ax.plot(t_time, wave_surface)
    plt.grid(color='black', linestyle='-', linewidth=0.5)
    plt.show()
