# coding=utf-8
from enum import Enum


class ProcCodeEnum(Enum):
    # 图像平滑
    GAUSSIAN_BLUR = '101'
    MEAN_BLUR = '102'
    MEDIA_BLUR = '103'
    B_F_BLUR = '104'
    JOINT_B_F_BLUR = '105'

    # 阈值分割
    AUTO_THRESHOLD = '201'
    MANUAL_THRESHOLD = '202'
    ADAPTIVE_THRESHOLD = '203'

    # 轮廓提取
    ACCURATE_CONTOUR = '301'
    FITTING_CONTOUR = '302'

    # 角点提取
    HARRIS_CORNER = '401'
    SUBPIX_CORNER = '402'
    R_J_CORNER = '403'

    # 形态学处理
    ERODE = '501'
    DILATE = '502'
