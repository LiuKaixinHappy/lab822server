from algorithms_base.no_process import NoProcHandler
from algorithms_segmentation.adaptive_threshold import AdaptiveThresholdHandler
from algorithms_segmentation.auto_threshold import AutoThresholdHandler
from algorithms_segmentation.manual_threshold import ManualThresholdHandler


def process(code, params, image):
    auto_thresh = AutoThresholdHandler()
    manual_thresh = ManualThresholdHandler()
    adaptive_thresh = AdaptiveThresholdHandler()
    no_proc_handler = NoProcHandler()

    auto_thresh.to_next(manual_thresh)
    manual_thresh.to_next(adaptive_thresh)
    adaptive_thresh.to_next(no_proc_handler)

    return auto_thresh.handle(code, params, image)
