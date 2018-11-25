import cv2
import numpy as np

from img_algorithms.algorithms_base.handler import Handler
from myenums.proc_code_enum import ProcCodeEnum


def sub_pixel_corner(image, win_size, zero_zone, criteria_max_count, criteria_epsilon):
    # TODO：分割红色，为角点
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh_img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    thresh_img = np.uint8(thresh_img)

    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh_img)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, criteria_max_count, criteria_epsilon)
    corners = cv2.cornerSubPix(img_gray, np.float32(centroids), (win_size, win_size), (zero_zone, zero_zone), criteria)

    corners = np.int0(corners)
    image[corners[:, 1], corners[:, 0]] = [0, 255, 0]
    return image


class SubPixelCornerHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.SUBPIX_CORNER:
            return sub_pixel_corner(image,
                                    int(params['winSize']),
                                    int(params['zeroZone']),
                                    float(params['criteriaMaxCount']),
                                    float(params['criteriaEpsilon']))
        else:
            return self._to_next.handle(code, params, image)
