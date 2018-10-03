# coding=utf-8


def get_border_type(chinese):
    border_types = dict({'边界复制': 'BORDER_REPLICATE',
                         '常数扩充': 'BORDER_CONSTANT',
                         '反射扩充': 'BORDER_REFLECT',
                         '边界为中心反射扩充': 'BORDER_REFLECT_101',
                         '平铺扩充': 'BORDER_WRAP'})
    return border_types[chinese]
