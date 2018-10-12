# coding=utf-8

import cv2
import numpy as np

from algorithms_base.handler import Handler
from algorithms_contour.share_methods import get_mode_type, get_method_type, get_binary_object_color
from myenums.proc_code_enum import ProcCodeEnum

CONTOUR_ON_ORIGIN = 0
CONTOUR_ONLY = 1


def accurate_contour(img, contour_width, binary_object_color, mode, method, output_type):
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    object_color = get_binary_object_color(binary_object_color)
    if object_color == 255:
        _, thresh_img = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY)
    else:
        _, thresh_img = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY_INV)
    _, contours, hierarchy = cv2.findContours(thresh_img, get_mode_type(mode), get_method_type(method))

    n = len(contours)

    if output_type == CONTOUR_ON_ORIGIN:
        for i in xrange(n):
            cv2.drawContours(img, contours, i, (255, 0, 0), contour_width)
        return img
    else:
        tmp = np.zeros(im_gray.shape, np.uint8)
        for i in xrange(n):
            cv2.drawContours(tmp, contours, i, (0, 0, 0), contour_width)
        return tmp


class AccurateContourHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.ACCURATE_CONTOUR:
            return accurate_contour(image,
                                    int(params['contourWidth']),
                                    int(params['binaryObjectColor']),
                                    int(params['mode']),
                                    int(params['method']),
                                    int(params['outputType']))
        else:
            return self._to_next.handle(code, params, image)
