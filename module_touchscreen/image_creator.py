import os
import tkinter
from tkinter import *
from PIL import Image, ImageDraw, ImageTk

# Display on RPi
os.environ["DISPLAY"]=":0"

class ImageCreator():
    """
    The ImageCreator class serves different purposes:
    - creating a canvas
    - displaying an image on the canvas
    - resetting the canvas blank during an experiment
    - showing either a left or right or both rectangless
    """
    size_canvas = (800,480)
    rectangle_left = ((510, 0), (790, 300))
    rectangle_right = ((10, 0), (285, 300 ))
    saving_path = '/home/pi/Pictures/pillow_imagedraw.jpg'

    def __init__(self):
        self.root = tkinter.Tk() 
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.focus_set()    
        self.root.config(cursor="none")
        self.canvas = tkinter.Canvas(self.root,width=self.w,height=self.h)
        self.canvas.pack()
        self.canvas.configure(background='black')
    
    def showPIL(self, pilImage):
        """
        Function to show image in full display on Rpi.
        Input: 
            - pilImage: a JPG image used for the experiments
        """              

        self.canvas.delete("all")

        imgWidth, imgHeight = pilImage.size
        if imgWidth > self.w or imgHeight > self.h:
            ratio = min(self.w/imgWidth, self.h/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = self.canvas.create_image(self.w/2,self.h/2,image=image)

        self.root.update_idletasks()
        self.root.update()

        
    def show_left_and_right_rectangles(self):
        """
        This function allows the user to show both left and right rectangles on the canvas
        """
        im = Image.new(mode="RGB", size=ImageCreator.size_canvas, color=0)
        draw = ImageDraw.Draw(im)

        draw.rectangle(xy=ImageCreator.rectangle_left, fill=(255,255,255), outline=None)
        draw.rectangle(xy=ImageCreator.rectangle_right, fill=(255,255,255), outline=None)

        im.save(ImageCreator.saving_path, quality=100)
        pilImage = Image.open(ImageCreator.saving_path)
        self.showPIL(pilImage)

    def reset_canvas(self):
        """
        This function resets the canvas blank
        """
        im = Image.new(mode="RGB", size=ImageCreator.size_canvas, color=0)
        draw = ImageDraw.Draw(im)        
        im.save(ImageCreator.saving_path, quality=100)
        pilImage = Image.open(ImageCreator.saving_path)
        self.showPIL(pilImage)

    def show_left_rectangle(self):
        """
        This function shows the left rectangle only
        """
        im = Image.new(mode="RGB", size=ImageCreator.size_canvas, color=0)
        draw = ImageDraw.Draw(im)

        draw.rectangle(xy=ImageCreator.rectangle_left, fill=(255,255,255), outline=None)

        im.save(ImageCreator.saving_path, quality=100)
        pilImage = Image.open(ImageCreator.saving_path)
        self.showPIL(pilImage)

    def show_right_rectangle(self):
        """
        This function shows the right rectangle only
        """
        im = Image.new(mode="RGB", size=ImageCreator.size_canvas, color=0)
        draw = ImageDraw.Draw(im)

        draw.rectangle(xy=ImageCreator.rectangle_right, fill=(255,255,255), outline=None)

        im.save(ImageCreator.saving_path, quality=100)
        pilImage = Image.open(ImageCreator.saving_path)
        self.showPIL(pilImage)
