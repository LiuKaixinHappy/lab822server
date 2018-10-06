import base64

import cv2
import os

import numpy as np
from PIL import Image

from algorithms.border_type_enum import get_border_type
from algorithms.constant import ROOT_PATH
from algorithms.handler import Handler
from util import get_unique_file_name
from algorithms.proc_code_enum import ProcCodeEnum


def mean_blur(img_name, k_size_w, k_size_h, border_type):
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

    blur = cv2.blur(img,
                    ksize=(k_size_w, k_size_h),
                    borderType=get_border_type(border_type))

    processed_img = Image.fromarray(blur.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], ProcCodeEnum.MEAN_BLUR, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as imageFile:
        base64_data = base64.b64encode(imageFile.read())
    return dict({'image': base64_data})


class MeanBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.MEAN_BLUR:
            img = base64.b64decode(image)
            img_name = get_unique_file_name()
            with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
                img_file.write(img)

            return mean_blur(img_name,
                             int(params['kSizeW']),
                             int(params['kSizeH']),
                             int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)