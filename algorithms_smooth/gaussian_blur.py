import base64
import os

import cv2
import numpy as np
from PIL import Image

from algorithms_base.handler import Handler
from algorithms_smooth.share_methods import get_border_type
from algorithms_base.constant import ROOT_PATH
from util import get_unique_file_name
from myenums.proc_code_enum import ProcCodeEnum


def gaussian_blur(img_name, k_size_w, k_size_h, sigma_x, sigma_y, border_type):
    # print('{},{},{},{},{},{}'.format(img_name, k_size_w, k_size_h, sigma_x, sigma_y, get_border_type(border_type)))
    # print('type:{},{},{},{},{},{}'.format(type(img_name), type(k_size_w),
    #                                       type(k_size_h), type(sigma_x), type(sigma_y),
    #                                       type(get_border_type(border_type))))
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

    blur = cv2.GaussianBlur(img,
                            ksize=(k_size_w, k_size_h),
                            sigmaX=sigma_x,
                            sigmaY=sigma_y,
                            borderType=get_border_type(border_type))

    processed_img = Image.fromarray(blur.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], ProcCodeEnum.GAUSSIAN_BLUR, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as image_file:
        base64_data = base64.b64encode(image_file.read())
    return dict({'image': base64_data})


class GaussianBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.GAUSSIAN_BLUR:
            img = base64.b64decode(image)
            img_name = get_unique_file_name()
            with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
                img_file.write(img)

            return gaussian_blur(img_name,
                                 int(params['kSizeW']),
                                 int(params['kSizeH']),
                                 float(params['sigmaX']),
                                 float(params['sigmaY']),
                                 int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
