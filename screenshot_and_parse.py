import cv2
import pyautogui
import numpy as np
import easyocr
import requests
from concurrent import futures
from pynput.keyboard import Listener
from pynput import keyboard
import logging


URL = "https://api.warframe.market/v1"


def preprocess_frame(frame):
    logging.debug("Preprocessing screenshot")
    frame = get_grayscale(frame)
    return frame


def canny(frame):
    logging.debug("Applying Canny filter to screenshot")
    frame = cv2.Canny(frame, 100, 200)
    return frame


def opening(frame):
    logging.debug("Applying opening effect to screenshot")
    kernel = np.ones((5, 5), np.uint8)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    return frame


def erosion(frame):
    logging.debug("Applying erosion effect to screenshot")
    kernel = np.ones((5, 5), np.uint8)
    frame = cv2.erode(frame, kernel, iterations=1)
    return frame


def dilate(frame):
    logging.debug("Applying dilation to screenshot")
    kernel = np.ones((5, 5), np.uint8)
    frame = cv2.dilate(frame, kernel, iterations=1)
    return frame


def thresholding(frame):
    logging.debug("Applying thresholding to screenshot")
    frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return frame


def remove_noise(frame):
    logging.debug("Removing noise from screenshot")
    frame = cv2.medianBlur(frame, 5)
    return frame


def get_grayscale(frame):
    logging.debug("Converting screenshot to grayscale")
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2GRAY)
    return frame


def run_easyocr(frame):
    logging.debug("Executing ocr on screenshot")
    reader = easyocr.Reader(['en'])
    output = reader.readtext(frame)
    return output


def get_price(item):
    logging.debug("Getting the price of {item}".format(item=item))
    market = query_market(item)
    if market.status_code == 200:
        market = market.json()['payload']['orders']
        ingame_orders = get_ingame_orders(market)
        order_price_and_quantities = extract_plat_and_quantity_from_order(ingame_orders)
        avg_price = print_average_price(item, order_price_and_quantities)
        return avg_price


def query_market(item):
    item = str.lower(item)
    item = str.replace(item, ' ', '_')
    get_text = '/items/{item}/orders'.format(item=item)
    full_url = URL + get_text
    headers = {'accept': 'application/json', 'Platform': 'pc'}
    logging.debug("Sending request to {url} along with {headers}".format(url=full_url, headers=headers))
    market = requests.get(url=full_url, headers=headers)
    logging.debug("Received {data}".format(data=market.status_code))
    return market


def get_ingame_orders(market):
    ingame_orders = []
    for order in market:
        if order["user"]["status"] == "ingame" and order["order_type"] == "sell":
            ingame_orders.append(order)
    return ingame_orders


def extract_plat_and_quantity_from_order(ingame_orders):
    order_price_and_quantities = []
    for order in ingame_orders:
        order_price_and_quantities.append((order['platinum'], order['quantity']))
    return order_price_and_quantities


def print_average_price(item, order_price_and_quantities):
    sum_plat = 0
    sum_quantity = 0
    for pair in order_price_and_quantities:
        price, quantity = pair
        sum_plat += price * quantity
        sum_quantity += quantity
    average_price = sum_plat / sum_quantity
    logging.debug("{item}: Average Price: {price}".format(item=item, price=average_price))
    return average_price


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
    frame = pyautogui.screenshot()
    frame = np.array(frame)
    #frame = cv2.imread("fissure_reward_2.jpg")
    x = len(frame[0])
    y = len(frame)
    frame = frame[y // 10:5 * y // 10, 0:x]
    frame = preprocess_frame(frame)
    words = run_easyocr(frame)
    prices = dict()
    for word in words:
        location, item, _ = word
        cv2.rectangle(frame, location[0], location[2], (255, 0, 0), 1)
        prices[item] = executor.submit(get_price, item)
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
