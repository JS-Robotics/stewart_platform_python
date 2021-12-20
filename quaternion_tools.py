# https://gamedev.stackexchange.com/questions/28395/rotating-vector3-by-a-quaternion
# https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion/535223 - Real good link
# https://marc-b-reynolds.github.io/quaternions/2017/08/08/QuatRotMatrix.html -- Quat rot mat
# http://www.songho.ca/opengl/gl_quaternion.html -- Rot matrix derivationn
# https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles -- Fire wikipedia page

from math import asin, atan2, pi, cos, sin


def hamilton_product(a, b):
    hp = [
        a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3],
        a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2],
        a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1],
        a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0]
    ]
    return hp


def quaternion_rotation(q, p):
    if len(q) != 4:
        print(f"size of quaternion q != 4, actual size: {len(q)}")
        return -1
    if len(p) != 3:
        print(f"size of vector point p != 3, actual size: {len(p)}")
        return -1

    q_rot_mat = [
        2*q[0]*q[0] - 1 + 2*q[1]*q[1], 2*q[1]*q[2] - 2*q[0]*q[3], 2*q[1]*q[3] + 2*q[0]*q[2],
        2*q[1]*q[2] + 2*q[0]*q[3], 2*q[0]**2 - 1 + q[2]**2, 2*q[2]*q[3] - 2*q[0]*q[1],
        2*q[1]*q[3] - 2*q[0]*q[2], 2*q[2]*q[3] + 2*q[0]*q[1], 2*q[0]*q[0] - 1 + 2*q[3]*q[3]
    ]

    rot = [
        q_rot_mat[0]*p[0] + q_rot_mat[1]*p[1] + q_rot_mat[2]*p[2],
        q_rot_mat[3]*p[0] + q_rot_mat[4]*p[1] + q_rot_mat[5]*p[2],
        q_rot_mat[6] * p[0] + q_rot_mat[7] * p[1] + q_rot_mat[8] * p[2],
    ]
    return rot


def quaternion_to_euler(q, deg: bool = False):
    alpha = atan2(2 * (q[0] * q[1] + q[2] * q[3]), 1 - 2 * (q[1] ** 2 + q[2] ** 2))
    beta = asin(round(2 * (q[0] * q[2] - q[3] * q[1]), 3))
    gamma = atan2(2 * (q[0] * q[3] + q[1] * q[2]), 1 - 2 * (q[2] ** 2 + q[3] ** 2))

    if deg:
        alpha = alpha*180/pi
        beta = beta*180/pi
        gamma = gamma*180/pi

    return [alpha, beta, gamma]


def vector_3d_rotation(vector3, alpha, beta, gamma):
    c1 = cos(alpha)
    c2 = cos(beta)
    c3 = cos(gamma)

    s1 = sin(alpha)
    s2 = sin(beta)
    s3 = sin(gamma)

    rot_mat = [
        c3*c2, -s3*c1 + c3*s2*s1, s3*s1 + c3*s2*c1,
        s3*c2, c3*c1 + s3*s2*s1, -c3*s1 + s3*s2*c1,
        -s2,       c2*s1,            c2*c1
    ]

    rotated = [
        rot_mat[0]*vector3[0] + rot_mat[1]*vector3[1] + rot_mat[2]*vector3[2],
        rot_mat[3]*vector3[0] + rot_mat[4]*vector3[1] + rot_mat[5]*vector3[2],
        rot_mat[6]*vector3[0] + rot_mat[7]*vector3[1] + rot_mat[8]*vector3[2]
        ]
    return rotated
