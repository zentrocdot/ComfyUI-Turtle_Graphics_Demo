#!/usr/bin/python
'''Simple Turtle Graphics demo(nstrator).'''
# pylint: disable=protected-access
# pylint: disable=useless-return
# pylint: disable=invalid-name
# pylint: disable=bare-except
# pylint: disable=broad-exception-caught
# pylint: disable=no-member
# pylint: disable=too-many-positional-arguments
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=unused-variable
# pylint: disable=line-too-long
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-function-args
# pylint: disable=global-statement

# Import the standard Python modules.
import tkinter as tk
import turtle
from math import cos, sin
import math
import re
import hashlib
import pathlib
import time
from datetime import datetime
from time import sleep
from io import BytesIO
import traceback
from tkinter import messagebox

# Import the third party Python modules.
import torch
import webcolors
import cv2
import numpy as np
from PIL import Image
import imageio

# Set some paths.
SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
PARENT_PATH = SCRIPT_PATH.parent.absolute()
CUSTOM_NODES_PATH = pathlib.Path(PARENT_PATH).parent.resolve()
COMFYUI_PATH = pathlib.Path(CUSTOM_NODES_PATH).parent.resolve()
OUTPUT_PATH = ''.join([str(COMFYUI_PATH), "/output"])

# Set some constants.
TURTLE_TITLE = "Spirograph Simulation"

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

# ----------------------------
# Function create_color_list()
# ----------------------------
def create_color_list(col_str: str) -> list:
    '''Create color list function.

    Create a color list from a given color string.

    @PARAMS
        col_str -> color string (str)
    @RETURNS
        col_list - > color list (list)
    '''
    # Remove whitespaces from the given color string.
    stripString = str(col_str).strip()
    # Create a list from the given color string.
    col_list = stripString.split(",")
    # Remove whitespaces from the created color list.
    col_list = [x.strip(' ') for x in col_list]
    # Return the color list.
    return col_list

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

# ------------------------
# Function replace_color()
# ------------------------
def replace_color(image, old_color, new_color):
    '''Replace old color by new color.

    First the PIL image is converted to a Numpy array. Then the old color is
    replaced by the new color.

    @PARAMS
        image     -> image to modify (PIL)
        old_color -> old color name (str)
        new_color -> new color name (str)

    @RETURNS
        numpy_image -> modified image (numpy)
    '''
    # Convert image to RGB.
    image = image.convert('RGB')
    # Convert PIL image to Numpy array.
    numpy_image = np.array(image)
    # Determine the RGB color tuples.
    old_color = color_to_rgb(old_color)
    new_color = color_to_rgb(new_color)
    # Replace old color with new color.
    numpy_image[(numpy_image == old_color).all(axis = -1)] = new_color
    # Return the image as Numpy array.
    return numpy_image

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
    h, w, _ = image.shape
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

# ----------------
# Ellipse function
# ----------------
def ellipse(ts, a, b, phi, h=0, k=0, theta=1):
    '''Turtle Graphics ellipse.'''
    # Get phi in radians.
    phi_rad = math.radians(phi)
    # Set the rotation angle.
    alpha = 360
    # Pen up.
    ts.up()
    # Loop over the roattion angle.
    for t in range(0,alpha+1):
        # Pen down if in start position.
        if t != 0:
            ts.down()
        # Degrees in radians conversion.
        rad = math.radians(t)
        # Calculate the ellipse.
        x0 = h + (a * math.cos(rad))
        y0 = k + (b * math.sin(rad))
        # Rotate the ellipse in counter clockwise direction.
        x1 = math.cos(theta * phi_rad) * x0 + math.sin(theta * phi_rad) * y0
        y1 = -math.sin(theta * phi_rad) * x0 + math.cos(theta * phi_rad) * y0
        # Set the heading of the turtle.
        ts.seth(phi)
        # Draw point of the ellipse
        ts.setposition(x1, y1)
    # Return None
    return None

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

