import base64
import os

import cv2
import numpy as np
from PIL import Image

from algorithms.constant import ROOT_PATH
from algorithms.handler import Handler
from util import get_unique_file_name
from algorithms.proc_code_enum import ProcCodeEnum


def median_blur(img_name, k_size):
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

    blur = cv2.medianBlur(img, ksize=k_size)

    processed_img = Image.fromarray(blur.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], ProcCodeEnum.MEDIA_BLUR, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as imageFile:
        base64_data = base64.b64encode(imageFile.read())
    return dict({'image': base64_data})


class MediaBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.MEDIA_BLUR:
            img = base64.b64decode(image)
            img_name = get_unique_file_name()
            with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
                img_file.write(img)

            return median_blur(img_name, int(params['kSize']))
        else:
            return self._to_next.handle(code, params, image)
