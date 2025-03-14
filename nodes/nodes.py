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
import re
import hashlib
import time
import turtle
from io import BytesIO

# Import the third party Python modules.
import torch
import webcolors
import cv2
import numpy as np
from PIL import Image

# Set some constants.
TURTLE_TITLE = "Object-Oriented Turtle Demo"

# Set the shape of the turtle.
TURTLE = ['turtle', 'arrow', 'blank', 'circle', 'classic', 'square', 'triangle']

# Define the resize sampler.
RESIZE_SAMPLER = {"LANCZOS": 1, "BICUBIC": 3, "BILINEAR": 2,
                  "BOX": 4, "HAMMING": 5, "NEAREST": 0}
KEYS = list(RESIZE_SAMPLER.keys())

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

# *******************************
# Class TurtleGraphicsCirclesDemo
# *******************************
class TurtleGraphicsCirclesDemo:
    '''Create a Turtle Graphics circle demo.'''

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
                "number_rotations": ("INT", {"default": 36, "min": 1, "max": 1024}),
                "circle_radius": ("INT", {"default": 120, "min": 1, "max": 1024}),
                "rotation_angle": ("FLOAT", {"default": 10.0, "min": 1.0, "max": 360.0}),
                "start_angle": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 360.0}),
                "shape": (TURTLE, {}),
                "hide_turtle": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "fill_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "replace_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "remove_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "fg_color": ("STRING", {"multiline": True, "default": "red, green, blue, yellow, cyan, magenta"}),
                "pen_color": ("STRING", {"multiline": False, "default": "red"}),
                "fill_color": ("STRING", {"multiline": False, "default": "blue"}),
                "replacement_color": ("STRING", {"multiline": False, "default": "black"}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "resize_sampler": (KEYS, {}),
                "screen_x": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_y": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_color": ("STRING", {"multiline": False, "default": "orange"}),
                "withdraw_window": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
            },
            "optional": {
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "turtle_graphics_main"
    CATEGORY = "🐢 Turtle Graphics"
    OUTPUT_NODE = True

    def demo(self, thickness, turtle_speed, shape, number_rotations, rotation_angle,
             hide_turtle, circle_radius, screen_color, fg_color, screen_x, screen_y,
             fill_on_off, fill_color, pen_color, replace_on_off, remove_on_off,
             withdraw_window, start_angle):
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
            # Define turtle screen.
            sc = turtle.Screen()
            sc.setup(screen_x, screen_y)
            # Set title and background color.
            turtle.title(TURTLE_TITLE)
            # Clear the screen.
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
            # Start fill.
            if fill_on_off:
                ts.begin_fill()
            # ------------------------------------
            # Run a loop.
            # ------------------------------------
            ts.right(start_angle)
            for _ in range(number_rotations):
                ts.pencolor(fg_color[_ % col_len])
                ts.circle(circle_radius)
                ts.right(rotation_angle)
            # ------------------------------------
            # End of loop.
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
            # Get the canvas from the screen.
            cs = turtle.getscreen().getcanvas()
            eps = cs.postscript(colormode='color')
            # Create a Pil image.
            pil_image = Image.open(BytesIO(eps.encode('utf-8'))).convert("RGB")
            # Turtle is done.
            if withdraw_window:
                root.quit()
            else:
                turtle.exitonclick()
                # Catch error on closing.
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
        # Return the opencv image.
        return pil_image

    def turtle_graphics_main(self, thickness, turtle_speed, shape, number_rotations,
            rotation_angle, hide_turtle, circle_radius, screen_color, fg_color,
            screen_x, screen_y, fill_on_off, fill_color, replacement_color, width,
            height, pen_color, replace_on_off, remove_on_off, withdraw_window,
            start_angle, resize_sampler):
        '''Main node function. Create a Turtle Graphics demo.'''
        # Run the demo.
        image = self.demo(thickness, turtle_speed, shape, number_rotations,
                    rotation_angle, hide_turtle, circle_radius, screen_color,
                    fg_color, screen_x, screen_y, fill_on_off, fill_color,
                    pen_color, replace_on_off, remove_on_off, withdraw_window,
                    start_angle)
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
        # Convert 'PIL' image to Tensor.
        image = pil2tensor(image)
        # Return the return types.
        return (image,)

# ******************************
# Class TurtleGraphicsSpiralDemo
# ******************************
class TurtleGraphicsSpiralDemo:
    '''Create a Turtle Graphics circle demo.'''

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
                "max_length": ("INT", {"default": 270, "min": 1, "max": 2048}),
                "angle": ("INT", {"default": 59, "min": 1, "max": 2048}),
                "start_angle": ("INT", {"default": 0, "min": 0, "max": 2048}),
                "shape": (TURTLE, {}),
                "hide_turtle": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "fill_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "replace_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "remove_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "fg_color": ("STRING", {"multiline": True, "default": "red, green, blue, yellow, cyan, magenta"}),
                "pen_color": ("STRING", {"multiline": False, "default": "red"}),
                "fill_color": ("STRING", {"multiline": False, "default": "blue"}),
                "replacement_color": ("STRING", {"multiline": False, "default": "black"}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "resize_sampler": (KEYS, {}),
                "screen_x": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_y": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_color": ("STRING", {"multiline": False, "default": "orange"}),
                "withdraw_window": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
            },
            "optional": {
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "turtle_graphics_main"
    CATEGORY = "🐢 Turtle Graphics"
    OUTPUT_NODE = True

    def demo(self, thickness, turtle_speed, shape, max_length, hide_turtle,
             screen_color, fg_color, screen_x, screen_y, fill_on_off,
             fill_color, pen_color, angle, withdraw_window, start_angle):
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
            # Define turtle screen.
            sc = turtle.Screen()
            sc.setup(screen_x, screen_y)
            # Set title and background color.
            turtle.title(TURTLE_TITLE)
            # Clear the screen.
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
            # Start fill.
            if fill_on_off:
                ts.begin_fill()
            # ------------------------------------
            # Run a loop.
            # ------------------------------------
            ts.left(start_angle)
            for x in range(max_length):
                ts.pencolor(fg_color[x % col_len])
                ts.forward(x)
                ts.left(angle)
            # ------------------------------------
            # End of loop.
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
            # Get the canvas from the screen.
            cs = turtle.getscreen().getcanvas()
            eps = cs.postscript(colormode='color')
            # Create a Pil image.
            pil_image = Image.open(BytesIO(eps.encode('utf-8'))).convert("RGB")
            # Turtle is done.
            if withdraw_window:
                root.quit()
            else:
                turtle.exitonclick()
                # Catch error on closing.
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
        # Return the opencv image.
        return pil_image

    def turtle_graphics_main(self, thickness, turtle_speed, shape, max_length, hide_turtle,
                         screen_color, fg_color, screen_x, screen_y, fill_on_off,
                         fill_color, replacement_color, width, height,
                         pen_color, replace_on_off, remove_on_off, angle, withdraw_window,
                         start_angle, resize_sampler):
        '''Main node function. Create a Turtle Graphics demo.'''
        # Run the demo.
        image = self.demo(thickness, turtle_speed, shape, max_length,
                          hide_turtle, screen_color, fg_color,
                          screen_x, screen_y, fill_on_off,
                          fill_color, pen_color, angle, withdraw_window, start_angle)
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
        # Convert 'PIL' image to Tensor.
        image = pil2tensor(image)
        # Return the return types.
        return (image,)

# *****************************************
# Class TurtleGraphicsCircleLobesSpiralDemo
# *****************************************
class TurtleGraphicsCircleLobesDemo:
    '''Create a Turtle Graphics circle demo.'''

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
                "number_lobes": ("INT", {"default": 5, "min": 1, "max": 2048}),
                "number_circles": ("INT", {"default": 28, "min": 1, "max": 2048}),
                "start_radius": ("INT", {"default": 5, "min": 1, "max": 2048}),
                "start_angle": ("INT", {"default": 45, "min": 0, "max": 360}),
                "increment_angle": ("INT", {"default": 0, "min": 0, "max": 360}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0}),
                "switch_color": ("BOOLEAN", {"default": False}),
                "shape": (TURTLE, {}),
                "hide_turtle": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "fill_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "replace_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "remove_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "fg_color": ("STRING", {"multiline": True, "default": "red, green, blue, yellow, cyan, magenta"}),
                "pen_color": ("STRING", {"multiline": False, "default": "red"}),
                "fill_color": ("STRING", {"multiline": False, "default": "blue"}),
                "replacement_color": ("STRING", {"multiline": False, "default": "black"}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "resize_sampler": (KEYS, {}),
                "screen_x": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_y": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_color": ("STRING", {"multiline": False, "default": "orange"}),
                "withdraw_window": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
            },
            "optional": {
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "turtle_graphics_main"
    CATEGORY = "🐢 Turtle Graphics"
    OUTPUT_NODE = True

    def demo(self, thickness, turtle_speed, shape, number_circles, hide_turtle,
             screen_color, fg_color, screen_x, screen_y, fill_on_off, fill_color,
             pen_color, start_radius, withdraw_window, start_angle, increment_angle,
             scale, number_lobes, switch_color):
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
            # Start fill.
            if fill_on_off:
                ts.begin_fill()
            # ------------------------------------
            # Prepare and run a loop.
            # ------------------------------------
            ang = 360.0 / number_lobes
            ts.left(start_angle)
            for i in range(number_circles):
                if switch_color:
                    ts.pencolor(fg_color[i % col_len])
                for j in range (0, number_lobes):
                    if not switch_color:
                        ts.pencolor(fg_color[j % col_len])
                    ts.circle(start_radius*i*scale)
                    ts.left(ang)
                ts.left(increment_angle)
            # ------------------------------------
            # End of loop.
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
            # Get the canvas from the screen.
            cs = turtle.getscreen().getcanvas()
            eps = cs.postscript(colormode='color')
            # Create a Pil image.
            pil_image = Image.open(BytesIO(eps.encode('utf-8'))).convert("RGB")
            # Turtle is done.
            if withdraw_window:
                root.quit()
            else:
                turtle.exitonclick()
                # Catch error on closing.
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
        # Return the opencv image.
        return pil_image

    def turtle_graphics_main(self, thickness, turtle_speed, shape, number_circles,
            hide_turtle, screen_color, fg_color, screen_x, screen_y, fill_on_off,
            fill_color, replacement_color, width, height, pen_color, replace_on_off,
            remove_on_off, start_radius, withdraw_window, start_angle, increment_angle,
            scale, number_lobes, switch_color, resize_sampler):
        '''Main node function. Create a Turtle Graphics demo.'''
        # Run the demo.
        image = self.demo(thickness, turtle_speed, shape, number_circles, hide_turtle,
            screen_color, fg_color, screen_x, screen_y, fill_on_off, fill_color,
            pen_color, start_radius, withdraw_window, start_angle, increment_angle,
            scale, number_lobes, switch_color)
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
        # Convert 'PIL' image to Tensor.
        image = pil2tensor(image)
        # Return the return types.
        return (image,)

# *******************************
# Class TurtleGraphicsSquaresDemo
# *******************************
class TurtleGraphicsSquaresDemo:
    '''Create a Turtle Graphics circle demo.'''

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
                "number_rotations": ("INT", {"default": 84, "min": 1, "max": 2048}),
                "start_length": ("INT", {"default": 10, "min": 0, "max": 2048}),
                "increment_length": ("INT", {"default": 2, "min": 0, "max": 2048}),
                "angle": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 360.0}),
                "increment_angle": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 360.0}),
                "start_angle": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 360.0}),
                "switch_color": ("BOOLEAN", {"default": True}),
                "shape": (TURTLE, {}),
                "hide_turtle": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "fill_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "replace_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "remove_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
                "fg_color": ("STRING", {"multiline": True, "default": "red, green, blue, yellow, cyan, magenta"}),
                "pen_color": ("STRING", {"multiline": False, "default": "red"}),
                "fill_color": ("STRING", {"multiline": False, "default": "blue"}),
                "replacement_color": ("STRING", {"multiline": False, "default": "black"}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "resize_sampler": (KEYS, {}),
                "screen_x": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_y": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "screen_color": ("STRING", {"multiline": False, "default": "orange"}),
                "withdraw_window": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
            },
            "optional": {
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "turtle_graphics_main"
    CATEGORY = "🐢 Turtle Graphics"
    OUTPUT_NODE = True

    def demo(self, thickness, turtle_speed, shape, number_rotations, hide_turtle,
             screen_color, fg_color, screen_x, screen_y, fill_on_off,
             fill_color, pen_color, start_length, increment_length,
             withdraw_window, angle, start_angle, increment_angle, switch_color):
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
            # Start fill.
            if fill_on_off:
                ts.begin_fill()
            # ------------------------------------
            # Run a loop.
            # ------------------------------------
            fac = start_length
            ts.left(start_angle)
            for i in range(number_rotations):
                if switch_color:
                    ts.pencolor(fg_color[i % col_len])
                for j in range (0,4):
                    if not switch_color:
                        ts.pencolor(fg_color[j % col_len])
                    ts.forward(fac)
                    ts.left(90)
                ts.left(angle)
                angle = angle + increment_angle
                fac = fac + increment_length
            # ------------------------------------
            # End of loop.
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
            # Get the canvas from the screen.
            cs = turtle.getscreen().getcanvas()
            eps = cs.postscript(colormode='color')
            # Create a Pil image.
            pil_image = Image.open(BytesIO(eps.encode('utf-8'))).convert("RGB")
            # Turtle is done.
            if withdraw_window:
                root.quit()
            else:
                turtle.exitonclick()
                # Catch error on closing.
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
        # Return the opencv image.
        return pil_image

    def turtle_graphics_main(self, thickness, turtle_speed, shape, number_rotations,
                         hide_turtle, screen_color, fg_color, screen_x,
                         screen_y, fill_on_off, fill_color, replacement_color,
                         width, height, pen_color, replace_on_off, remove_on_off,
                         start_length, increment_length, withdraw_window, angle,
                         start_angle, increment_angle, switch_color, resize_sampler):
        '''Main node function. Create a Turtle Graphics demo.'''
        # Run the demo.
        image = self.demo(thickness, turtle_speed, shape, number_rotations,
                          hide_turtle, screen_color, fg_color,
                          screen_x, screen_y, fill_on_off,
                          fill_color, pen_color, start_length, increment_length,
                          withdraw_window, angle, start_angle, increment_angle, switch_color)
        # Pil image to Numpy array.
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
        # Convert 'PIL' image to Tensor.
        image = pil2tensor(image)
        # Return the return types.
        return (image,)

COLOR_STRING = "white, whitesmoke, snow, seashell, cornsilk, azure, " + \
               "aliceblue, antiquewhite, ivory, honeydew, mistyrose, " + \
               "lightyellow, lemonchiffon, beige, moccasin, navajowhite, " + \
               "linen, mintcream, khaki, darkkhaki, tan, peru, burlywood, " + \
               "peachpuff, papayawhip, beige, bisque, wheat, " + \
               "lightgoldenrodyellow, yellow, orange, orangered, " + \
               "darkorange, gold, darkgoldenrod, chocolate, " + \
               "lightpink, pink, orchid, darkorchid, palevioletred, " + \
               "hotpink, magenta, darkmagenta, salmon, darksalmon, " + \
               "coral, lightcoral, rosybrown, tomato, indianred, red, " + \
               "firebrick, maroon, deeppink, crimson, darkred, brown, " + \
               "sienna, greenyellow, chartreuse, lawngreen, " + \
               "mediumspringgreen, mediumaquamarine, palegreen, " + \
               "mediumaquamarine, yellowgreen, olivedrab, olive, " + \
               "forestgreen, lime, limegreen, springgreen, chartreuse, " + \
               "darkseagreen, darkslategray, lightgray, dimgray, gray, " + \
               "lightslategrey, slategray, silver, lightsteelblue, " + \
               "darkcyan, darkslateblue, blanchedalmond, turquoise, " + \
               "paleturquoise, cadetblue, aquamarine, aqua, cyan, darkcyan, " + \
               "lightcyan, lavender, skyblue, royalblue, deepskyblue, " + \
               "dodgerblue, thistle, teal, violet, blueviolet, purple, " + \
               "rebeccapurple, indigo, blue, cornflowerblue, mediumblue, " + \
               "navy, midnightblue, darkblue"

# ************************************
# Class TurtleGraphicsConcateLinesDemo
# ************************************
class TurtleGraphicsConcateLinesDemo:
    '''Create a Turtle Graphics circle demo.'''

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
                "thickness": ("FLOAT", {"default": 0.1, "min": 0.1, "max": 100000.0, "step": 0.1}),
                "turtle_speed": ("INT", {"default": 0, "min": 0, "max": 10}),
                "number_rotations": ("INT", {"default": 375, "min": 1, "max": 2048}),
                "angle": ("FLOAT", {"default": 99.5, "min": 0.0, "max": 360.0}),
                "start_angle": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 360.0}),
                "shape": (TURTLE, {}),
                "hide_turtle": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "fill_on_off": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
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
                "screen_color": ("STRING", {"multiline": False, "default": "orange"}),
                "withdraw_window": ("BOOLEAN", {"default": False, "label_on": "on", "label_off": "off"}),
            },
            "optional": {
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "turtle_graphics_main"
    CATEGORY = "🐢 Turtle Graphics"
    OUTPUT_NODE = True

    def demo(self, thickness, turtle_speed, shape, number_rotations, hide_turtle,
             screen_color, fg_color, screen_x, screen_y, fill_on_off,
             fill_color, pen_color, withdraw_window, angle, start_angle):
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
            # Start fill.
            if fill_on_off:
                ts.begin_fill()
            # ------------------------------------
            # Run a loop.
            # ------------------------------------
            idx = 0
            fac = number_rotations // col_len
            ts.left(start_angle)
            for x in range(1, number_rotations):
                idx = int((x/fac))
                if idx < col_len:
                    ts.pencolor(fg_color[idx])
                ts.forward(x)
                ts.right(angle)
            # ------------------------------------
            # End of loop.
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
            # Get the canvas from the screen.
            cs = turtle.getscreen().getcanvas()
            eps = cs.postscript(colormode='color')
            # Create a Pil image.
            pil_image = Image.open(BytesIO(eps.encode('utf-8'))).convert("RGB")
            # Turtle is done.
            if withdraw_window:
                root.quit()
            else:
                turtle.exitonclick()
                # Catch error on closing.
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
        # Return the opencv image.
        return pil_image

    def turtle_graphics_main(self, thickness, turtle_speed, shape, number_rotations,
                         hide_turtle, screen_color, fg_color, screen_x,
                         screen_y, fill_on_off, fill_color, replacement_color,
                         width, height, pen_color, replace_on_off, remove_on_off,
                         withdraw_window, angle, start_angle, resize_sampler):
        '''Main node function. Create a Turtle Graphics demo.'''
        # Run the demo.
        image = self.demo(thickness, turtle_speed, shape, number_rotations,
                          hide_turtle, screen_color, fg_color, screen_x,
                          screen_y, fill_on_off, fill_color, pen_color,
                          withdraw_window, angle, start_angle)
        # Pil image to Numpy array.
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
        # Convert 'PIL' image to Tensor.
        image = pil2tensor(image)
        # Return the return types.
        return (image,)
