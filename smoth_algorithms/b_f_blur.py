import base64
import os

from smoth_algorithms.constant import ROOT_PATH
from smoth_algorithms.handler import Handler
from smoth_algorithms.proc_code_enum import ProcCodeEnum


class BFBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.B_F_BLUR:
            pass
        else:
            return self._to_next.handle(code, params, image)
