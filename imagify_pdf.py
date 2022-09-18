from pathlib import Path

import numpy as np
import PyPDF2
from PIL import Image
import cv2


def page_to_image(page: PyPDF2.PageObject) -> np.ndarray:
    """
    Extracts image from single-image PDF page
    :param page: page from PyPDF2.PdfReader
    :return: np.ndarray image
    """
    x_object = page["/Resources"]["/XObject"].getObject()

    for obj in x_object:
        if x_object[obj]["/Subtype"] == "/Image":
            size = (x_object[obj]["/Width"], x_object[obj]["/Height"])
            data = x_object[obj].getData()
            if x_object[obj]["/ColorSpace"] == "/DeviceRGB":
                mode = "RGB"
            else:
                mode = "P"

            if x_object[obj]["/Filter"] == "/FlateDecode":
                img = Image.frombytes(mode, size, data)
                img.save(obj[1:] + ".png")
                return cv2.imread(obj[1:] + ".png")
            elif x_object[obj]["/Filter"] == "/DCTDecode":
                img = open(obj[1:] + ".jpg", "wb")
                img.write(data)
                img.close()
                return cv2.imread(obj[1:] + ".jpg")
            elif x_object[obj]["/Filter"] == "/JPXDecode":
                img = open(obj[1:] + ".jp2", "wb")
                img.write(data)
                img.close()
                return cv2.imread(obj[1:] + ".jp2")

    raise NotImplementedError


def pages(filename: str):
    reader = PyPDF2.PdfReader(Path(filename))
    num_pages = reader.getNumPages()
    for page in range(num_pages):
        yield reader.getPage(page)
