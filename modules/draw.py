import cv2
import numpy as np

DEFAULT_FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
DEFAULT_FONT_SCALE = 1
DEFAULT_TEXT_COLOR = (255,255,0)
DEFAULT_FONT_WEIGHT = 1

def drawText(
    img: np.ndarray,
    text:str,
    location:list=[0,0],
    color:tuple=DEFAULT_TEXT_COLOR,
    fontWeight:int=DEFAULT_FONT_WEIGHT,
    fontScale:float=DEFAULT_FONT_SCALE,
    font=DEFAULT_FONT
    ):

    if location[0] < 0:
        location[0] = 0
    
    if location[1] < 0:
        location[1] = 0

    return cv2.putText(
        img,
        text,
        location,
        font,
        fontScale,
        color,
        fontWeight
    )
