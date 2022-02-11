import logging
import easyocr

class OCRRunner:

    def __init__(self):
        pass

    def run_ocr(self, img):
        return self.run_easyocr(img)

    def run_easyocr(self, frame):
        logging.debug("Executing ocr on screenshot")
        reader = easyocr.Reader(['en'])
        output = reader.readtext(frame)
        return output
