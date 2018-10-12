# coding=utf-8
import cv2


# NOTE:顺序不可变
def get_mode_type(index):
    """
    获得轮廓检测模式.
    RETR_EXTERNAL: 最外围轮廓
    RETR_LIST: 检测所有轮廓，包括内围、外围，但是轮廓不建立等级关系
    RETR_CCOMP: 检测所有轮廓，但是只建立两个等级关系
    RETR_TREE: 检测所有轮廓，建立等级树

    :param index: 用户选择索引
    :return:
    """
    mode_type = [cv2.RETR_EXTERNAL,
                 cv2.RETR_LIST,
                 cv2.RETR_CCOMP,
                 cv2.RETR_TREE]
    return mode_type[index]


# NOTE:顺序不可变
def get_method_type(index):
    """
    获得轮廓的近似方法
    CHAIN_APPROX_NONE: 保留边界所有连续轮廓点
    CHAIN_APPROX_SIMPLE: 仅保留拐点信息
    CHAIN_APPROX_TC89_L1, CHAIN_APPROX_TC89_KCOS: Teh-Chin近似算法

    :param index:
    :return:
    """
    method_type = [cv2.CHAIN_APPROX_NONE,
                   cv2.CHAIN_APPROX_SIMPLE,
                   cv2.CHAIN_APPROX_TC89_L1,
                   cv2.CHAIN_APPROX_TC89_KCOS]
    return method_type[index]


# NOTE:顺序不可变
def get_binary_object_color(index):
    """
    获得二值化后物体的颜色

    :param index:
    :return:
    """
    binary_object_color = [0, 255]
    return binary_object_color[index]

