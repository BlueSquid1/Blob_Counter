import cv2
import numpy as np
import glob
import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

#inputs
root_image_folder = "./input_images"


#get absolute path to images from relative path
root_image_path = os.path.abspath(root_image_folder)

image_paths = glob.glob(root_image_path + "/*")

win = Tk()
win.title("Counter")
win.geometry("1000x700")

def load_image():
    pass

for image_num in range(len(image_paths)):
    image_path = image_paths[image_num]

    #load image
    print("opening image num: " + str(image_num) + " from path: " + image_path)
    img_bgr = cv2.imread(image_path)

    #apply blue threshold
    input_blue, input_green,input_red = cv2.split(img_bgr)
    _, thresh_img = cv2.threshold(input_blue, 210, 255, cv2.THRESH_BINARY)

    #dilate picture
    kernal = np.ones((2, 2), np.uint8)
    dilation_img = cv2.dilate(thresh_img, kernal, iterations=1)

    #count blobs
    contours, hierarchy = cv2.findContours(dilation_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blob_count = len(contours)

    #display images
    input_im_rgb = cv2.merge((input_red, input_green, input_blue))
    output_img_bw = dilation_img

    input_im = Image.fromarray(input_im_rgb)
    input_im = input_im.resize((500, 500), Image.ANTIALIAS)
    input_imgtk = ImageTk.PhotoImage(image=input_im)

    output_im = Image.fromarray(output_img_bw)
    output_im = output_im.resize((500, 500), Image.ANTIALIAS)
    output_imgtk = ImageTk.PhotoImage(image=output_im)

    input_panel = Label(win, image=input_imgtk)
    input_panel.grid(row=0, column=0, padx=4, pady=4)

    output_panel = Label(win, image=output_imgtk)
    output_panel.grid(row=0, column=1, columnspan=2, padx=4, pady=4)

    threshold_label = Label(win, text="Blue Threshold:")
    threshold_label.grid(row=1, column=1, padx=4, pady=4, sticky=E)

    threshold_entry = Entry(win)
    threshold_entry.grid(row=1, column=2, padx=4, pady=4, sticky=W)

    count_label = Label(win, text="Cell Count: " + str(blob_count))
    count_label.grid(row=2, column=1, columnspan=2, padx=4, pady=4)

btn = Button(win, text="Next Image", command=load_image)
btn.grid(row=3, column=1, columnspan=2, padx=4, pady=4)
win.mainloop()