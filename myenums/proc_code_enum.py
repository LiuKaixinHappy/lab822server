from enum import Enum


class ProcCodeEnum(Enum):
    GAUSSIAN_BLUR = '101'
    MEAN_BLUR = '102'
    MEDIA_BLUR = '103'
    B_F_BLUR = '104'
    JOINT_B_F_BLUR = '105'

    AUTO_THRESHOLD = '201'
    MANUAL_THRESHOLD = '202'
    ADAPTIVE_THRESHOLD = '203'
