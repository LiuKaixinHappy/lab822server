import base64
import os

from smoth_algorithms.constant import ROOT_PATH
from smoth_algorithms.handler import Handler
from smoth_algorithms.proc_code_enum import ProcCodeEnum


class MeanBlurHandler(Handler):
    def handle(self, code, params, image):
        if code == ProcCodeEnum.MEAN_BLUR:
            pass
        else:
            self._to_next.handle(code, params, image)