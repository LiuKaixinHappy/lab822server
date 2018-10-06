import base64
import math

import cv2
import os

import numpy as np
from PIL import Image

from algorithms.border_type_enum import get_border_type
from algorithms.constant import ROOT_PATH
from algorithms.handler import Handler
from util import get_unique_file_name
from algorithms.proc_code_enum import ProcCodeEnum


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


def joint_b_f_blur(img_name, k_size_w, k_size_h, sigma_g, sigma_d, border_type):
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

    blur = jbf(img,
               k_size_w=k_size_w,
               k_size_h=k_size_h,
               sigma_g=sigma_g,
               sigma_d=sigma_d,
               border_type=get_border_type(border_type))

    processed_img = Image.fromarray(blur.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], ProcCodeEnum.JOINT_B_F_BLUR, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as imageFile:
        base64_data = base64.b64encode(imageFile.read())
    return dict({'image': base64_data})


class JointBFBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.JOINT_B_F_BLUR:
            img = base64.b64decode(image)
            img_name = get_unique_file_name()
            with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
                img_file.write(img)

            return joint_b_f_blur(img_name,
                                  int(params['kSizeW']),
                                  int(params['kSizeH']),
                                  float(params['sigmaG']),
                                  float(params['sigmaD']),
                                  int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
