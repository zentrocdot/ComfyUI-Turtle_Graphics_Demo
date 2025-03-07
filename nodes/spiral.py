#!/usr/bin/python
'''Simple Turtle Graphics demo(nstrator).'''
# pylint: disable=invalid-name
# pylint: disable=bare-except
# pylint: disable=broad-exception-caught
# pylint: disable=no-member
# pylint: disable=too-many-positional-arguments
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=protected-access
# pylint: disable=too-many-lines
# pylint: disable=unused-variable

# Import the standard Python modules.
import tkinter as tk
import re
import hashlib
import pathlib
import time
import turtle
from io import BytesIO
from datetime import datetime
import traceback
from tkinter import messagebox

# Import the third party Python modules.
import torch
import webcolors
import cv2
import numpy as np
from PIL import Image

# Set some paths.
SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
PARENT_PATH = SCRIPT_PATH.parent.absolute()
IMAGE_PATH = ''.join([str(PARENT_PATH), "/images"])
SPLASH_PATH = ''.join([str(PARENT_PATH), "/images/splash2.gif"])
CUSTOM_NODES_PATH = pathlib.Path(PARENT_PATH).parent.resolve()
COMFYUI_PATH = pathlib.Path(CUSTOM_NODES_PATH).parent.resolve()
OUTPUT_PATH = ''.join([str(COMFYUI_PATH), "/output"])

# Set some constants.
TURTLE_TITLE = "Object-Oriented Turtle Demo"

# Set the shape of the turtle.
TURTLE = ['turtle', 'arrow', 'blank', 'circle', 'classic', 'square', 'triangle']

# Define the resize sampler.
RESIZE_SAMPLER = {"LANCZOS": 1, "BICUBIC": 3, "BILINEAR": 2,
                  "BOX": 4, "HAMMING": 5, "NEAREST": 0}
KEYS = list(RESIZE_SAMPLER.keys())

# Set message flag.
MSG_FLAG = False

# -------------------
# Class Error Window.
# -------------------
class ErrWin:
    '''Err win class.'''
    def __init__(self, error_message):
        err_win = tk.Tk()
        err_win.withdraw()
        err_win.option_add('*Dialog.msg.font', 'Helvetica 12 bold')
        err_win.option_add('*Dialog.msg.width', 20)
        err_win.option_add("*Dialog.msg.wrapLength", "6i")
        messagebox.showerror("ERROR", "\n" + error_message)
        err_win.destroy()

# ------------------
# Class Info Window.
# ------------------
class InfWin():
    '''Inf win class.'''
    def __init__(self, info_message):
        inf_win = tk.Tk()
        inf_win.option_add('*Dialog.msg.font', 'Helvetica 12 bold')
        inf_win.option_add('*Dialog.msg.width', 20)
        inf_win.option_add("*Dialog.msg.wrapLength", "6i")
        inf_win.overrideredirect(1)
        inf_win.withdraw()
        messagebox.showinfo("INFO", info_message)
        inf_win.destroy()

# ----------------------
# Function Error Window.
# ----------------------
def error(message, title="ERROR"):
    '''Error function.'''
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()

# ---------------------
# Function Info Window.
# ---------------------
def info(message, title="INFO"):#
    '''Info function.'''
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

# ***************************
# Function get function name.
# ***************************
def get_function_name(func):
    '''Get the name of a function.'''
    # Get the name of the function.
    return func.__name__

# -----------------
# Function save_eps
# -----------------
def save_eps(turtle, EPS_PATH, screen_x, screen_y):
    '''Save eps file.'''
    # Get the screen canvas.
    canvas = turtle.getscreen()
    # Save the eps image.
    ps_width = screen_x
    ps_height = screen_y
    ps_x = -int(screen_x/2)
    ps_y = -int(screen_y/2)
    ps_pw = screen_x
    ps_ph = screen_y
    canvas.getcanvas().postscript(file=EPS_PATH, x=ps_x, y=ps_y,
                                  width=ps_width, height=ps_height,
                                  pagewidth=ps_pw, pageheight=ps_ph)
    # Return None.
    return None

# -----------------
# Function save_png
# -----------------
def save_png(EPS_PATH, PNG_PATH, width, height, resize_sampler):
    '''Save png file.'''
    # Set the target bounds.
    target_bounds = (width, height)
    # Load the image and scale the image.
    scale = 10
    new_img = Image.open(EPS_PATH)
    new_img.load(scale=scale)
    # Check color type of image.
    if new_img.mode in ('P', '1'):
        new_img = new_img.convert("RGB")
    pad = int(scale * 1 * 1.4)
    cx, cy = new_img.size
    new_img = new_img.crop((0,pad,cx-pad,cy-0))
    # Calculate the aspect ratio of the image.
    aspect_ratio = min(target_bounds[0] / new_img.size[0],
                       target_bounds[1] / new_img.size[1])
    # Calculate the new size.
    new_size = (int(new_img.size[0] * aspect_ratio),
                int(new_img.size[1] * aspect_ratio))
    # Resize the image.
    resize_sampler = RESIZE_SAMPLER[resize_sampler]
    pil_image = new_img.resize(new_size, resample=resize_sampler)
    # Save the image.
    pil_image.save(PNG_PATH)
    # Return None.
    return pil_image

