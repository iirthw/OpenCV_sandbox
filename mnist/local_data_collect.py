import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from PIL import Image, ImageDraw

class DataCollect:

    def __init__(self, stroke_size, canvas_width, canvas_height):
        self.stroke_size = stroke_size
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.last_x = 0
        self.last_y = 0
        self.canvas = None

        self.app = None

        # PIL image twin buffer that mirrors what is drawn on the canvas
        self.image_twin = None
        self.draw_twin = None

        # The twin image will be downscaled according to downscale_width and
        # downscale_height before adding that data to the pool for pickling.
        self.downscale_width = 28
        self.downscale_height = 28

        # constant used for on-demand increment and decrement of the stroke width.
        self.stroke_increment = 5
        self.stroke_min_size = 1
        self.stroke_max_size = max(self.canvas_width, self.canvas_height)

        self.black = (0, 0, 0)

    def get_xy(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw_stroke(self, event):
        top_left_point = (
            self.last_x - self.stroke_size,
            self.last_y - self.stroke_size
            )
        bottom_right_point = (
            self.last_x + self.stroke_size, 
            self.last_y + self.stroke_size
            )

        # Draw on the canvas
        self.canvas.create_oval(
            (top_left_point[0],
            top_left_point[1], 
            bottom_right_point[0], 
            bottom_right_point[1]),
            fill='white', outline = 'white',
            )

        self.last_x, self.last_y = event.x, event.y

        # Draw on the image twin
        self.draw_twin.ellipse([top_left_point, bottom_right_point], fill='white')

    def on_mouse_right_button(self, event):
        # In case if a single pixel is needed, use the following: 
        # pixel00 = self.image_twin.getpixel((0, 0))
        
        pixels = list(self.image_twin.getdata())

        im = self.image_twin
        im.thumbnail((self.downscale_width, self.downscale_height), Image.ANTIALIAS)
        plt.imshow(im)
        plt.show()

    def clear_canvas(self, event):
        print('clear_canvas')
        # Clear Tk canvas
        self.canvas.delete('all')
        # Clear Pillow image as well 
        self.image_twin = Image.new('RGB', 
            (self.canvas_width, self.canvas_height), self.black)
        self.draw_twin = ImageDraw.Draw(self.image_twin)

    def quit(self, event):
        self.app.quit()

    def decrement_stroke_size(self, event):
        temp = self.stroke_size - self.stroke_increment
        if temp < self.stroke_min_size:
            self.stroke_size = self.stroke_min_size
        else:
            self.stroke_size = temp
        
        print('decrement stroke size: ' + str(self.stroke_size))        

    def increment_stroke_size(self, event):
        temp = self.stroke_size + self.stroke_increment
        if temp > self.stroke_max_size:
            self.stroke_size = self.stroke_max_size
        else:
            self.stroke_size = temp
        
        print('increment stroke size: ' + str(self.stroke_size))

    def run(self):        
        self.image_twin = Image.new('RGB', 
            (self.canvas_width, self.canvas_height), self.black)
        self.draw_twin = ImageDraw.Draw(self.image_twin)

        self.app = Tk()
        self.app.geometry(str(self.canvas_width) + 'x' + str(self.canvas_height))

        self.canvas = Canvas(self.app, bg='black')
        self.canvas.pack(anchor='nw', fill='both', expand=1)        

        self.canvas.bind('<Button-1>', self.get_xy)
        # Button-3 corresponds to the right mouse button,
        # while Button-2 corresponds to the middle button if available,
        # that might be confusing if not reading the docs of tkinter.
        self.canvas.bind('<Button-3>', self.on_mouse_right_button)
        self.canvas.bind('<B1-Motion>', self.draw_stroke)

        self.app.bind('<space>', self.clear_canvas)
        self.app.bind('<q>', self.quit)
        self.app.bind('<Escape>', self.quit)
        self.app.bind('-', self.decrement_stroke_size)
        # Be careful with your keyboard layout to make sure you actually press
        # '+' key, rather than '=' for example, which both might share the 
        # same physical key on the keyboard.
        self.app.bind('+', self.increment_stroke_size)

        self.app.mainloop()
 
dc = DataCollect(stroke_size=16, canvas_width=200, canvas_height=200)
dc.run()