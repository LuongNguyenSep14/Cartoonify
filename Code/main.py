"""Build application that cartoonify an input image"""
import os  # for OS interaction
import tkinter as tk
from tkinter import *
import cv2  # read image
import easygui  # to open the file box
from tkinter import messagebox

import matplotlib.pyplot as plt

"""
Step 2: Building a File Box to choose a particular file
"""


def upload():
    """
    use to choose a file
    and store a file path as string
    """
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


"""The above code opens the file box, i.e the pop-up box to choose the file from the device, which opens every time 
you run the code. fileopenbox() is the method in easyGUI module which returns the path of the chosen file as a string."""


def cartoonify(ImagePath):
    """
    this function is used to cartoonify an input image
    :param ImagePath:
    """
    # read an image
    originalImage = cv2.imread(ImagePath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
    w, h, c = originalImage.shape
    # confirm that image is chosen
    if originalImage is None:
        print("Can't find any Image. Choose appropriate file")
        sys.exit()
    resized1 = cv2.resize(originalImage, (w, h))

    # convert image into Gray Scale
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    resized2 = cv2.resize(grayImage, (w, h))

    # apply median blur to smoothen an image
    blurGrayImage = cv2.medianBlur(grayImage, 5)
    resized3 = cv2.resize(blurGrayImage, (w, h))

    # retrieve edge from blurGrayImage
    # by using threshold technique.
    edges = cv2.adaptiveThreshold(blurGrayImage, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    resized4 = cv2.resize(edges, (w, h))

    # apply bilateral filter to remove noise
    # and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalImage, 9, 300, 300)
    resized5 = cv2.resize(colorImage, (w, h))

    # masking edged image with our "bilateral Image"
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=edges)
    resized6 = cv2.resize(cartoonImage, (w, h))

    images = [originalImage, grayImage, blurGrayImage, edges, colorImage, cartoonImage]

    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(8, 8))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1 = Button(top, text='Save Cartoon Image', command=lambda: save(ImagePath, cartoonImage), padx=50, pady=5)
    save1.configure(bg='#364156', fg='white', font=('consolas', 10, 'bold'))
    save1.pack(side=BOTTOM, pady=50)
    plt.show()


"""
Functionally of save button
"""


def save(ImagePath, cartoonImage):
    """
    use to save image
    """
    # saving image using imwrite()
    newName = "cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName + extension)
    cv2.imwrite(path, cv2.cvtColor(cartoonImage, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName + " at " + path
    tk.messagebox.showinfo(message=I)


top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify your Image')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('consolas', 20, 'bold'))

upload1 = Button(top, text='Cartoonify an Image', command=upload, padx=50, pady=5)
upload1.configure(bg='#364156', foreground='white', font=('consolas', 10, 'bold'))
upload1.pack(side=TOP, pady=50)

top.mainloop()
