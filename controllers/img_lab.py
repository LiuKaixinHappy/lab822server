# coding=utf-8
import base64
import logging
import os
import traceback

import cv2
import numpy as np
from PIL import Image

from algorithms_base.constant import ROOT_PATH
from algorithms_contour import contour_manager
from algorithms_segmentation import segmentation_manager
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
        try:
            img_name = base64_to_img_file(image_base64)
        except IOError as e:
            app.logger.exception(e)
            return jsonify({'result': 0, 'message': '哎呀～图片base64编码转化失败，请再试一次或换张图'})

        log = None
        try:
            if int(o_code) < 200:
                img_arr = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)
                if img_arr is None:
                    return jsonify({'result': 0, 'message': '哎呀～图片读取失败，请联系管理员'})

                processed_img_arr = smooth_manager.process(o_code, o_params, img_arr)
            elif int(o_code) < 300:
                img_arr = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_GRAYSCALE)
                if img_arr is None:
                    return jsonify({'result': 0, 'message': '哎呀～图片读取失败，请联系管理员'})

                thresh, processed_img_arr = segmentation_manager.process(o_code, o_params, img_arr)
                log = dict({'str': '最佳阈值为{}'.format(thresh)})
            elif int(o_code) < 400:
                img_arr = cv2.imread(os.path.join(ROOT_PATH, img_name), cv2.IMREAD_COLOR)
                if img_arr is None:
                    return jsonify({'result': 0, 'message': '哎呀～图片读取失败，请联系管理员'})

                processed_img_arr = contour_manager.process(o_code, o_params, img_arr)
            else:
                return jsonify({'result': 0, 'message': '哎呀～该方法尚未完成，请静候佳音'})
        except Exception as e:
            app.logger.exception(e)
            return jsonify({'result': 0, 'message': '处理失败:{}'.format(e.message)})

        try:
            processed_img_name = img_arr_to_img_file(img_name, o_code, processed_img_arr)
        except IOError as e:
            app.logger.exception(e)
            return jsonify({'result': 0, 'message': '哎呀～处理后图片保存失败，请再试一次'})

        try:
            base64_data = img_file_to_base64(processed_img_name)
        except Exception as e:
            app.logger.exception(e)
            return jsonify({'result': 0, 'message': '哎呀～图片转换传输失败，请再试一次'})

        if log is None:
            message = dict({'image': base64_data})
        else:
            message = dict({'image': base64_data, 'log': log})
        return jsonify({'result': 1, 'message': message})


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