# ******************
# Create color list.
# ******************
def create_color_list(fg_color):
    '''Create color list.'''
    # Create a fg color list.
    stripString = str(fg_color).strip()
    fg_color = stripString.split(",")
    fg_color = [x.strip(' ') for x in fg_color]
    return fg_color

# **********************
# Remove color function.
# **********************
def remove_color(src):
    '''Remove color.'''
    # Convert image to grayscale.
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(src)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 4)
    # Return destination.
    return dst

# ***********************
# Replace color function.
# ***********************
def replace_color(image, replacement_color):
    '''Replace color.'''
    # Set the original color.
    original_col = (255, 255, 255)
    # Determine color tuple.
    replace_col = color_to_rgb(replacement_color)
    # Replace original color with replacement color.
    image[(image == original_col).all(axis = -1)] = replace_col
    # Return new image.
    return image

# *************
# Color to rgb.
# *************
def color_to_rgb(color):
    '''Color to rgb.'''
    # Check input color type.
    if color is None or isinstance(color, (list, tuple)):
        rgb = color
    elif re.match('#', color):
        rgb = webcolors.hex_to_rgb(color)
    else:
        rgb = webcolors.name_to_rgb(color)
    # Get the components of the color.
    r,g,b = rgb[0], rgb[1], rgb[2]
    # Return the RGB color tuple.
    return r,g,b

# ***********************
# Function string2tuple()
# ***********************
def string2tuple(color_string):
    '''String to tuple function.'''
    # Initialise the color tuple.
    color_tuple = (64,64,64)
    # Try to create a color tuple.
    try:
        stripString = str(color_string).replace('(','').replace(')','').strip()
        rgb = stripString.split(",")
        r, g, b = int(rgb[0].strip()), int(rgb[1].strip()), int(rgb[2].strip())
        color_tuple = (r, g, b)
    except:
        print("ERROR. Could not create color tuple!")
        color_tuple = (128,128,128)
    # Return the color tuple
    return color_tuple

# *****************
# Resize Pil image.
# *****************
def resize_pil_image(image, width, height, sampler):
    '''Resize Pil image.'''
    h, w, c = image.shape
    #print("Dimensions:", h, w, c)
    if h == height and w == width:
        # Print message.
        print("Image not upscaled ...")
        # Return the image.
        return image
    # Numpy array to Pil image.
    image = Image.fromarray(image)
    # Resize Pil image.
    pil_image = image.resize((width, height), resample=sampler)
    # Pil image to Numpy array.
    image = np.array(pil_image)
    # Return Image.
    return image

# --------------------
# Make image function.
# --------------------
def make_image(text, wx=10, hy=256):
    '''Make a new image.'''
    # Set rows and cols.
    n, m = 512, 512
    # Create an empty image.
    image = np.zeros([n,m,3], dtype=np.uint8)
    # Add text to the image
    position = (wx, hy)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 0, 255)
    thickness = 2
    cv2.putText(image, text, position, font, font_scale,
                color, thickness, cv2.LINE_AA)
    # Return the image.
    return image

# -----------------------
# Tensor to PIL function.
# -----------------------
def tensor2pil(image):
    '''Tensor to PIL image.'''
    # Return PIL image.
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# -------------------------------
# Convert PIL to Tensor function.
# -------------------------------
def pil2tensor(image):
    '''PIL image to tensor.'''
    # Return tensor.
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

COLOR_STRING = ["lightcyan", "cyan", "yellow", "gold", "orange", "red",
          "firebrick", "violet", "magenta", "springgreen", "green",
          "blue", "midnightblue"]

