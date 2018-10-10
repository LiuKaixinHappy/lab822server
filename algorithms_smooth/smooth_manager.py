from algorithms_base.no_process import NoProcHandler
from algorithms_smooth.b_f_blur import BFBlurHandler
from algorithms_smooth.gaussian_blur import GaussianBlurHandler
from algorithms_smooth.joint_b_f_blur import JointBFBlurHandler
from algorithms_smooth.mean_blur import MeanBlurHandler
from algorithms_smooth.media_blur import MediaBlurHandler


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
