from pytesseract import image_to_string, image_to_data, image_to_boxes, image_to_osd, Output
import numpy as np


DEFAULT_LANGUAGE = 'rus'


def read_boxes(img: np.ndarray, language: str = DEFAULT_LANGUAGE) -> dict:
    boxes = image_to_boxes(img, lang=language, output_type=Output.DICT)
    return boxes


def read_raw_text(img: np.ndarray, language: str = DEFAULT_LANGUAGE) -> dict:
    text = image_to_string(img, lang=language, output_type=Output.STRING)
    return text
