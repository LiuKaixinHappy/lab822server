# coding=utf-8
import cv2


# NOTE:顺序不可变
def get_thresh_type(index):
    thresh_type = [cv2.THRESH_BINARY,
                   cv2.THRESH_BINARY_INV,
                   cv2.THRESH_TRUNC,
                   cv2.THRESH_TOZERO,
                   cv2.THRESH_TOZERO_INV]
    return thresh_type[index]
