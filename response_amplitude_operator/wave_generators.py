from response_amplitude_operator import wave_spectrums
import random
from math import pi, sqrt, cos, sin


def irregular_waves(w, H_s, T_p, y=None, x=None):
    amplitude = []
    phase = []
    spectrum = []
    wave_frequencies_length = len(w)
    for wave_frequency in range(wave_frequencies_length):
        spectrum.append(wave_spectrums.jonswap_wave_spectrum(w[wave_frequency], H_s, T_p, y))
        s_j = spectrum[-1]
        if wave_frequency < (wave_frequencies_length - 1):
            delta_omega = w[wave_frequency + 1] - w[wave_frequency]
        else:
            delta_omega = w[wave_frequency] - w[wave_frequency-1]

        amplitude.append(sqrt(2 * s_j * delta_omega))
        random.seed((wave_frequency*1 + 6))
        phase.append(random.uniform(0, 2*pi))

    return spectrum, amplitude, phase


def irregular_surface_propagation(w, H_s, T_p, y=None, x=None):

    s_list_sp, amps, phases = irregular_waves(w, H_s, T_p, y, x)
    sim_time = []  # TODO make dynamic
    time_resolution = 30000
    for n in range(time_resolution):
        sim_time.append(600*n/time_resolution)

    surface_propagation = []
    # surface = 0
    for i in range(len(sim_time)):
        surface = 0
        for freq in range(len(w)):
            surface = surface + (amps[freq] * cos(w[freq]*sim_time[i] + phases[freq]))
        surface_propagation.append(surface)
    return sim_time, surface_propagation


def body_displacement(w, H_s, T_p, wave_direction=0, y=None, x=None):
    # sim_time, surface_propagation = irregular_surface_propagation(w, H_s, T_p, y, x)
    angle = wave_direction * pi / 180  # Convert from deg to rad
    heave = []
    surge = []
    sway = []
    roll = []
    pitch = []
    yaw = []

    s_list_sp, amps, phases = irregular_waves(w, H_s, T_p, y, x)
    sim_time = []  # TODO make dynamic
    time_resolution = 3000  # TODO make a better method of adding a simulation time
    for n in range(time_resolution):
        sim_time.append(60*n/time_resolution)

    # Determining amplitude factor on body (slender vessel)
    # heave_amp is always 1
    surge_amp = _absolute_value(cos(angle))
    sway_amp = _absolute_value(sin(angle))
    roll_amp = _absolute_value(sin(angle))
    pitch_amp = _absolute_value(cos(angle))
    yaw_amp = _absolute_value(0.5 * sin(2*angle))

    # Determining phase lag
    # have_phase is always 0rad for any direction
    if cos(angle) >= 0:
        surge_phase = pi/2  # 90deg
        pitch_phase = -pi/2  # -90deg
    else:
        surge_phase = -pi / 2  # 90deg
        pitch_phase = pi / 2  # -90deg

    if sin(angle) >= 0:
        sway_phase = pi/2  # 90deg
        roll_phase = pi/2  # 90deg
    else:
        sway_phase = -pi / 2  # 90deg
        roll_phase = -pi / 2  # 90deg

    if sin(2*angle) >= 0:
        yaw_phase = pi
    else:
        yaw_phase = 0

    print(f"surge_amp = {surge_amp}")
    print(f"sway_amp = {sway_amp}")
    print(f"roll_amp = {roll_amp}")
    print(f"pitch_amp = {pitch_amp}")
    print(f"yaw_amp = {yaw_amp}")

    for i in range(len(sim_time)):
        _heave = 0
        _surge = 0
        _sway = 0
        _roll = 0
        _pitch = 0
        _yaw = 0
        for freq in range(len(w)):
            _heave = _heave + (amps[freq] * cos(w[freq]*sim_time[i] + phases[freq]))
            _surge = _surge + (surge_amp * amps[freq] * cos(w[freq]*sim_time[i] + phases[freq] + surge_phase))
            _sway = _sway + (sway_amp * amps[freq] * cos(w[freq]*sim_time[i] + phases[freq] + sway_phase))
            _roll = _roll + (roll_amp * amps[freq] * cos(w[freq]*sim_time[i] + phases[freq] + roll_phase))
            _pitch = _pitch + (pitch_amp * amps[freq] * cos(w[freq]*sim_time[i] + phases[freq] + pitch_phase))
            _yaw = _yaw + (yaw_amp * amps[freq] * cos(w[freq]*sim_time[i] + phases[freq] + yaw_phase))

        heave.append(_heave)
        surge.append(_surge)
        sway.append(_sway)
        roll.append(_roll)
        pitch.append(_pitch)
        yaw.append(_yaw)

    return heave, surge, sway, roll, pitch, yaw, sim_time


def _absolute_value(value):
    if value < 0:
        value = -1 * value
        return value
    else:
        return value


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    test = 1
    wave_frequencies = []
    Hs = 4
    Tp = 8
    resolution = 100

    for n_step in range(resolution):
        wave_frequencies.append(2 * (n_step + 0.001) / resolution)

    if test == 0:
        t_time, wave_surface = irregular_surface_propagation(wave_frequencies, Tp, Hs)
        fig = plt.figure()
        ax = plt.axes()
        line = ax.plot(t_time, wave_surface)
        plt.grid(color='black', linestyle='-', linewidth=0.5)
        plt.show()

    if test == 1:
        heave, surge, sway, roll, pitch, yaw, t_time = body_displacement(wave_frequencies, Hs, Tp, 0)

        # Convert from rad to deg
        for step in range(len(heave)):
            roll[step] = roll[step]*180/pi
            pitch[step] = pitch[step]*180/pi
            yaw[step] = yaw[step]*180/pi

        figs, (ax1, ax2) = plt.subplots(2)

        line1 = ax1.plot(t_time, heave, label='heave [m]')
        line2 = ax1.plot(t_time, surge, label='surge [m]')
        line3 = ax1.plot(t_time, sway, label='sway [m]')
        line4 = ax2.plot(t_time, roll, label='roll [deg]')
        line5 = ax2.plot(t_time, pitch, label='pitch [deg]')
        line6 = ax2.plot(t_time, yaw, label='yaw [deg]')

        ax1.grid(color='black', linestyle='-', linewidth=0.5)
        ax2.grid(color='black', linestyle='-', linewidth=0.5)
        ax1.legend()
        ax2.legend()

        plt.show()
