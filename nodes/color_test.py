import webcolors
import re

def color_to_rgb(color):
    if color == 'none' or isinstance(color, (list, tuple)):
        rgb = color
    elif re.match('#', color):
        rgb = webcolors.hex_to_rgb(color)
    else:
        rgb = webcolors.name_to_rgb(color)
    r,g,b = rgb[0], rgb[1], rgb[2]
    return r,g,b

print(color_to_rgb('#ff0000'))
