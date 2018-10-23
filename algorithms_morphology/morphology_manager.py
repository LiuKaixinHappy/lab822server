from algorithms_base.no_process import NoProcHandler
from algorithms_morphology.dilate import DilateHandler
from algorithms_morphology.erode import ErodeHandler


def process(code, params, image):
    erode_handler = ErodeHandler()
    dilate_handler = DilateHandler()
    no_proc_handler = NoProcHandler()

    erode_handler.to_next(dilate_handler)
    dilate_handler.to_next(no_proc_handler)
    return erode_handler.handle(code, params, image)
