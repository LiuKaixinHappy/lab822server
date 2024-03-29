import cv2

from img_algorithms.algorithms_base import Handler
from img_algorithms.algorithms_base import get_thresh_type
from myenums.proc_code_enum import ProcCodeEnum


def manual_threshold(image, max_val, thresh, thresh_type):
    return cv2.threshold(image, thresh, max_val, get_thresh_type(thresh_type))


class ManualThresholdHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.MANUAL_THRESHOLD:
            return manual_threshold(image,
                                    int(params['maxVal']),
                                    int(params['thresh']),
                                    int(params['threshType']))
        else:
            return self._to_next.handle(code, params, image)
