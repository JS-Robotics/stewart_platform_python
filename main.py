from stewart_platform import StewartPlatform


platform = StewartPlatform(fixed_long=90, fixed_short=40, dynamic_long=70, dynamic_short=30,
                           home_height=10, T_p=8, H_s=4, wave_angle=50)

platform.animate(plot_wave_data=True)

