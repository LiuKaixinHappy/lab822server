# coding=utf-8
import cv2
from enum import Enum

from algorithms_base.handler import Handler
from myenums.proc_code_enum import ProcCodeEnum
from algorithms_segmentation.share_methods import get_thresh_type


class FindThreshTypeEnum(Enum):
    OTSU = 0
    TRIANGLE = 1
    ENTROPY = 2
    HISTOGRAM = 3


def auto_threshold(img, max_val, find_thresh_type, thresh_type):
    thresh = 0
    if find_thresh_type == FindThreshTypeEnum.OTSU:
        thresh, thresh_img = cv2.threshold(img, thresh, max_val, cv2.THRESH_OTSU + get_thresh_type(thresh_type))
    elif find_thresh_type == FindThreshTypeEnum.TRIANGLE:
        thresh, thresh_img = cv2.threshold(img, thresh, max_val, cv2.THRESH_TRIANGLE + get_thresh_type(thresh_type))
    else:
        raise Exception('哎呀～该阈值类型尚未实现，请静候佳音')
    return thresh, thresh_img


class AutoThresholdHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.AUTO_THRESHOLD:
            return auto_threshold(image,
                                  int(params['maxVal']),
                                  int(params['findThreshType']),
                                  int(params['threshType']))
        else:
            return self._to_next.handle(code, params, image)
