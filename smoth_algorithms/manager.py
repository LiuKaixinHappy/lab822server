from smoth_algorithms.no_process import NoProcHandler
from smoth_algorithms.b_f_blur import BFBlurHandler
from smoth_algorithms.gaussian_blur import GaussianBlurHandler
from smoth_algorithms.joint_b_f_blur import JointBFBlurHandler
from smoth_algorithms.mean_blur import MeanBlurHandler
from smoth_algorithms.media_blur import MediaBlurHandler


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
