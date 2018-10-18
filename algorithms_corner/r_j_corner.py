import cv2
import numpy as np

from algorithms_base.handler import Handler
from myenums.proc_code_enum import ProcCodeEnum


def get_cosine(a, b):
    return a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))


def r_j_corner(image, m_factor):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh_img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    _, contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contour = contours[0].reshape(len(contours[0]), 2)

    n = len(contour)

    m = int(n * m_factor)

    local_maxs, sizes = get_local_max_and_size(contour, m, n)

    corners = get_corners(contour, local_maxs, n, sizes)

    cv2.drawContours(image, corners, -1, (255, 0, 0), 1)

    return image


def get_corners(contour, local_maxs, n, sizes):
    corners = []
    for i in range(n):
        r = sizes[i] / 2
        if r == 0:
            continue
        right = (i + r) % n
        left = (i + n - r) % n
        if left > right:
            splice = local_maxs[left:] + local_maxs[:right + 1]
        else:
            splice = local_maxs[left:right + 1]
        if (left + splice.index(max(splice))) % n == i:
            corners.append(contour[i])
    return np.array(corners).reshape(len(corners), 1, 2)


def get_local_max_and_size(contour, m, n):
    local_maxs = []
    sizes = []
    for i in range(n):
        tmp_min = 2
        for j in range(m - 1, -1, -1):
            if j == 0:
                sizes.append(j)
                local_maxs.append(-1)
                break
            x1 = contour[i]
            x2 = contour[(i + j) % n]
            x3 = contour[(i + n - j) % n]
            a = x2 - x1
            b = x3 - x2
            cosine = get_cosine(a, b)
            if cosine <= tmp_min:
                tmp_min = cosine
            else:
                sizes.append(j)
                local_maxs.append(cosine)
                break
    return local_maxs, sizes


class RJCornerHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.R_J_CORNER:
            return r_j_corner(image,
                              float(params['mFactor']))
        else:
            return self._to_next.handle(code, params, image)
