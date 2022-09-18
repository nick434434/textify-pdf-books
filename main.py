from imagify_pdf import pages, page_to_image

from image_processing import preprocess, divide_page, show_image, resize_image

from textify import read_boxes, read_raw_text


def get_pages_texts(processor):
    processor.send(None)
    for page in pages("manual.pdf"):
        page_img = page_to_image(page)
        top, bottom = divide_page(page_img)

        processor.send(read_raw_text(preprocess(bottom)))

        processor.send(read_raw_text(preprocess(top)))
        # show_image("top preprocessed", resize_image(ready))


def writer(filename: str):
    page_num = 1
    with open(filename, "w") as f:
        while True:
            text = (yield)
            f.write(f"*****\nPage {page_num}\n*****\n\n")
            f.write(text)
            page_num += 1


if __name__ == '__main__':
    get_pages_texts(writer("v1.txt"))
