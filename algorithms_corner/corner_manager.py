from algorithms_base.no_process import NoProcHandler
from algorithms_corner.harris_corner import HarrisCornerHandler
from algorithms_corner.r_j_corner import RJCornerHandler


def process(code, params, image):
    harris_corner = HarrisCornerHandler()
    r_j_corner = RJCornerHandler()
    no_proc_handler = NoProcHandler()

    harris_corner.to_next(r_j_corner)
    r_j_corner.to_next(no_proc_handler)
    return harris_corner.handle(code, params, image)