# --------------------
# Function save_video.
# --------------------
def save_videos(frames, video_types):
    '''Save video function.'''
    d = datetime.now().strftime("%m%d%Y_%H%M%S_%f")
    if video_types == "GIF":
        name_gif = "/ComfyUI_" + str(d) + ".gif"
        GIF_PATH = ''.join([str(OUTPUT_PATH), name_gif])
        frames[0].save(GIF_PATH, format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=200, loop=0)
    elif video_types == "MP4":
        name_mp4 = "/ComfyUI_" + str(d) + ".mp4"
        MP4_PATH = ''.join([str(OUTPUT_PATH), name_mp4])
        imageio.mimsave(MP4_PATH, frames)
    # Return None
    return None

# ***********************************
# Class TurtleGraphicsEpitrochoidDemo
# ***********************************
class TurtleGraphicsEpitrochoidDemo:
    '''Create a Turtle Graphics Epitrochoid demo.'''

    def __init__(self):
        '''Class __init__ function.'''
        self.screen_x = 512
        self.screen_y = 512
        self.quit = False
        self.sc = turtle.Screen()
        self.sc.setup(self.screen_x, self.screen_y)
        self.root = turtle.getscreen()._root
        self.root.option_add('*Dialog.msg.font', 'Helvetica 12 bold')
        self.root.option_add('*Dialog.msg.width', 32)
        self.root.option_add("*Dialog.msg.wrapLength", "6i")
        self.root.protocol("WM_DELETE_WINDOW", self.root.update)
        self.root.bind('<Escape>', self.quit_loop)
        #self.root.bind("<KeyRelease>", self.key)

    def key(self, event):
        '''Key bind test function.'''
        print(event.keysym)

    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        '''Class method IS_CHANGED.'''
        m = hashlib.sha256()
        bytes_string = str(time.time()).encode("utf-8")
        m.update(bytes_string)
        return m.digest().hex()

    @classmethod
    def INPUT_TYPES(cls):
        '''Define the input types.'''
        return {
            "required": {
                "number_rotations": ("INT", {"default": 9, "min": 1, "max": 2048}),
                "R": ("FLOAT", {"default": 100.0, "min": 0.0, "max": 2048.0}),
                "r": ("FLOAT", {"default": 60.0, "min": 0.0, "max": 2048.0}),
                "d": ("FLOAT", {"default": 50.0, "min": 0.0, "max": 2048.0}),
                "theta": ("FLOAT", {"default": 0.1, "min": 0.01, "max": 2048.0, "step": 0.01}),
                "pen_thickness": ("FLOAT", {"default": 2.5, "min": 0.1, "max": 100000.0, "step": 0.1}),
                "spirograph_thickness": ("FLOAT", {"default": 1.5, "min": 0.1, "max": 100000.0, "step": 0.1}),
                "remove_spirograph": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "point_size": ("FLOAT", {"default": 8.0, "min": 0.1, "max": 100000.0, "step": 0.1}),
                "turtle_speed": ("FLOAT", {"default": 0.00, "min": 0.00, "max": 10, "step": 0.01}),
                "colorful_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "fill_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "bg_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "bg_color": ("STRING", {"multiline": False, "default": "black"}),
                "fg_color": ("STRING", {"multiline": True, "default": "red, green, blue, yellow, cyan, magenta"}),
                "r_color": ("STRING", {"multiline": False, "default": "lightslateblue"}),
                "R_color": ("STRING", {"multiline": False, "default": "darkslategray"}),
                "fill_color": ("STRING", {"multiline": False, "default": "blue"}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "resize_sampler": (KEYS, {}),
                "screen_x": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_y": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_color": ("STRING", {"multiline": False, "default": "orange"}),
                "withdraw_window": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "remove_background": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "start_delay": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 120.0, "step": 0.1}),
                "save_video": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "video_types": (["GIF", "MP4"], {}),
                "save_Kth_image": ("INT", {"default": 8, "min": 1, "max": 4096}),
            },
            "optional": {
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "turtle_graphics_main"
    CATEGORY = "🐢 Turtle Graphics/➿ Spirograph"
    OUTPUT_NODE = True

    def quit_loop(self, *args, **kwargs):
        '''Close windows handler.'''
        self.quit = True
        print("You try to interrupt the Turtle Graphics drawing!")

    def spirograph(self, ts, tsPen, R, r, d, fill_on_off,
                   start_delay, R_color, r_color, number_rotations,
                   theta, fill_color, remove_spirograph, point_size,
                   colorful_on_off, fg_color, col_len, turtle_speed,
                   save_video, Kth):
        '''Spirograph.'''
        # Reset quit flag.
        self.quit = False
        # Initialise the frames list.
        frames = []
        # Set start delay.
        if start_delay >= 0.0:
            sleep(start_delay)
        # Set some variables.
        angle = 0
        # Calculate number of steps.
        number_steps = int((2 * math.pi * number_rotations / theta)+1)
        # Go to start position.
        tsPen.penup()
        tsPen.goto(R+r-d, 0)
        tsPen.pendown()
        # Start fill.
        if fill_on_off:
            tsPen.fillcolor(fill_color)
            tsPen.begin_fill()
        for t in range(0, number_steps):
            if self.quit:
                break
            if not remove_spirograph:
                # Draw the fixed circle.
                ts.clear()
                ts.penup()
                ts.setheading(0)
                ts.goto(0, -R)
                ts.color(R_color)
                ts.pendown()
                ts.circle(R)
            # Increment angle.
            angle += theta
            if not remove_spirograph:
                # Calculate a new position.
                x = (R + r) * cos(angle)
                y = (R + r) * sin(angle)
                # Draw the rolling circle.
                ts.penup()
                ts.goto(x, y-r)
                ts.color(r_color)
                ts.pendown()
                ts.circle(r)
                # Draw curve.
                ts.penup()
                ts.goto(x, y)
                ts.pendown()
                # Calculate x and y coordinate of the curve.
            x = (R + r) * cos(angle) - d * cos(((R+r)/r)*angle)
            y = (R + r) * sin(angle) - d * sin(((R+r)/r)*angle)
            if not remove_spirograph:
                ts.dot(point_size)  # Print inner dot.
                ts.goto(x, y)       # Print arm
                ts.dot(point_size)  # Print outer dot.
            if colorful_on_off:
                tsPen.pencolor(fg_color[t % col_len])
            tsPen.goto(x, y)  # Draw curve.
            ts.getscreen().update()
            # Sleep a little bit.
            sleep(turtle_speed)
            if save_video:
                if t % Kth == 0:
                    print(t)
                    eps = turtle.getscreen().getcanvas().postscript()
                    img = Image.open(BytesIO(eps.encode('utf-8')))
                    frames.append(img)
        # End fill.
        if fill_on_off:
            tsPen.end_fill()
        # Show message.
        messagebox.showinfo("INFO", "Spirograph successfully completed!")
        # Return None.
        return frames

    def demo(self, spirograph_thickness, turtle_speed, number_rotations,
            screen_color, fg_color, screen_x, screen_y, fill_on_off,
            fill_color, r_color, R_color, withdraw_window, bg_on_off,
            bg_color, r, R, d, width, height, resize_sampler,
            remove_background, point_size, pen_thickness,
            remove_spirograph, theta, start_delay, colorful_on_off,
            video_types, save_video, Kth):
        '''Create a simple Turtle Graphics Demo.'''
        global MSG_FLAG
        if not MSG_FLAG:
            messagebox.showinfo("INFO", "Interrupt the drawing by pressing the Escape key!")
            MSG_FLAG = True
        # Get the name of the function.
        func = get_function_name(self.demo)
        # Initialise the frames list.
        frames = []
        # Create the fg color list.
        fg_color = create_color_list(fg_color)
        # Set the length of the color list.
        col_len = len(fg_color)
        # Set width and height of an empty image.
        n, m = 512, 512
        # Set the image to None.
        pil_image = Image.new('RGB', (n, m))
        # Try to draw an image.
        try:
            # Setup screen.
            self.sc.setup(self.screen_x, self.screen_y)
            # Withdraw window.
            if withdraw_window:
                self.root.iconify()
                self.root.withdraw()
            else:
                self.root.withdraw()
                self.root.iconify()
                self.root.deiconify()
            # Reset the screen.
            turtle.reset()
            turtle.resetscreen()
            # Clear the screen.
            turtle.clear()
            turtle.clearscreen()
            # Set title and background color.
            turtle.title(TURTLE_TITLE)
            turtle.bgcolor(screen_color)
            # Hide the turtle in general.
            turtle.hideturtle()
            # Define the turtle object.
            ts = turtle.Turtle()
            ts.hideturtle()
            ts.speed(0)
            ts.pensize(spirograph_thickness)
            ts.pencolor(R_color)
            # Define the pen object.
            tsPen = turtle.Turtle()
            tsPen.hideturtle()
            tsPen.speed(0)
            tsPen.pensize(pen_thickness)
            tsPen.color(fg_color[0])  # Curve color.
            # Set the turtle tracer.
            turtle.tracer(0,0)
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
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # Start Spirograph                                           +
            frames = self.spirograph(ts, tsPen, R, r, d, fill_on_off,
                         start_delay, R_color, r_color, number_rotations,
                         theta, fill_color, remove_spirograph, point_size,
                         colorful_on_off, fg_color, col_len, turtle_speed,
                         save_video, Kth)
            # End Spirograph                                             +
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # Save video.
            if save_video:
                save_videos(frames, video_types)
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
        except turtle.Terminator as err:
            # Print the error message.
            err_str = "turtle.Terminator ERROR in function:"
            if str(err) != "":
                print(err_str, func + "->", str(err))
            else:
                print(err_str, func, "->", "empty")
            # Print the traceback.
            print(traceback.format_exc())
            # Create an image.
            img_txt = "Oops, something went wrong!"
            pil_image = make_image(img_txt, 25, 256)
            # Print the info message.
            # inf_msg = "Press Queue!"
            # InfWin(inf_msg)
        except Exception as err:
            # Print the error message.
            err_str = "ERROR:"
            if str(err) != "":
                print(err_str, func + "->", str(err))
            else:
                print(err_str, func, "->", "empty")
            # Print the traceback.
            print(traceback.format_exc())
        # Try to remove the background.
        try:
            # Set name and path.
            name_trans = "/ComfyUI_" + str(d) + "_trans.png"
            TRANS_PATH = ''.join([str(OUTPUT_PATH), name_trans])
            # Remove background.
            if remove_background:
                pil_image = replace_color(pil_image, bg_color, "black")
                pil_image = remove_color(pil_image)
                # Create a Numpy array and save the image.
                imgNEW = Image.fromarray(pil_image)
                imgNEW.save(TRANS_PATH)
        except Exception as err:
            # Print error message.
            print("ERROR:", str(err))
            print(traceback.format_exc())
        # Show message.
        #messagebox.showinfo("INFO", "Ready for drawing again!")
        info("Ready for drawing again!")
        # Return the opencv image.
        return pil_image

    def turtle_graphics_main(self, spirograph_thickness, turtle_speed,
            number_rotations, screen_color, fg_color, screen_x, screen_y,
            fill_on_off, fill_color, bg_color, width, height, r_color,
            R_color, bg_on_off, withdraw_window, resize_sampler, r, R, d,
            remove_background, point_size, pen_thickness, remove_spirograph,
            theta, start_delay, colorful_on_off, video_types, save_video,
            save_Kth_image):
        '''Main node function. Create a Turtle Graphics demo.'''
        # Get the name of this function.
        func = get_function_name(self.turtle_graphics_main)
        # Setup of the turtle screen.
        self.screen_x = screen_x
        self.screen_y = screen_y
        # Run the spirograph demo.
        image = self.demo(spirograph_thickness, turtle_speed,
                    number_rotations, screen_color, fg_color,
                    screen_x, screen_y, fill_on_off, fill_color,
                    r_color, R_color, withdraw_window, bg_on_off,
                    bg_color, r, R, d, width, height, resize_sampler,
                    remove_background, point_size, pen_thickness,
                    remove_spirograph, theta, start_delay,
                    colorful_on_off, video_types, save_video,
                    save_Kth_image)
        # Convert the 'PIL' image to a Tensor.
        image = pil2tensor(image)
        # Return the return types.
        return (image,)
