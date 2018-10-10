from algorithms_base.no_process import NoProcHandler
from algorithms_contour.accurate_contour import AccurateContourHandler


def process(code, params, image):
    accurate_contour = AccurateContourHandler()
    no_proc_handler = NoProcHandler()

    accurate_contour.to_next(no_proc_handler)
    return accurate_contour.handle(code, params, image)
