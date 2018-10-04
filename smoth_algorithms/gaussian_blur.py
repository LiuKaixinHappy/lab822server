import base64
import os
import cv2
import numpy as np
from PIL import Image
from smoth_algorithms.border_type_enum import get_border_type
from smoth_algorithms.constant import ROOT_PATH
from smoth_algorithms.handler import Handler
from smoth_algorithms.proc_code_enum import ProcCodeEnum


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

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as imageFile:
        base64_data = base64.b64encode(imageFile.read())
    return dict({'imgContent': base64_data, 'imgName': processed_img_name})


class GaussianBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.GAUSSIAN_BLUR:
            if len(image['content']) > 0:
                img = base64.b64decode(image['content'])
                img_file = open('{}/{}'.format(ROOT_PATH, image['name']), 'wb')
                img_file.write(img)
                img_file.close()
            params_dict = dict()
            for each in params:
                params_dict[each['pName']] = each['pValue']
            return gaussian_blur(image['name'],
                                 int(params_dict['kSizeW']),
                                 int(params_dict['kSizeH']),
                                 float(params_dict['sigmaX']),
                                 float(params_dict['sigmaY']),
                                 int(params_dict['borderType']))
        else:
            return self._to_next.handle(code, params, image)
