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
# pylint: disable=redefined-outer-name

# Import the standard Python modules.
import re
import hashlib
import pathlib
import time
import turtle
from datetime import datetime
import math

# Import the third party Python modules.
import torch
import webcolors
import cv2
import numpy as np
from PIL import Image

# Set some paths.
SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
PARENT_PATH = SCRIPT_PATH.parent.absolute()
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

# ****************
# OneSide function
# ****************
def OneSide(ts, side, diag, level):
    '''oneSide function.'''
    if level==0:
        return
    else:
        OneSide(ts, side, diag, level-1)
        ts.right(45); ts.forward(diag); ts.right(45)
        OneSide(ts, side, diag, level-1)
        ts.left(90); ts.forward(side); ts.left(90)
        OneSide(ts, side, diag, level-1)
        ts.right(45); ts.forward(diag); ts.right(45)
        OneSide(ts, side, diag, level-1)

# *******************
# Sierpinski function
# *******************
def sierpinski(ts, side, level, color):
    '''Sierpinski function.'''
    diag = side / math.sqrt(2)
    for i in range(4):
        ts.pencolor(color[i % len(color)])
        OneSide(ts, side, diag, level)
        ts.right(45)
        ts.forward(diag)
        ts.right(45)

# ****************************************
# Class TurtleGraphicsSirpinskiCurveDemo
# ****************************************
class TurtleGraphicsSierpinskiCurveDemo:
    '''Create a Turtle Graphics rotated pentagram demo.'''

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
                "level": ("INT", {"default": 4, "min": 1, "max": 2048}),
                "side": ("FLOAT", {"default": 16.5, "min": 0.0, "max": 2048}),
                "xpos": ("INT", {"default": 256, "min": 0, "max": 4096}),
                "ypos": ("INT", {"default": 256, "min": 0, "max": 4096}),
                "start_angle": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 360.0}),
                "thickness": ("FLOAT", {"default": 0.1, "min": 0.1, "max": 100000.0, "step": 0.1}),
                "turtle_speed": ("INT", {"default": 0, "min": 0, "max": 10}),
                "turtle_shape": (TURTLE, {}),
                "hide_turtle": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "fill_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "bg_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "bg_color": ("STRING", {"multiline": False, "default": "black"}),
                "fg_color": ("STRING", {"multiline": True, "default": "red, green, blue, yellow, cyan, magenta"}),
                "pen_color": ("STRING", {"multiline": False, "default": "red"}),
                "fill_color": ("STRING", {"multiline": False, "default": "blue"}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "resize_sampler": (KEYS, {}),
                "screen_x": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_y": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_color": ("STRING", {"multiline": False, "default": "orange"}),
                "withdraw_window": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "remove_background": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
            },
            "optional": {
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "turtle_graphics_main"
    CATEGORY = "🐢 Turtle Graphics"
    OUTPUT_NODE = True

    def demo(self, thickness, turtle_speed, turtle_shape, level,
            hide_turtle, screen_color, fg_color, screen_x, screen_y,
            fill_on_off, fill_color, pen_color, withdraw_window,
            start_angle, bg_on_off, bg_color, side, width, height,
            resize_sampler, remove_background, xpos, ypos):
        '''Create a simple Turtle Graphics Demo.'''
        # Create a fg color list.
        fg_color = create_color_list(fg_color)
        # Set the len.
        col_len = len(fg_color)
        # Set image to None.
        n,m = 512,512
        pil_image = Image.new('RGB', (n, m))
        # Try to draw an image.
        try:
            # Define the turtle screen.
            sc = turtle.Screen()
            sc.setup(screen_x, screen_y)
            # Set title and background color.
            turtle.title(TURTLE_TITLE)
            # Clear the screen.
            turtle.clear()
            turtle.clearscreen()
            turtle.bgcolor(screen_color)
            # Withdraw window.
            root = turtle.getscreen()._root
            if withdraw_window:
                root.withdraw()
            else:
                root.deiconify()
            # Define the turtle object.
            ts = turtle.Turtle()
            # Set the fill color.
            ts.fillcolor(fill_color)
            # Set the pen color.
            ts.pencolor(pen_color)
            # Set the shape of the turtle.
            ts.shape(turtle_shape)
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
                x0, y0 = -int(screen_x/2)+pad, -int(screen_y/2)+pad
                x1, y1 = int(screen_x/2)-pad, int(screen_y/2)-pad
                rect = tkwin.create_rectangle(x0, y0, x1, y1,
                           width=0, outline=bg_color, fill=bg_color)
            # Start fill.
            if fill_on_off:
                ts.begin_fill()
            # ------------------------------------
            # START MAIN IMAGE CREATION
            # ------------------------------------
            ts.left(start_angle)
            ts.up()
            ts.goto(xpos, ypos)
            ts.right(90)
            ts.down()
            sierpinski(ts, side, level, fg_color)
            # ------------------------------------
            # END MAIN IMAGE CREATION
            # ------------------------------------
            # End fill.
            if fill_on_off:
                ts.end_fill()
            # Reset the pen color.
            ts.pencolor(pen_color)
            # Hide the turtle.
            if hide_turtle:
                turtle.hideturtle()
                ts.hideturtle()
            # Set the file names.
            d = datetime.now().strftime("%m%d%Y_%H%M%S_%f")
            name_eps = "/TGN_" + str(d) + ".eps"
            name_png = "/TGN_" + str(d) + ".png"
            name_trans = "/TGN_" + str(d) + "_trans.png"
            EPS_PATH = ''.join([str(OUTPUT_PATH), name_eps])
            PNG_PATH = ''.join([str(OUTPUT_PATH), name_png])
            TRANS_PATH = ''.join([str(OUTPUT_PATH), name_trans])
            # Get the screen canvas.
            eps_cs = turtle.getscreen()
            # Save the eps image.
            ps_width = screen_x
            ps_height = screen_y
            ps_x = -int(screen_x/2)
            ps_y = -int(screen_y/2)
            ps_pw = screen_x
            ps_ph = screen_y
            eps_cs.getcanvas().postscript(file=EPS_PATH, x=ps_x, y=ps_y,
                                          width=ps_width, height=ps_height,
                                          pagewidth=ps_pw, pageheight=ps_ph)
            # Scale the image up and down.
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
            print(cx,cy)
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
            # Turtle is done.
            if withdraw_window:
                root.quit()
            else:
                turtle.exitonclick()
                # Catch errors while closing window.
                try:
                    turtle.done()
                    turtle.mainloop()
                except:
                    pass
        except Exception as err:
            if str(type(err)) == "<class 'turtle.Terminator'>":
                print("ERROR:", "turtle.Terminator")
            else:
                print("ERROR:", str(err))
        # Try to remove the background.
        try:
            if remove_background:
                pil_image = replace_color(pil_image, bg_color, "black")
                pil_image = remove_color(pil_image)
                imgNEW = Image.fromarray(pil_image)
                imgNEW.save(TRANS_PATH)
        except Exception as err:
            print("ERROR:", str(err))
        # Return the opencv image.
        return pil_image

    def turtle_graphics_main(self, thickness, turtle_speed, turtle_shape,
            level, hide_turtle, screen_color, fg_color,
            screen_x, screen_y, fill_on_off, fill_color, bg_color,
            width, height, pen_color, bg_on_off, withdraw_window,
            start_angle, resize_sampler, side, remove_background,
            xpos, ypos):
        '''Main node function. Create a Turtle Graphics demo.'''
        # Run the demo.
        image = self.demo(thickness, turtle_speed, turtle_shape,
                    level, hide_turtle, screen_color,
                    fg_color, screen_x, screen_y, fill_on_off,
                    fill_color, pen_color, withdraw_window,
                    start_angle, bg_on_off, bg_color, side, width,
                    height, resize_sampler, remove_background,
                    xpos, ypos)
        # Convert PIL image to Numpy array.
        numpy_image = np.array(image)
        # Resize the image.
        sampler = RESIZE_SAMPLER[resize_sampler]
        # Convert 'PIL' image to Tensor.
        image = pil2tensor(image)
        # Return the return types.
        return (image,)
