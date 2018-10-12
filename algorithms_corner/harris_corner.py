import cv2
import numpy as np

from algorithms_base.handler import Handler
from myenums.proc_code_enum import ProcCodeEnum


def harris_corner(image, block_size, k_size, k, threshold):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray = np.float32(img_gray)

    dst = cv2.cornerHarris(img_gray, block_size, k_size, k)

    dst = cv2.dilate(dst, None)

    image[dst > threshold * dst.max()] = [255, 0, 0]

    return image


class HarrisCornerHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.HARRIS_CORNER:
            return harris_corner(image,
                                 int(params['blockSize']),
                                 int(params['kSize']),
                                 float(params['k']),
                                 float(params['threshold']))
        else:
            return self._to_next.handle(code, params, image)
