from img_algorithms.algorithms_base import NoProcHandler
from img_algorithms.algorithms_segmentation import AdaptiveThresholdHandler
from img_algorithms.algorithms_segmentation import AutoThresholdHandler
from img_algorithms.algorithms_segmentation import ManualThresholdHandler


def process(code, params, image):
    auto_thresh = AutoThresholdHandler()
    manual_thresh = ManualThresholdHandler()
    adaptive_thresh = AdaptiveThresholdHandler()
    no_proc_handler = NoProcHandler()

    auto_thresh.to_next(manual_thresh)
    manual_thresh.to_next(adaptive_thresh)
    adaptive_thresh.to_next(no_proc_handler)

    return auto_thresh.handle(code, params, image)
