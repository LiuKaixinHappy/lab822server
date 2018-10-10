# coding=utf-8
import base64
import os

import cv2
import numpy as np
from PIL import Image
from enum import Enum

from algorithms_base.constant import ROOT_PATH
from algorithms_base.handler import Handler
from app import app
from myenums.proc_code_enum import ProcCodeEnum
from myenums.threshold_type_enum import get_thresh_type
from util import get_unique_file_name


class FindThreshTypeEnum(Enum):
    OTSU = 0
    TRIANGLE = 1
    ENTROPY = 2
    HISTOGRAM = 3


def auto_threshold(img_name, max_val, find_thresh_type, thresh_type):
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

    thresh = 0
    if find_thresh_type == FindThreshTypeEnum.OTSU:
        thresh, thresh_img = cv2.threshold(img, thresh, max_val, cv2.THRESH_OTSU + get_thresh_type(thresh_type))
    elif find_thresh_type == FindThreshTypeEnum.TRIANGLE:
        thresh, thresh_img = cv2.threshold(img, thresh, max_val, cv2.THRESH_TRIANGLE + get_thresh_type(thresh_type))
    else:
        return None
    processed_img = Image.fromarray(thresh_img.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], ProcCodeEnum.B_F_BLUR, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as imageFile:
        base64_data = base64.b64encode(imageFile.read())
    return dict({'image': base64_data, 'log': dict({'str': thresh})})


class AutoThresholdHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.AUTO_THRESHOLD:
            img = base64.b64decode(image)
            img_name = get_unique_file_name()
            with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
                img_file.write(img)

            return auto_threshold(img_name,
                                  int(params['maxVal']),
                                  int(params['findThreshType']),
                                  int(params['threshType']))
        else:
            return self._to_next.handle(code, params, image)
