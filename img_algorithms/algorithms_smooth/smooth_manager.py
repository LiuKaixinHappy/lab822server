from img_algorithms.algorithms_base import NoProcHandler
from img_algorithms.algorithms_smooth import BFBlurHandler
from img_algorithms.algorithms_smooth import GaussianBlurHandler
from img_algorithms.algorithms_smooth import JointBFBlurHandler
from img_algorithms.algorithms_smooth import MeanBlurHandler
from img_algorithms.algorithms_smooth import MediaBlurHandler


def process(code, params, image):
    gaussian_blur = GaussianBlurHandler()
    mean_blur = MeanBlurHandler()
    media_blur = MediaBlurHandler()
    b_f_blur = BFBlurHandler()
    joint_b_f_blur = JointBFBlurHandler()
    no_proc_handler = NoProcHandler()

    gaussian_blur.to_next(mean_blur)
    mean_blur.to_next(media_blur)
    media_blur.to_next(b_f_blur)
    b_f_blur.to_next(joint_b_f_blur)
    joint_b_f_blur.to_next(no_proc_handler)

    return gaussian_blur.handle(code, params, image)
