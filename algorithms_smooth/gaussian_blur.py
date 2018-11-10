import cv2

from algorithms_base.handler import Handler
from algorithms_base.share_methods import get_border_type
from myenums.proc_code_enum import ProcCodeEnum


def gaussian_blur(image, k_size_w, k_size_h, sigma_x, sigma_y, border_type):
    return cv2.GaussianBlur(image,
                            ksize=(k_size_w, k_size_h),
                            sigmaX=sigma_x,
                            sigmaY=sigma_y,
                            borderType=get_border_type(border_type))


class GaussianBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.GAUSSIAN_BLUR:

            return gaussian_blur(image,
                                 int(params['kSizeW']),
                                 int(params['kSizeH']),
                                 float(params['sigmaX']),
                                 float(params['sigmaY']),
                                 int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
