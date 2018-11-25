from img_algorithms.algorithms_base import NoProcHandler
from img_algorithms.algorithms_contour import AccurateContourHandler


def process(code, params, image):
    accurate_contour = AccurateContourHandler()
    no_proc_handler = NoProcHandler()

    accurate_contour.to_next(no_proc_handler)
    return accurate_contour.handle(code, params, image)
