from app import app
from flask import request, jsonify, url_for, render_template
from models.img_type import ImgType
from models.img_operations import ImgOperation
from flask_swagger import swagger


@app.route('/')
def a():
    return "Hello World"


@app.route('/static/swagger.yaml')
def swagger():
    return render_template('../static/swagger.yaml')


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
        operations = request.args.get('operations')
