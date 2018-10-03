import base64
import os
import cv2
import numpy as np
from PIL import Image
from cStringIO import StringIO
from algorithms.border_type_enum import get_border_type
from algorithms.constant import ROOT_PATH
from algorithms.handler import Handler
from algorithms.proc_code_enum import ProcCodeEnum


def gaussian_blur(img_name, k_size_w, k_size_h, sigma_x, sigma_y, border_type):
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

    blur = cv2.GaussianBlur(img, (k_size_w, k_size_h), sigma_x, sigma_y, get_border_type(border_type))

    processed_img = Image.fromarray(blur.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], ProcCodeEnum.GAUSSIAN_BLUR, path_and_suffix)
    processed_img.save(os.path.join(ROOT_PATH, processed_img_name), path_and_suffix[1])

    output_buffer = StringIO()
    img.save(output_buffer, format=path_and_suffix[1])
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data)
    return dict({'imgContent': base64_data, 'imgName': processed_img_name})


class GaussianBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.GAUSSIAN_BLUR:
            img = base64.b64decode(image['content'])
            img_file = open(os.path.join(ROOT_PATH, image['name']), 'wb')
            img_file.write(img)
            img_file.close()
            return gaussian_blur(img['name'], params['kSizeW'], params['kSizeH'], params['sigmaX'],
                                 params['sigmaY'], params['borderType'])
        else:
            self._to_next.handle(code, params, image)
