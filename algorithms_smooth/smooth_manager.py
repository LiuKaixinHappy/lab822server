import base64
import os

import cv2
import numpy as np
from PIL import Image

from algorithms_base.constant import ROOT_PATH
from algorithms_base.no_process import NoProcHandler
from algorithms_smooth.b_f_blur import BFBlurHandler
from algorithms_smooth.gaussian_blur import GaussianBlurHandler
from algorithms_smooth.joint_b_f_blur import JointBFBlurHandler
from algorithms_smooth.mean_blur import MeanBlurHandler
from algorithms_smooth.media_blur import MediaBlurHandler
from util import get_unique_file_name


def do(code, params, img):
    gaussian_blur = GaussianBlurHandler()
    mean_blur = MeanBlurHandler()
    media_blur = MediaBlurHandler()
    b_f_blur = BFBlurHandler()
    joint_b_f_blur = JointBFBlurHandler()
    no_proc_handler = NoProcHandler()

    gaussian_blur.to_next(mean_blur)
    mean_blur.to_next(media_blur)
    media_blur.to_next(b_f_blur)
    b_f_blur.to_next(joint_b_f_blur)
    joint_b_f_blur.to_next(no_proc_handler)

    return gaussian_blur.handle(code, params, img)


def process(code, params, image):
    img = base64.b64decode(image)
    img_name = get_unique_file_name()
    with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
        img_file.write(img)
    img = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

    img = do(code, params, img)

    processed_img = Image.fromarray(img.astype(np.uint8))

    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], code, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))

    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as image_file:
        base64_data = base64.b64encode(image_file.read())
    return dict({'image': base64_data})


