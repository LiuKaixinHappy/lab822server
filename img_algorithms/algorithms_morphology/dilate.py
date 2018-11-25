import cv2

from img_algorithms.algorithms_base import Handler
from img_algorithms.algorithms_base import get_border_type, get_shape_type
from myenums.proc_code_enum import ProcCodeEnum


def do_dilate(image, k_size, shape, iterations, border_type):
    return cv2.dilate(src=image,
                      kernel=cv2.getStructuringElement(get_shape_type(shape), (k_size, k_size)),
                      iterations=iterations,
                      borderType=get_border_type(border_type))


class DilateHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.DILATE:
            return do_dilate(image,
                             int(params['kSize']),
                             int(params['shape']),
                             int(params['iterations']),
                             int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
