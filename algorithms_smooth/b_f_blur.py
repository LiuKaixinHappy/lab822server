import cv2

from algorithms_base.handler import Handler
from algorithms_smooth.share_methods import get_border_type
from myenums.proc_code_enum import ProcCodeEnum


def b_f_blur(img, d, sigma_color, sigma_space, border_type):
    return cv2.bilateralFilter(img,
                               d=d,
                               sigmaColor=sigma_color,
                               sigmaSpace=sigma_space,
                               borderType=get_border_type(border_type))


class BFBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.B_F_BLUR:

            return b_f_blur(image,
                            int(params['d']),
                            float(params['sigmaColor']),
                            float(params['sigmaSpace']),
                            int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
