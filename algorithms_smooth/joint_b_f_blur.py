import math

import cv2

import numpy as np

from algorithms_base.handler import Handler
from algorithms_smooth.share_methods import get_border_type
from myenums.proc_code_enum import ProcCodeEnum


def get_closeness_weight(sigma_g, k_size_w, k_size_h):
    r, c = np.mgrid[0:k_size_h:1, 0:k_size_w:1]
    r -= (k_size_h - 1) / 2
    c -= (k_size_w - 1) / 2
    close_weight = np.exp(-0.5 * (np.power(r, 2) + np.power(c, 2)) / math.pow(sigma_g, 2))
    return close_weight


def jbf(img, k_size_w, k_size_h, sigma_g, sigma_d, border_type):
    closeness_weight = get_closeness_weight(sigma_g, k_size_w, k_size_h)
    img_g = cv2.GaussianBlur(img, (k_size_w, k_size_h), sigma_g)

    center_h = (k_size_h - 1) / 2
    center_w = (k_size_w - 1) / 2

    img_p = cv2.copyMakeBorder(img, center_h, center_h, center_w, center_w, border_type)
    img_gp = cv2.copyMakeBorder(img_g, center_h, center_h, center_w, center_w, border_type)

    rows, cols = img.shape
    i, j = 0, 0

    joint_b_f = np.zeros(img.shape, np.float64)
    for r in np.arange(center_h, center_h + rows, 1):
        for c in np.arange(center_w, center_w + cols, 1):
            pixel = img_gp[r][c]

            r_top, r_bottom = r - center_h, r + center_h
            c_left, c_right = c - center_w, c + center_w

            region = img_gp[r_top:r_bottom + 1, c_left:c_right + 1]
            similarity_weight = np.exp(-0.5 * np.power(region - pixel, 2.0) / math.pow(sigma_d, 2.0))
            weight = closeness_weight * similarity_weight
            weight = weight / np.sum(weight)
            joint_b_f[i][j] = np.sum(img_p[r_top:r_bottom + 1, c_left:c_right + 1] * weight)
            j += 1
        j = 0
        i += 1
    return joint_b_f


def joint_b_f_blur(img, k_size_w, k_size_h, sigma_g, sigma_d, border_type):
    return jbf(img,
               k_size_w=k_size_w,
               k_size_h=k_size_h,
               sigma_g=sigma_g,
               sigma_d=sigma_d,
               border_type=get_border_type(border_type))


class JointBFBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.JOINT_B_F_BLUR:

            return joint_b_f_blur(image,
                                  int(params['kSizeW']),
                                  int(params['kSizeH']),
                                  float(params['sigmaG']),
                                  float(params['sigmaD']),
                                  int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
