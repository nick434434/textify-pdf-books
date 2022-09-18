import numpy as np
import cv2
from imutils import rotate_bound


def resize_image(image: np.ndarray, h: int = None, w: int = None) -> np.ndarray:
    h0, w0 = image.shape[:2]
    if h is None and w is None:
        h = 1000
    if h is None:
        size = (w, int(round(h0 * w / w0)))
    if w is None:
        size = (int(round(w0 * h / h0)), h)
    return cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)


def show_image(window_name: str, image: np.ndarray, delay: int = 0) -> int:
    cv2.imshow(window_name, image)
    return cv2.waitKey(delay)


def divide_page(page_image: np.ndarray):
    h = page_image.shape[0]
    return page_image[:h//2, :], page_image[h//2:, :]


def rotate_image(image: np.ndarray, angle: int = 90) -> np.ndarray:
    return rotate_bound(image, angle)


def preprocess(image: np.ndarray) -> np.ndarray:
    """
    Take an image with text (supposedly written in one main direction) and apply improvements before running tesseract
    :param image: scanned PDF page image with text
    :return: improved image for tesseract
    """
    processed = image.copy()
    if len(processed.shape) > 2:
        processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

    processed = rotate_image(processed, 90)
    processed = cv2.threshold(processed, 175, 255, cv2.THRESH_BINARY)[-1]
    # processed = cv2.adaptiveThreshold(processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return processed
