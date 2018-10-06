import uuid


def get_unique_file_name():
    return '{}.jpg'.format(str(uuid.uuid4()))
