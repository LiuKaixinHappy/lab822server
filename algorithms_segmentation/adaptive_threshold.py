# coding=utf-8
import cv2
import numpy as np

from algorithms_base.handler import Handler
from myenums.proc_code_enum import ProcCodeEnum


def adaptive_threshold(image, k_size, ratio):
    print 'k_size:{}, ratio:{}'.format(k_size, ratio)
    img_mean = cv2.boxFilter(image, cv2.CV_32FC1, (k_size, k_size))

    out = image - (1.0 - ratio) * img_mean
    out[out >= 0] = 255
    out[out < 0] = 0

    return '自适应阈值', out.astype(np.uint8)


class AdaptiveThresholdHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.ADAPTIVE_THRESHOLD:
            return adaptive_threshold(image,
                                      int(params['kSize']),
                                      float(params['ratio']))
        else:
            return self._to_next.handle(code, params, image)
