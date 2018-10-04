import base64
import cv2
import os

import numpy as np
from PIL import Image

from smoth_algorithms.border_type_enum import get_border_type
from smoth_algorithms.constant import ROOT_PATH
from smoth_algorithms.handler import Handler
from smoth_algorithms.proc_code_enum import ProcCodeEnum


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
    return dict({'imgContent': base64_data, 'imgName': processed_img_name})


class BFBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.B_F_BLUR:
            if len(image['content']) > 0:
                img = base64.b64decode(image['content'])
                img_file = open('{}/{}'.format(ROOT_PATH, image['name']), 'wb')
                img_file.write(img)
                img_file.close()
            params_dict = dict()
            for each in params:
                params_dict[each['pName']] = each['pValue']
            return b_f_blur(image['name'],
                            int(params_dict['d']),
                            float(params_dict['sigmaColor']),
                            float(params_dict['sigmaSpace']),
                            int(params_dict['borderType']))
        else:
            return self._to_next.handle(code, params, image)
