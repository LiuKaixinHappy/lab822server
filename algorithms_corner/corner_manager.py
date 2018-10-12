from algorithms_base.no_process import NoProcHandler
from algorithms_corner.harris_corner import HarrisCornerHandler


def process(code, params, image):
    harris_corner = HarrisCornerHandler()
    no_proc_handler = NoProcHandler()

    harris_corner.to_next(no_proc_handler)
    return harris_corner.handle(code, params, image)
