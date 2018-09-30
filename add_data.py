# -*- coding: utf-8 -*-
from mongoengine import *


connect('lab822')


class ImgType(Document):
    name = StringField(required=True)


class ImgParam(Document):
    type = StringField(required=True)
    name = StringField(required=True)
    value = ListField()
    limit = StringField()


class ImgOperation(Document):
    name = StringField(required=True)
    code = StringField(required=True)
    type = ListField(EmbeddedDocumentField('ImgType'))
    params = ListField(EmbeddedDocumentField('ImgParam'))


def insert():
    type1 = ImgType(name='图像平滑').save()
    type2 = ImgType(name='边缘检测').save()
    type3 = ImgType(name='轮廓提取').save()

    param1 = ImgParam(type='input', name='卷积核宽', value=[], limit='odd').save()
    param2 = ImgParam(type='input', name='卷积核高', value=[], limit='odd').save()
    param3 = ImgParam(type='input', name='水平方向标准差', value=[], limit='').save()
    param4 = ImgParam(type='input', name='垂直方向标准差', value=[], limit='').save()
    param5 = ImgParam(type='choice', name='边界扩充方式',
                      value=['边界复制', '常数扩充', '反射扩充', '边界为中心反射扩充', '平铺扩充'],
                      limit='').save()
    param6 = ImgParam(type='input', name='算子宽', value=[], limit='').save()
    param7 = ImgParam(type='input', name='算子高', value=[], limit='').save()
    param8 = ImgParam(type='input', name='锚点', value=[], limit='').save()
    param9 = ImgParam(type='input', name='窗口大小', value=[], limit='>1').save()
    param10 = ImgParam(type='input', name='权重模板宽', value=[], limit='').save()
    param11 = ImgParam(type='input', name='sigma color', value=[], limit='').save()
    param12 = ImgParam(type='input', name='sigma space', value=[], limit='').save()
    param13 = ImgParam(type='input', name='权重模板高', value=[], limit='').save()
    param14 = ImgParam(type='input', name='空间距离权重模板标准差', value=[], limit='').save()
    param15 = ImgParam(type='input', name='相似性权重模板标准差', value=[], limit='').save()

    operation1 = ImgOperation(name='高斯平滑', code='101', type=[type1],
                              params=[param1, param2, param3, param4, param5]).save()
    operation2 = ImgOperation(name='均值平滑', code='102', type=[type1],
                              params=[param6, param7, param8, param5]).save()


# insert()

o1s = list(ImgOperation.objects(type__name='图像平滑').exclude('id', 'name', 'code'))

for o1 in o1s:
    print o1.id
    print o1.name
    print o1.code

    for each in o1.type:
        print each.name

    for each in o1.params:
        print each.type
        print each.name
        print ','.join(each.value)
        print each.limit
        print '\n'
