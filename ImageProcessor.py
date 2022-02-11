import cv2
import logging
import numpy as np
import pyautogui


class ImageProcessor:

    def __init__(self):
        pass

    def get_image(self, file_name):
        return cv2.imread(file_name)

    def canny(self, frame):
        logging.debug("Applying Canny filter to screenshot")
        frame = cv2.Canny(frame, 100, 200)
        return frame

    def opening(self, frame):
        logging.debug("Applying opening effect to screenshot")
        kernel = np.ones((5, 5), np.uint8)
        frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        return frame

    def erosion(self, frame):
        logging.debug("Applying erosion effect to screenshot")
        kernel = np.ones((5, 5), np.uint8)
        frame = cv2.erode(frame, kernel, iterations=1)
        return frame

    def dilate(self, frame):
        logging.debug("Applying dilation to screenshot")
        kernel = np.ones((5, 5), np.uint8)
        frame = cv2.dilate(frame, kernel, iterations=1)
        return frame

    def thresholding(self, frame):
        logging.debug("Applying thresholding to screenshot")
        frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return frame

    def remove_noise(self, frame):
        logging.debug("Removing noise from screenshot")
        frame = cv2.medianBlur(frame, 5)
        return frame

    def get_grayscale(self, frame):
        logging.debug("Converting screenshot to grayscale")
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2GRAY)
        return frame

    def find_squares(self, img):
        #blurred = cv2.medianBlur(img, 5)
        #cv2.imshow("blurred", blurred)
        sharpened = cv2.bilateralFilter(img, 5, 50, 50)
        cv2.imshow("sharpened", sharpened)
        noisless = remove_noise(sharpened)
        cv2.imshow("noiseless", noisless)
        threshold = thresholding(sharpened)
        cv2.imshow("threshold", threshold)

    def enhance_contrast(self, img, alpha, beta):
        new_img = np.zeros(img.shape, img.dtype)
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for c in range(img.shape[2]):
                    new_img[y, x, c] = np.clip(alpha * img[y, x, c] + beta, 0, 255)
        return new_img

    def resize(self, img, new_x, new_y):
        return cv2.resize(img, (new_x, new_y))

    def crop(self, frame):
        x = len(frame[0])
        y = len(frame)
        frame = frame[y // 10:5 * y // 10, 0:x]
        return frame

    def take_screenshot(self):
        frame = pyautogui.screenshot()
        frame = np.array(frame)
        return frame