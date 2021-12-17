from math import pi, sin, cos
from quaternion_tools import quaternion_rotation, quaternion_to_euler

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    angle = 90
    rotation = angle/180*pi
    p = [1, 0, 0]
    q = [cos(rotation/2), 0, 0, sin(rotation/2)]
    print(quaternion_rotation(q, p))
    print(quaternion_to_euler(q, deg=True))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
