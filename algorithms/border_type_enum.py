# coding=utf-8
import cv2


def get_border_type(index):
    border_types = [cv2.BORDER_REPLICATE,
                    cv2.BORDER_CONSTANT,
                    cv2.BORDER_REFLECT,
                    cv2.BORDER_REFLECT_101,
                    cv2.BORDER_WRAP]
    return border_types[index]
