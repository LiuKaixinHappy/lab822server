# coding=utf-8
from img_algorithms.algorithms_base.handler import Handler


class NoProcHandler(Handler):
    def handle(self, code, params, image):
        raise Exception('哎呀～{}号图像处理方法尚未完成，请静候佳音'.format(code))
