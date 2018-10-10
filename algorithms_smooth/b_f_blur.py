import base64

import cv2
import os

import numpy as np
from PIL import Image

from algorithms_base.handler import Handler
from algorithms_smooth.share_methods import get_border_type
from algorithms_base.constant import ROOT_PATH
from util import get_unique_file_name
from myenums.proc_code_enum import ProcCodeEnum


def b_f_blur(img_name, d, sigma_color, sigma_space, border_type):
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

    blur = cv2.bilateralFilter(img,
                               d=d,
                               sigmaColor=sigma_color,
                               sigmaSpace=sigma_space,
                               borderType=get_border_type(border_type))

    processed_img = Image.fromarray(blur.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], ProcCodeEnum.B_F_BLUR, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as imageFile:
        base64_data = base64.b64encode(imageFile.read())
    return dict({'image': base64_data})


class BFBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.B_F_BLUR:
            img = base64.b64decode(image)
            img_name = get_unique_file_name()
            with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
                img_file.write(img)

            return b_f_blur(img_name,
                            int(params['d']),
                            float(params['sigmaColor']),
                            float(params['sigmaSpace']),
                            int(params['borderType']))
        else:
            return self._to_next.handle(code, params, image)
