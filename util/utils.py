# coding=utf-8
import base64
import os

import cv2
import uuid

from app import app
from config import get_root_path


def get_unique_file_name():
    return '{}.jpg'.format(str(uuid.uuid4()))


def img_file_to_base64(processed_img_name):
    with open('{}/{}'.format(get_root_path(), processed_img_name), "rb") as image_file:
        base64_data = base64.b64encode(image_file.read())
    return base64_data


def img_arr_to_img_file(img_name, o_code, processed_img_arr):
    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], o_code, path_and_suffix[1])
    # print processed_img_name
    cv2.imwrite('{}/{}'.format(get_root_path(), processed_img_name), processed_img_arr)
    return processed_img_name


def base64_to_img_file(image):
    img = base64.b64decode(image)
    img_name = get_unique_file_name()
    with open('{}/{}'.format(get_root_path(), img_name), 'wb') as img_file:
        img_file.write(img)
    return img_name


def delete_files(file_names):
    for file_name in file_names:
        file_path_n_name = os.path.join(get_root_path(), file_name)
        if os.path.exists(file_path_n_name):
            os.remove(file_path_n_name)
            app.logger.debug('Delete {}'.format(file_name))
        else:
            app.logger.debug('Delete error, Not Found {}'.format(file_name))
