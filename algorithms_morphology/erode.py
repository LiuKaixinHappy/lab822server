import cv2

from algorithms_base.handler import Handler
from algorithms_base.share_methods import get_border_type, get_shape_type
from myenums.proc_code_enum import ProcCodeEnum


def do_erode(image, k_size, shape, iterations, border_type, border_value):
    return cv2.erode(image, cv2.getStructuringElement(get_shape_type(shape), (k_size, k_size)), iterations,
                     get_border_type(border_type),
                     border_value)


class ErodeHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.ERODE:
            return do_erode(image,
                            int(params['kSize']),
                            int(params['shape']),
                            int(params['iterations']),
                            int(params['borderType']),
                            int(params['borderValue']))
        else:
            return self._to_next.handle(code, params, image)
