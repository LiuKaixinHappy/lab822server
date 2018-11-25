# coding=utf-8
import math

import cv2
import numpy as np
from enum import Enum

from img_algorithms.algorithms_base.handler import Handler
from myenums.proc_code_enum import ProcCodeEnum
from img_algorithms.algorithms_base.share_methods import get_thresh_type


class FindThreshTypeEnum(Enum):
    OTSU = 0
    TRIANGLE = 1
    ENTROPY = 2
    HISTOGRAM = 3


def cal_gray_hist(image):
    r, c = image.shape

    gray_hist = np.zeros([256], np.uint64)
    for i in range(r):
        for j in range(c):
            gray_hist[image[i][j]] += 1
    return gray_hist


def thresh_entropy(img, max_val, thresh_type):
    rows, cols = img.shape
    gray_hist = cal_gray_hist(img)
    norm_gray_hist = gray_hist / float(rows * cols)
    zero_cumu_moment = np.zeros([256], np.float32)
    for k in xrange(256):
        if k == 0:
            zero_cumu_moment[k] = norm_gray_hist[k]
        else:
            zero_cumu_moment[k] = zero_cumu_moment[k - 1] + norm_gray_hist[k]

    entropy = np.zeros([256], np.float32)
    for k in xrange(256):
        if k == 0:
            if norm_gray_hist[k] == 0:
                entropy[k] = 0
            else:
                entropy[k] = -norm_gray_hist[k] * math.log10(norm_gray_hist[k])
        else:
            if norm_gray_hist[k] == 0:
                entropy[k] = entropy[k - 1]
            else:
                entropy[k] = entropy[k - 1] - norm_gray_hist[k] * math.log10(norm_gray_hist[k])
    f_thresh = np.zeros([256], np.float32)
    total_entropy = entropy[255]
    for k in xrange(255):
        max_front = np.max(norm_gray_hist[0: k + 1])
        max_back = np.max(norm_gray_hist[k + 1:256])
        if max_front == 0 or zero_cumu_moment[k] == 0 or max_front == 1 or zero_cumu_moment[k] == 1 \
                or total_entropy == 0:
            f_thresh1 = 0
        else:
            f_thresh1 = entropy[k] / total_entropy * (math.log10(zero_cumu_moment[k]) / math.log10(max_front))
        if max_back == 0 or 1 - zero_cumu_moment[k] == 0 or max_back == 1 or 1 - zero_cumu_moment[k] == 1:
            f_thresh2 = 0
        else:
            if total_entropy == 0:
                f_thresh2 = (math.log10(1 - zero_cumu_moment[k]) / math.log10(max_back))
            else:
                f_thresh2 = (1 - entropy[k] / total_entropy) * (
                        math.log10(1 - zero_cumu_moment[k]) / math.log10(max_back))
        f_thresh[k] = f_thresh1 + f_thresh2

    thresh_loc = np.where(f_thresh == np.max(f_thresh))
    thresh = thresh_loc[0][0]

    return cv2.threshold(img, thresh, max_val, get_thresh_type(thresh_type))


def auto_threshold(img, max_val, find_thresh_type, thresh_type):
    thresh = 0
    if find_thresh_type == FindThreshTypeEnum.OTSU:
        thresh, thresh_img = cv2.threshold(img, thresh, max_val, cv2.THRESH_OTSU + get_thresh_type(thresh_type))
    elif find_thresh_type == FindThreshTypeEnum.TRIANGLE:
        thresh, thresh_img = cv2.threshold(img, thresh, max_val, cv2.THRESH_TRIANGLE + get_thresh_type(thresh_type))
    elif find_thresh_type == FindThreshTypeEnum.ENTROPY:
        thresh, thresh_img = thresh_entropy(img, max_val, thresh_type)
    else:
        raise Exception('哎呀～该阈值类型尚未实现，请静候佳音')
    return thresh, thresh_img


class AutoThresholdHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.AUTO_THRESHOLD:
            return auto_threshold(image,
                                  int(params['maxVal']),
                                  int(params['findThreshType']),
                                  int(params['threshType']))
        else:
            return self._to_next.handle(code, params, image)
