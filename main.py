import numpy as np
import matplotlib.pyplot as plt
import cv2
import easygui
import imageio
import os
import tkinter as tk
from PIL import Image, ImageTk
import sys


def cartoonify(ImagePath):
    # read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    # print(originalmage)  # image is stored in form of numbers

    # Code to retain shape of original image of readability
    h, w, _ = originalmage.shape
    size = (h, w)

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, size)
    plt.imshow(ReSized1, cmap='gray')

    # converting an image to grayscale
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, size)
    plt.imshow(ReSized2, cmap='gray')

    # applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, size)
    plt.imshow(ReSized3, cmap='gray')

    # retrieving the edges for cartoon effect
    # by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 9)
    ReSized4 = cv2.resize(getEdge, size)
    plt.imshow(ReSized4, cmap='gray')

    # applying bilateral filter to remove noise
    # and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, size)
    plt.imshow(ReSized5, cmap='gray')

    # masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, size)
    plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.show()


""" fileopenbox opens the box to choose file
and help us store file path as string """


def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


upload()
