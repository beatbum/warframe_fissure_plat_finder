import cv2
from concurrent import futures
from pynput.keyboard import Listener
from pynput import keyboard
import logging

from ImageProcessor import ImageProcessor
from OCRRunner import OCRRunner
from MarketInterface import MarketInterface

image_processor = ImageProcessor()
ocr_runner = OCRRunner()
market = MarketInterface()


def preprocess_frame(frame):
    logging.debug("Preprocessing screenshot")
    frame = image_processor.get_grayscale(frame)
    return frame


def main(key):
    try:
        if key == keyboard.Key.page_down:
            print("entering main loop")
            prices = main_logic()
            for item in prices:
                price = prices[item].result()
                if price is not None:
                    print("{item}: {price}".format(item=item, price=price))
    except AttributeError:
        print(key)


def main_logic():
    print("entering main_logic")
    executor = futures.ThreadPoolExecutor(max_workers=8)
    # frame = image_processor.take_screenshot()
    frame = image_processor.get_image("tests/fissure_reward_2.jpg")
    # frame = image_processor.resize(frame, 1920, 1080)
    frame = image_processor.crop(frame)
    frame = preprocess_frame(frame)
    words = ocr_runner.run_ocr(frame)
    prices = dict()
    for word in words:
        location, item, _ = word
        cv2.rectangle(frame, location[0], location[2], (255, 0, 0), 1)
        prices[item] = executor.submit(market.get_price, item)
    futures.wait(prices.values())
    # cv2.imshow('frame', frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return prices


if __name__ == '__main__':
    with Listener(on_press=main) as listener:
        print("started")
        while True:
            listener.join()
