import os

ROOT_PATH = './static'
SWAGGER_PATH = os.path.join(os.path.dirname(os.path.abspath('lab822server')), 'swagger/swagger.yaml')


def get_root_path():
    return ROOT_PATH


def get_swagger_path():
    return SWAGGER_PATH
