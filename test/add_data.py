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
    pName = StringField()


class ImgOperation(Document):
    name = StringField(required=True)
    code = StringField(required=True)
    type = ListField(EmbeddedDocumentField('ImgType'))
    params = ListField(EmbeddedDocumentField('ImgParam'))


def insert_old():
    type1 = ImgType(name='图像平滑').save()

    param1 = ImgParam(type='input', name='卷积核宽', value=[], limit='odd', pName='kSizeW')
    param2 = ImgParam(type='input', name='卷积核高', value=[], limit='odd', pName='kSizeH')
    param3 = ImgParam(type='input', name='水平方向标准差', value=[], limit='', pName='sigmaX')
    param4 = ImgParam(type='input', name='垂直方向标准差', value=[], limit='', pName='sigmaY')
    param5 = ImgParam(type='select', name='边界扩充方式',
                      value=['边界复制', '常数扩充', '反射扩充', '边界为中心反射扩充', '平铺扩充'],
                      limit='', pName='borderType')
    param6 = ImgParam(type='input', name='算子宽', value=[], limit='odd', pName='kSizeW')
    param7 = ImgParam(type='input', name='算子高', value=[], limit='odd', pName='kSizeH')
    param9 = ImgParam(type='input', name='窗口大小', value=[], limit='odd >1', pName='kSize')
    param10 = ImgParam(type='input', name='滤波像素邻域直径', value=[], limit='', pName='d')
    param11 = ImgParam(type='input', name='sigma color', value=[], limit='', pName='sigmaColor')
    param12 = ImgParam(type='input', name='sigma space', value=[], limit='', pName='sigmaSpace')
    param8 = ImgParam(type='input', name='权重模板宽', value=[], limit='odd', pName='kSizeW')
    param13 = ImgParam(type='input', name='权重模板高', value=[], limit='odd', pName='kSizeH')
    param14 = ImgParam(type='input', name='空间距离权重模板标准差', value=[], limit='int <5', pName='sigmaG')
    param15 = ImgParam(type='input', name='相似性权重模板标准差', value=[], limit='', pName='sigmaD')

    operation1 = ImgOperation(name='高斯平滑', code='101', type=[type1],
                              params=[param1, param2, param3, param4, param5]).save()
    operation2 = ImgOperation(name='均值平滑', code='102', type=[type1],
                              params=[param6, param7, param5]).save()
    operation3 = ImgOperation(name='中值平滑', code='103', type=[type1],
                              params=[param9]).save()
    operation4 = ImgOperation(name='双边滤波', code='104', type=[type1],
                              params=[param10, param11, param12, param5]).save()
    operation5 = ImgOperation(name='联合双边滤波', code='105', type=[type1],
                              params=[param8, param13, param14, param15, param5]).save()


def insert_old2():
    type2 = ImgType(name='阈值分割').save()

    param16 = ImgParam(type='input', name='二值化最大值', value=[], limit='int >-1 <256', pName='maxVal')
    param17 = ImgParam(type='select', name='分割类型',
                       value=['THRESH_BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO',
                              'THRESH_TOZERO_INV'], limit='', pName='threshType')
    param18 = ImgParam(type='select', name='自动计算阈值算法',
                       value=['Otsu', 'Triangle', '熵算法', '直方图'], limit='', pName='findThreshType')

    operation5 = ImgOperation(name='自动分割', code='201', type=[type2],
                              params=[param16, param17, param18]).save()
    param16 = ImgParam(type='input', name='二值化最大值', value=[], limit='int >-1 <256', pName='maxVal')
    param9 = ImgParam(type='input', name='窗口大小', value=[], limit='odd >1', pName='kSize')
    param17 = ImgParam(type='select', name='分割类型',
                       value=['THRESH_BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO',
                              'THRESH_TOZERO_INV'], limit='', pName='threshType')
    param23 = ImgParam(type='input', name='阈值', value=[], limit='int', pName='thresh')

    operation7 = ImgOperation(name='手动分割', code='202', type=[type2],
                              params=[param16, param23, param17]).save()

    param24 = ImgParam(type='input', name='ratio', value=[], limit='>0 <1', pName='ratio')
    operation8 = ImgOperation(name='局部分割', code='203', type=[type2],
                              params=[param9, param24]).save()


def insert_old3():
    type3 = ImgType(name='轮廓提取').save()
    param19 = ImgParam(type='input', name='轮廓线宽度', value=[], limit='int >0', pName='contourWidth')
    param20 = ImgParam(type='select', name='检测模式',
                       value=['最外围轮廓', '所有轮廓(无等级)', '所有轮廓(两个等级)', '所有轮廓(等级树)'],
                       limit='', pName='mode')
    param21 = ImgParam(type='select', name='近似方法',
                       value=['保留所有轮廓', '仅保留拐点', 'Teh-Chin-L1', 'Teh-Chin-KCOS'],
                       limit='', pName='method')
    param22 = ImgParam(type='select', name='二值化后物体颜色',
                       value=['黑色', '白色'],
                       limit='', pName='binaryObjectColor')

    param29 = ImgParam(type='select', name='输出图片类型',
                       value=['原图+轮廓', '轮廓'],
                       limit='', pName='outputType')

    operation6 = ImgOperation(name='精确轮廓', code='301', type=[type3],
                              params=[param19, param22, param20, param21, param29]).save()


def insert():
    type4 = ImgType(name='角点检测').save()
    param25 = ImgParam(type='input', name='邻域大小', value=[], limit='int', pName='blockSize')
    param26 = ImgParam(type='input', name='窗口大小', value=[], limit='odd', pName='kSize')
    param27 = ImgParam(type='input', name='Harris自由参数', value=[], limit='', pName='k')
    param28 = ImgParam(type='input', name='角点判定阈值', value=[], limit='', pName='threshold')

    operation9 = ImgOperation(name='Harries', code='401', type=[type4],
                              params=[param25, param26, param27, param28]).save()

    param30 = ImgParam(type='input', name='平滑因子', value=[], limit='>0 <1', pName='mFactor')

    operation10 = ImgOperation(name='RJ算法', code='403', type=[type4],
                               params=[param30]).save()


insert_old()
insert_old2()
insert_old3()
insert()

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
