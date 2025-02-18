#!/usr/bin/python
'''Simple Turtle Graphics Demo.'''
# pylint: disable=invalid-name
# pylint: disable=protected-access
#
# version 0.0.0.1
#
# https://www.java-tech-stack.com/post/27187

# Import the Python Modules.
import turtle
import tkinter as tk
from PIL import Image

# Create a hidden tkinter root window
root = tk.Tk()
root.withdraw()  # Hide or withdraw the root window

# Create the turtle screen without showing the turtle screen.
screen = turtle.Screen()
screen.cv._rootwindow.withdraw()

# Set the filename.
FN0 = "pentagon.eps"
FN1 = "pentagon.jpg"

# Set up a pentagon.
sides = 5
angle = 360.0/5
sidelen = 250
fillcolor = "blue"

# Set the offset values.
dm0 = 170
dm1 = 120
dang = 90

# Define the turtle object.
ts = turtle.Turtle()
# Hide the turtle.
ts.hideturtle()
# Set the fill color.
ts.fillcolor(fillcolor)
# Pen up.
ts.up()
ts.right(dang)
ts.forward(dm0)
ts.right(dang)
ts.forward(dm1)
# Pen down.
ts.down()
# Begin fill.
ts.begin_fill()
# Start angle.
ts.right(angle)
# Draw the pentagon.
for i in range(0,5):
    ts.forward(sidelen)
    ts.right(angle)
# End fill.
ts.end_fill()

# Save the canvas output
screen.getcanvas().postscript(file=FN0)

# Convert to JPEG format.
Image.open(FN0).convert("RGB").save(FN1)
