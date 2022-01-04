from stewart_platform import StewartPlatform


platform = StewartPlatform(fixed_long=90, fixed_short=40, dynamic_long=70, dynamic_short=30)
platform.animate(plot_wave_date=False)
