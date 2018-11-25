# coding=utf-8
import os

import cv2

from img_algorithms import contour_manager
from img_algorithms import corner_manager
from img_algorithms import morphology_manager
from img_algorithms import segmentation_manager
from img_algorithms import smooth_manager
from app import app
from flask import request, jsonify
from models.img_type import ImgType
from models.img_operations import ImgOperation
import json

from util import get_root_path, base64_to_img_file, img_arr_to_img_file, img_file_to_base64
from util import get_swagger_path


@app.route('/swagger')
def swagger():
    with open(get_swagger_path()) as f:
        s = f.read()
    return str(s)


@app.route('/')
def hello():
    return 'hello'


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
                img_arr = cv2.imread(os.path.join(get_root_path, img_name))
                if img_arr is None:
                    return jsonify({'result': 0, 'message': '[图像平滑]图片读取失败，请联系QQ:644306737'})

                processed_img_arr = smooth_manager.process(o_code, o_params, img_arr)
            elif int(o_code) < 300:
                img_arr = cv2.imread(os.path.join(get_root_path, img_name), cv2.IMREAD_GRAYSCALE)
                if img_arr is None:
                    return jsonify({'result': 0, 'message': '[阈值分割]图片读取失败，请联系QQ:644306737'})

                thresh, processed_img_arr = segmentation_manager.process(o_code, o_params, img_arr)
                log = dict({'str': '最佳阈值为{}'.format(thresh)})
            elif int(o_code) < 400:
                img_arr = cv2.imread(os.path.join(get_root_path, img_name), cv2.IMREAD_COLOR)
                if img_arr is None:
                    return jsonify({'result': 0, 'message': '[轮廓提取]图片读取失败，请联系QQ:644306737'})

                processed_img_arr = contour_manager.process(o_code, o_params, img_arr)
            elif int(o_code) < 500:
                img_arr = cv2.imread(os.path.join(get_root_path, img_name), cv2.IMREAD_COLOR)
                if img_arr is None:
                    return jsonify({'result': 0, 'message': '[角点检测]图片读取失败，请联系QQ:644306737'})

                processed_img_arr = corner_manager.process(o_code, o_params, img_arr)
            elif int(o_code) < 600:
                img_arr = cv2.imread(os.path.join(get_root_path, img_name))
                if img_arr is None:
                    return jsonify({'result': 0, 'message': '[形态学处理]图片读取失败，请联系QQ:644306737'})

                processed_img_arr = morphology_manager.process(o_code, o_params, img_arr)
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


@app.route('/imgproc/learning/<section>/<title>', methods=['GET'])
def img_process_learning(section, title):
    try:
        with open(os.path.join('/var/lib/jenkins/workspace/data/img_proc/',
                               section, '{}.md'.format(title))) as f:
            content = f.read()
        return jsonify({'result': 1, 'message': dict({'content': content})})
    except Exception as e:
        app.logger.exception(e)
        return jsonify({'result': 0, 'message': '文件未找到'})
