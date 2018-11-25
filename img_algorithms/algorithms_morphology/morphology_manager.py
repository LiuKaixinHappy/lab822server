from img_algorithms.algorithms_base import NoProcHandler
from img_algorithms.algorithms_morphology import DilateHandler
from img_algorithms.algorithms_morphology import ErodeHandler
from img_algorithms.algorithms_morphology import MorphOperationsCalHandler


def process(code, params, image):
    erode_handler = ErodeHandler()
    dilate_handler = DilateHandler()
    morph_operations_cal_handler = MorphOperationsCalHandler()
    no_proc_handler = NoProcHandler()

    erode_handler.to_next(dilate_handler)
    dilate_handler.to_next(morph_operations_cal_handler)
    morph_operations_cal_handler.to_next(no_proc_handler)
    return erode_handler.handle(code, params, image)
