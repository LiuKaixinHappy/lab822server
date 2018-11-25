import cv2
import numpy as np

from img_algorithms.algorithms_base import Handler
from myenums.proc_code_enum import ProcCodeEnum


def get_cosine(a, b):
    return a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_interval(arr, lower_bound, upper_bound):
    if lower_bound > upper_bound or (lower_bound < 0 < upper_bound):
        if isinstance(arr, list):
            return arr[lower_bound:] + arr[:upper_bound]
        elif isinstance(arr, np.ndarray):
            return np.concatenate((arr[lower_bound:], arr[:upper_bound]))

    return arr[lower_bound:upper_bound]


def get_cos_of_support_region(outline, point_index, max_support_region, len_outline):
    cur_point = outline[point_index]
    last_cos = 1
    last_support_arm = max_support_region
    for support_arm in range(max_support_region, -1, -1):
        if support_arm == 0:
            return support_arm, -1
        pre_point = outline[(point_index + len_outline - support_arm) % len_outline]
        nxt_point = outline[(point_index + support_arm) % len_outline]
        cosine = get_cosine(pre_point - cur_point, nxt_point - cur_point)
        if cosine <= last_cos:
            last_cos = cosine
            last_support_arm = support_arm
        else:
            return last_support_arm, last_cos


def r_j_corner(image, m_factor):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh_img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    _, contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    outline = contours[0].reshape(len(contours[0]), 2)

    corners = get_all_corners(outline, m_factor)

    cv2.drawContours(image, corners, -1, (255, 0, 0), 3)

    return image


def get_all_corners(outline, min_corner_num=30):
    len_outline = len(outline)
    max_support_region = len_outline / min_corner_num
    corners = []
    cosines = []
    support_arms = []
    for i in range(len_outline):
        support_arm, cosine = get_cos_of_support_region(outline, i,
                                                        max_support_region, len_outline)
        cosines.append(cosine)
        support_arms.append(support_arm)
    for i in range(len_outline):
        cur_arm_half = support_arms[i] / 2
        if cur_arm_half == 0:
            continue
        lower_bound = (i - cur_arm_half + len_outline) % len_outline
        upper_bound = (i + cur_arm_half + 1) % len_outline
        discriminant_interval = get_interval(cosines, lower_bound, upper_bound)
        max_index = discriminant_interval.index(max(discriminant_interval))
        if (lower_bound + max_index) % len_outline == i:
            corners.append(outline[i])
    return np.array(corners).reshape(len(corners), 1, 2)


class RJCornerHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.R_J_CORNER:
            return r_j_corner(image,
                              int(params['mFactor']))
        else:
            return self._to_next.handle(code, params, image)
