import cv2
import numpy as np
import glob
import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

#inputs
root_image_folder = "./input_images"


def load_image(images_path):
    img_bgr = cv2.imread(images_path)
    input_blue, input_green,input_red = cv2.split(img_bgr)
    im_rgb = cv2.merge((input_red, input_green, input_blue))
    return im_rgb

def process_image(image_rgb, blue_threshold):
    #apply blue threshold
    input_red, input_green,input_blue = cv2.split(image_rgb)
    _, thresh_img = cv2.threshold(input_blue, blue_threshold, 255, cv2.THRESH_BINARY)

    #dilate picture
    kernal = np.ones((5, 5), np.uint8)
    img_erosion = cv2.erode(thresh_img, kernal, iterations=3)

    dilation_kernal = np.ones((2, 2), np.uint8)
    dilation_img = cv2.dilate(img_erosion, dilation_kernal, iterations=10)

    output_img_bw = dilation_img

    return output_img_bw

def count_blobs(img_bw):
    contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print("a")

    blob_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            if cv2.contourArea(contour) > 6500:
                if cv2.contourArea(contour) > 9000:
                    blob_count += 1
                blob_count += 1
            blob_count += 1
    return blob_count

def convert_to_tkinker_img(img_rgb, size_x, size_y):
    im = Image.fromarray(img_rgb)
    im = im.resize((size_x, size_y), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk

def update_output(input_img_rgb, output_img_bw, blob_count):
    global input_panel
    global output_panel
    global count_label

    input_img_tk = convert_to_tkinker_img(input_img_rgb, 500, 500)
    output_img_tk = convert_to_tkinker_img(output_img_bw, 500, 500)

    input_panel.configure(image=input_img_tk)
    input_panel.image = input_img_tk

    output_panel.configure(image=output_img_tk)
    output_panel.image = output_img_tk

    count_label.configure(text=blob_count)
    count_label.text = blob_count


def threshold_action():
    global cur_image_num
    global threshold_sv
    global image_paths

    blue_threshold = int(threshold_sv.get())

    input_img_rgb = load_image(image_paths[cur_image_num])
    output_img_bw = process_image(input_img_rgb, blue_threshold)
    blob_count = count_blobs(output_img_bw)
    update_output(input_img_rgb, output_img_bw, blob_count)

def next_image_action():
    global cur_image_num
    global image_paths
    global image_name
    global image_num

    cur_image_num += 1
    input_img_rgb = load_image(image_paths[cur_image_num])
    output_img_bw = process_image(input_img_rgb, 120)
    blob_count = count_blobs(output_img_bw)
    update_output(input_img_rgb, output_img_bw, blob_count)

    image_num.configure(text=str(cur_image_num))
    image_num.text = str(cur_image_num)

    cur_image_name = os.path.basename(image_paths[cur_image_num])
    image_name.configure(text=cur_image_name)
    image_name.text = cur_image_name

#init
#get absolute path to images from relative path
root_image_path = os.path.abspath(root_image_folder)
cur_image_num = 0

image_paths = glob.glob(root_image_path + "/*")

win = Tk()
win.title("Counter")
win.geometry("1000x700")

input_img_rgb = load_image(image_paths[cur_image_num])
output_img_bw = process_image(input_img_rgb, 100)
blob_count = count_blobs(output_img_bw)

input_img_tk = convert_to_tkinker_img(input_img_rgb, 500, 500)
output_img_tk = convert_to_tkinker_img(output_img_bw, 500, 500)

#display
input_panel = Label(win, image=input_img_tk)
input_panel.grid(row=0, column=0, padx=4, pady=4)

output_panel = Label(win, image=output_img_tk)
output_panel.grid(row=0, column=1, columnspan=2, padx=4, pady=4)

threshold_label = Label(win, text="Blue Threshold:")
threshold_label.grid(row=1, column=1, padx=4, pady=4, sticky=E)

threshold_sv = StringVar()
threshold_sv.set("120")
threshold_entry = Entry(win, textvariable=threshold_sv)
threshold_entry.grid(row=1, column=2, padx=4, pady=4, sticky=W)

count_label = Label(win, text="Cell Count: " + str(blob_count))
count_label.grid(row=2, column=1, columnspan=2, padx=4, pady=4)

image_num = Label(win, text="Image number: " + str(cur_image_num))
image_num.grid(row=2, column=0, padx=4, pady=4)

image_name = Label(win, text="Image name: " + os.path.basename(image_paths[cur_image_num]))
image_name.grid(row=3, column=0, padx=4, pady=4)

update_btn = Button(win, text="Refresh", command=threshold_action)
update_btn.grid(row=3, column=1, columnspan=2, padx=4, pady=4)

next_btn = Button(win, text="Next Image", command=next_image_action)
next_btn.grid(row=4, column=1, columnspan=2, padx=4, pady=4)
win.mainloop()