# imports
from tkinter import *  
from PIL import ImageTk,Image, ImageDraw 
import os
import tkinter
from PIL import Image, ImageTk

# Display on RPi
os.environ["DISPLAY"]=":0"

    # Function to show image with Pil and Tkinter in full display on Rpi
def showPIL(pilImage):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()
    
    
def create_and_show_image(size_canvas, rectangle_left,rectangle_right,saving_path):
    im = Image.new(mode="RGB", size=size_canvas, color=0)
    draw = ImageDraw.Draw(im)

    draw.rectangle(xy=rectangle_left, fill=(255,255,255), outline=None, width=2)
    draw.rectangle(xy=rectangle_right, fill=(255,255,255), outline=None, width=2)

    im.save(saving_path, quality=100)
    pilImage = Image.open(saving_path)
    showPIL(pilImage)

# Constant Variables
size_canvas = (1280,800)
rectangle_left = ((80, 0), (480, 400 ))
rectangle_right = ((800, 0), (1200, 400))
saving_path = '/home/pi/Pictures/pillow_imagedraw.jpg'

create_and_show_image(size_canvas,rectangle_left,rectangle_right,saving_path)