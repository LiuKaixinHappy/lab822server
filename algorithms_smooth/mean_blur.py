import cv2

from algorithms_base.handler import Handler
from algorithms_smooth.share_methods import get_border_type
from myenums.proc_code_enum import ProcCodeEnum


def mean_blur(img, k_size_w, k_size_h, border_type):
    return cv2.blur(img,
                    ksize=(k_size_w, k_size_h),
                    borderType=get_border_type(border_type))


class MeanBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.MEAN_BLUR:
            return mean_blur(image,
                             int(params['kSizeW']),
                             int(params['kSizeH']),
                             int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
