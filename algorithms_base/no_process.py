# coding=utf-8
from algorithms_base.handler import Handler
from my_exceptions import ImageProcError


class NoProcHandler(Handler):
    def handle(self, code, params, image):
        raise ImageProcError('抱歉，图像处理方法尚未完成')
