# coding=utf-8
from algorithms_contour import contour_manager
from algorithms_sigmentation import sigmentation_manager
from algorithms_smooth import smooth_manager
from app import app
from flask import request, jsonify
from models.img_type import ImgType
from models.img_operations import ImgOperation
import json

from my_exceptions import ImageProcError


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
        image = request_body['image']

        message = None
        try:
            if int(o_code) < 200:
                message = smooth_manager.process(o_code, o_params, image)
            elif int(o_code) < 300:
                message = sigmentation_manager.process(o_code, o_params, image)
            elif int(o_code) < 400:
                message = contour_manager.process(o_code, o_params, image)

            return jsonify({'result': 1, 'message': message})
        except Exception as e:
            print e
            return jsonify({'result': 0, 'message': e.message})
