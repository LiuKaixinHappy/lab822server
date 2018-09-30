from app import app
from flask import request, jsonify
from models.img_type import ImgType
from models.img_operations import ImgOperation


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
        pass
