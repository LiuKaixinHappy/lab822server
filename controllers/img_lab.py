# coding=utf-8
import base64
import os

import cv2
import numpy as np
from PIL import Image

from algorithms_base.constant import ROOT_PATH
from algorithms_contour import contour_manager
from algorithms_sigmentation import sigmentation_manager
from algorithms_smooth import smooth_manager
from app import app
from flask import request, jsonify
from models.img_type import ImgType
from models.img_operations import ImgOperation
import json

from util import get_unique_file_name


@app.route('/')
def index():
    return 'ok'


@app.route('/imgproc/lab', methods=['GET', 'POST'])
def img_process_lab():
    if request.method == 'GET':
        messages = []
        types = ImgType.objects.exclude('id')
        for each in types:
            sub_types = ImgOperation.objects(type__name=each.name).exclude('id', 'type')
            messages.append({'type': each.name, 'subType': list(sub_types)})

        return jsonify({'result': 1, 'message': messages})
    else:
        request_body = json.loads(request.get_data())
        operation = request_body['operations'][0]

        o_code = operation['code']
        o_params = operation['params']
        image_base64 = request_body['image']

        img_name = base64_to_img_file(image_base64)

        try:
            img_arr = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)

            if int(o_code) < 200:
                processed_img_arr = smooth_manager.process(o_code, o_params, img_arr)
            elif int(o_code) < 300:
                processed_img_arr = sigmentation_manager.process(o_code, o_params, img_arr)
            elif int(o_code) < 400:
                processed_img_arr = contour_manager.process(o_code, o_params, img_arr)

            processed_img_name = img_arr_to_img_file(img_name, o_code, processed_img_arr)

            base64_data = img_file_to_base64(processed_img_name)

            return jsonify({'result': 1, 'message': dict({'image': base64_data})})
        except Exception as e:
            print e
            return jsonify({'result': 0, 'message': e.message})


def img_file_to_base64(processed_img_name):
    with open('{}/{}'.format(ROOT_PATH, processed_img_name), "rb") as image_file:
        base64_data = base64.b64encode(image_file.read())
    return base64_data


def img_arr_to_img_file(img_name, o_code, processed_img_arr):
    processed_img = Image.fromarray(processed_img_arr.astype(np.uint8))
    path_and_suffix = img_name.split('.')
    processed_img_name = '{}_{}.{}'.format(path_and_suffix[0], o_code, path_and_suffix[1])
    # print processed_img_name
    processed_img.save('{}/{}'.format(ROOT_PATH, processed_img_name))
    return processed_img_name


def base64_to_img_file(image):
    img = base64.b64decode(image)
    img_name = get_unique_file_name()
    with open('{}/{}'.format(ROOT_PATH, img_name), 'wb') as img_file:
        img_file.write(img)
    return img_name
