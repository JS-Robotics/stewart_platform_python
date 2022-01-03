
from stewart_platform import StewartPlatform

platform = StewartPlatform(fixed_long=0.90, fixed_short=0.40, dynamic_long=0.70, dynamic_short=0.30)

print(platform.get_fixed_platform_points())
print(platform.get_dynamic_platform_points())
platform.plot_platforms(plot_dynamic_platform=True, plot_fixed_platform=True)