# *******************************************
# Class TurtleGraphicsSpiralColorStandardDemo
# *******************************************
class TurtleGraphicsSpiralColorStandardDemo:
    '''Create a Turtle Graphics circle demo.'''

    def __init__(self):
        '''Class __init__ function.'''
        self.screen_x = 512
        self.screen_y = 512
        self.quit = False
        self.sc = turtle.Screen()
        self.sc.setup(self.screen_x, self.screen_y)
        self.sc.bgpic(SPLASH_PATH)
        self.sc.title("Splash Screen Turtle Graphics")
        self.root = turtle.getscreen()._root
        #self.style = ttk.Style(self.root)
        #self.style.configure("classic")
        self.root.option_add('*Dialog.msg.font', 'Helvetica 12 bold')
        self.root.option_add('*Dialog.msg.width', 32)
        self.root.option_add("*Dialog.msg.wrapLength", "6i")
        self.root.protocol("WM_DELETE_WINDOW", self.root.update)
        self.root.bind('<Escape>', self.quit_loop)
        #self.root.bind("<KeyRelease>", self.key)

    def key(self, event):
        '''Key bind test function.'''
        print(event.keysym)

    def quit_loop(self, *args, **kwargs):
        '''Close windows handler.'''
        self.quit = True
        print("You try to interrupt the Turtle Graphics drawing!")

    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        '''Class method IS_CHNAGED.'''
        m = hashlib.sha256()
        bytes_string = str(time.time()).encode("utf-8")
        m.update(bytes_string)
        return m.digest().hex()

    @classmethod
    def INPUT_TYPES(cls):
        '''Define the input types.'''
        return {
            "required": {
                "thickness": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100000.0, "step": 0.1}),
                "turtle_speed": ("INT", {"default": 0, "min": 0, "max": 10}),
                "max_length": ("INT", {"default": 800, "min": 1, "max": 100000}),
                "scale_factor": ("FLOAT", {"default": 0.3, "min": 0.1, "max": 2048.0}),
                "increment_pen": ("FLOAT", {"default": 0.0001, "min": 0.0, "max": 2048.0, "step": 0.0001}),
                "angle": ("INT", {"default": 59, "min": 1, "max": 2048}),
                "start_angle": ("INT", {"default": 0, "min": 0, "max": 2048}),
                "shape": (TURTLE, {}),
                "hide_turtle": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "fill_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "bg_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "bg_color": ("STRING", {"multiline": False, "default": "black"}),
                "replace_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "remove_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "fg_color": ("STRING", {"multiline": True, "default": COLOR_STRING}),
                "pen_color": ("STRING", {"multiline": False, "default": "red"}),
                "fill_color": ("STRING", {"multiline": False, "default": "blue"}),
                "replacement_color": ("STRING", {"multiline": False, "default": "black"}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "resize_sampler": (KEYS, {}),
                "screen_x": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_y": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_color": ("STRING", {"multiline": False, "default": "aquamarine"}),
                "withdraw_window": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
            },
            "optional": {
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "turtle_graphics_main"
    CATEGORY = "🐢 Turtle Graphics/🌀 Spiral Color Demo"
    OUTPUT_NODE = True

    def demo(self, thickness, turtle_speed, shape, max_length, hide_turtle,
             screen_color, fg_color, screen_x, screen_y, fill_on_off,
             fill_color, pen_color, angle, withdraw_window, start_angle,
             scale_factor, width, height, resize_sampler, bg_on_off, bg_color, increment_pen):
        '''Create a simple Turtle Graphics Demo.'''
        # Reset quit flag.
        self.quit = False
        global MSG_FLAG
        if not MSG_FLAG:
            messagebox.showinfo("INFO", "Interrupt the drawing by pressing the Escape key!")
            MSG_FLAG = True
        # Create a fg color list.
        fg_color = create_color_list(fg_color)
        # Set the len.
        col_len = len(fg_color)
        # Set image to None.
        n,m = 512,512
        pil_image = Image.new('RGB', (n, m))
        # Try to draw an image.
        try:
            # Setup turtle screen.
            self.sc.setup(self.screen_x, self.screen_y)
            # Set title and background color.
            turtle.title(TURTLE_TITLE)
            # Reset the screen.
            turtle.reset()
            turtle.resetscreen()
            # Clear the screen.
            turtle.clear()
            turtle.clearscreen()
            # Clear the screen.
            turtle.clearscreen()
            turtle.bgcolor(screen_color)
            # Withdraw window.
            if withdraw_window:
                self.root.iconify()
                self.root.withdraw()
            else:
                self.root.withdraw()
                self.root.iconify()
                self.root.deiconify()
            # Define the turtle object.
            ts = turtle.Turtle()
            # Set the fill and pen color.
            ts.fillcolor(fill_color)
            ts.pencolor(pen_color)
            # Set the shape of the turtle.
            ts.shape(shape)
            # Set the speed of the turtle.
            ts.speed(turtle_speed)
            # Set the pen size.
            ts.pensize(thickness)
            # Hide the turtle.
            if hide_turtle:
                turtle.hideturtle()
                ts.hideturtle()
            # Check if background needed.
            if bg_on_off:
                # Get the turtle screen.
                cs = ts.getscreen()
                # Set a new tkwin canvas.
                tkwin = cs.getcanvas()
                # Add a new rectangle.
                pad = 0
                x0, y0 = -int(self.screen_x/2)+pad, -int(self.screen_y/2)+pad
                x1, y1 = int(self.screen_x/2)-pad, int(self.screen_y/2)-pad
                rect = tkwin.create_rectangle(x0, y0, x1, y1,
                           width=0, outline=bg_color, fill=bg_color)
            # Start fill.
            if fill_on_off:
                ts.begin_fill()
            # ------------------------------------
            # Run a loop.
            # ------------------------------------
            # Initialise some settings.
            idx = 0.0
            scaling = 0  
            range_factor =  col_len / max_length
            ts.left(start_angle)
            for x in range(max_length):
                ts.pensize(thickness+scaling)
                scaling += increment_pen 
                if self.quit:
                    break
                ts.pencolor(fg_color[int(idx)])
                ts.forward(x*scale_factor)
                ts.left(angle)
                idx += range_factor 
            # ------------------------------------
            # End of loop.
            # ------------------------------------
            # End fill.
            if fill_on_off:
                ts.end_fill()
            # Show message.
            messagebox.showinfo("INFO", "Spirograph successfully completed!")
            # Reset the pen color.
            #ts.pencolor(pen_color)
            # Hide the turtle.
            if hide_turtle:
                turtle.hideturtle()
                ts.hideturtle()
            # Get the canvas from the screen.
            #cs = turtle.getscreen().getcanvas()
            #eps = cs.postscript(colormode='color')
            # Create a Pil image.
            #pil_image = Image.open(BytesIO(eps.encode('utf-8'))).convert("RGB")
            # Get date and time.
            d = datetime.now().strftime("%m%d%Y_%H%M%S_%f")
            # Set the file names.
            name_png = "/ComfyUI_" + str(d) + ".png"
            name_eps = "/ComfyUI_" + str(d) + ".eps"
            # Set the paths.
            PNG_PATH = ''.join([str(OUTPUT_PATH), name_png])
            EPS_PATH = ''.join([str(OUTPUT_PATH), name_eps])
            # Save the eps image.
            save_eps(turtle, EPS_PATH, screen_x, screen_y)
            # Save the png image.
            pil_image = save_png(EPS_PATH, PNG_PATH, width, height, resize_sampler)
        except RuntimeError as err:
            # Print the error message.
            err_str = "RuntimeError ERROR in function:"
            if str(err) != "":
                print(err_str, func + "->", str(err))
            else:
                print(err_str, func, "->", "empty")
            # Print the traceback.
            print(traceback.format_exc())
        except tk.TclError as err:
            # Print the error message.
            err_str = "tkinter.TclError ERROR in function:"
            if str(err) != "":
                print(err_str, func + "->", str(err))
            else:
                print(err_str, func, "->", "empty")
            # Print the traceback.
            print(traceback.format_exc())
            # Create an image.
            img_txt = "Oops, something went wrong!"
            pil_image = make_image(img_txt, 25, 256)
            # Print the error message.
            # err_msg = "Oops, Error!"
            # ErrWin(err_msg)
        except Exception as err:
            if str(type(err)) == "<class 'turtle.Terminator'>":
                print("ERROR:", "turtle.Terminator")
            else:
                print("ERROR:", str(err))
        # Return the opencv image.
        return pil_image

    def turtle_graphics_main(self, thickness, turtle_speed, shape, max_length, hide_turtle,
                         screen_color, fg_color, screen_x, screen_y, fill_on_off,
                         fill_color, replacement_color, width, height,
                         pen_color, replace_on_off, remove_on_off, angle, withdraw_window,
                         start_angle, resize_sampler, scale_factor, bg_on_off, bg_color, increment_pen):
        '''Main node function. Create a Turtle Graphics demo.'''
        # Setup of the turtle screen based on the ComfyUI settings.
        self.screen_x = screen_x
        self.screen_y = screen_y
        # Run the demo.
        image = self.demo(thickness, turtle_speed, shape, max_length,
                          hide_turtle, screen_color, fg_color,
                          screen_x, screen_y, fill_on_off,
                          fill_color, pen_color, angle, withdraw_window,
                          start_angle, scale_factor, width, height, 
                          resize_sampler, bg_on_off, bg_color, increment_pen)
        # Pil image to numpy image.
        numpy_image = np.array(image)
        # Resize the image.
        sampler = RESIZE_SAMPLER[resize_sampler]
        image = resize_pil_image(numpy_image, width, height, sampler)
        # Replace the color if flag true.
        if replace_on_off:
            image = replace_color(image, replacement_color)
        # Remove the color if flag true.
        if remove_on_off:
            image = remove_color(image)
        info("Ready for drawing again!")
        # Convert 'PIL' image to Tensor.
        image = pil2tensor(image)
        # Return the return types.
        return (image,)





