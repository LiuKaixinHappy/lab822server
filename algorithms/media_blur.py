import base64
import os

from algorithms.constant import ROOT_PATH
from algorithms.handler import Handler
from algorithms.proc_code_enum import ProcCodeEnum


class MediaBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.MEDIA_BLUR:
            pass
        else:
            self._to_next.handle(code, params, image)
