import cv2

from img_algorithms.algorithms_base.handler import Handler
from myenums.proc_code_enum import ProcCodeEnum


def median_blur(img, k_size):
    return cv2.medianBlur(img, ksize=k_size)


class MediaBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.MEDIA_BLUR:
            return median_blur(image, int(params['kSize']))
        else:
            return self._to_next.handle(code, params, image)
