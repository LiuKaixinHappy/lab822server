import cv2

from img_algorithms.algorithms_base import Handler
from img_algorithms.algorithms_base import get_shape_type, get_border_type, get_morphology_operations
from myenums.proc_code_enum import ProcCodeEnum


def do_operations(image, k_size, shape, op, iterations, border_type):
    return cv2.morphologyEx(src=image,
                            kernel=cv2.getStructuringElement(get_shape_type(shape), (k_size, k_size)),
                            op=get_morphology_operations(op),
                            iterations=iterations,
                            borderType=get_border_type(border_type))


class MorphOperationsCalHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.MORPH_OPERATIONS_CAL:
            return do_operations(image,
                                 int(params['kSize']),
                                 int(params['shape']),
                                 int(params['op']),
                                 int(params['iterations']),
                                 int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
