# coding=utf-8
import base64
import os

import cv2
import numpy as np
from PIL import Image

from algorithms_base.constant import ROOT_PATH
from algorithms_base.handler import Handler
from algorithms_contour.share_methods import get_mode_type, get_method_type
from myenums.proc_code_enum import ProcCodeEnum
from util import get_unique_file_name


def is_binary_image(img):
    w, h = img.shape
    for i in xrange(w):
        for j in xrange(h):
            if img[i][j] != 255 or img[i][j] != 0:
                return False
    return True


def accurate_contour(img_name, contour_width, mode, method):
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_COLOR)

    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh_img = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY)

    _, contours, hierarchy = cv2.findContours(thresh_img, get_mode_type(mode), get_method_type(method))

    n = len(contours)

    for i in xrange(n):
        cv2.drawContours(img, contours, i, (255, 0, 0), contour_width)

    processed_img = Image.fromarray(img.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], ProcCodeEnum.MEDIA_BLUR, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as imageFile:
        base64_data = base64.b64encode(imageFile.read())
    return dict({'image': base64_data})


class AccurateContourHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.ACCURATE_CONTOUR:
            img = base64.b64decode(image)
            img_name = get_unique_file_name()
            with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
                img_file.write(img)

            return accurate_contour(img_name,
                                    int(params['contourWidth']),
                                    int(params['mode']),
                                    int(params['method']))
        else:
            return self._to_next.handle(code, params, image)
