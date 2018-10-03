# coding=utf-8
from smoth_algorithms import manager
from app import app
from flask import request, jsonify
from models.img_type import ImgType
from models.img_operations import ImgOperation
import json


@app.route('/')
def a():
    return "Hello World"


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
        operations = request_body['operations']
        o_code = operations['code']
        o_params = operations['params']
        image = request_body['image']
        message = manager.process(o_code, o_params, image)
        if message is None:
            return jsonify({'result': 0, 'message': '未找到图像处理方法'})

        return jsonify({'result': 1, 'message': message})
