# Import the user defined Python modules of the node.
from .nodes.nodes import *
from .nodes.rotated_pentagram import *
from .nodes.rotated_nstar import *
from .nodes.sierpinski_curve import *
from .nodes.rotated_ellipse import *
from .nodes.spirograph import *
from .nodes.epitrochoid import *

# Define the node class mappings.
NODE_CLASS_MAPPINGS = {
    "🪲 Turtle Graphics Circles Demo": TurtleGraphicsCirclesDemo,
    "🪲 Turtle Graphics Circle Lobes Demo": TurtleGraphicsCircleLobesDemo,  
    "🪲 Turtle Graphics Squares Demo": TurtleGraphicsSquaresDemo,
    "🪲 Turtle Graphics Spiral Demo": TurtleGraphicsSpiralDemo,
    "🪲 Turtle Graphics Concate Lines Demo": TurtleGraphicsConcateLinesDemo,
    "🪲 Turtle Graphics Rotated Pentagram Demo": TurtleGraphicsRotatedPentagramDemo,
    "🪲 Turtle Graphics Rotated Nstar Demo": TurtleGraphicsRotatedNstarDemo,
    "🪲 Turtle Graphics Sierpinski Curve": TurtleGraphicsSierpinskiCurveDemo,
    "🪲 Turtle Graphics Rotated Ellipse": TurtleGraphicsRotatedEllipseDemo,
    "🪲 Turtle Graphics Spirograph": TurtleGraphicsSpirographDemo,
    "🪲 Turtle Graphics Epitrochoid": TurtleGraphicsEpitrochoidDemo,
    }

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

# Define the message.
MESSAGE = "\033[34mTurtle Graphics Demo Nodes: \033[92mLoaded\033[0m" 

# Print message into the terminal window.
print(MESSAGE)
