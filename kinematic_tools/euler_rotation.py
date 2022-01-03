
from math import cos, sin


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
