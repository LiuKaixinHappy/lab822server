from algorithms_base.no_process import NoProcHandler
from algorithms_sigmentation.auto_threshold import AutoThresholdHandler


def process(code, params, image):
    auto_thresh = AutoThresholdHandler()
    no_proc_handler = NoProcHandler()

    auto_thresh.to_next(no_proc_handler)
    return auto_thresh.handle(code, params, image)
