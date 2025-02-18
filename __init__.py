# Import the Python modules of the node.
from .nodes.nodes import *

NODE_CLASS_MAPPINGS = {
    "🪲 Turtle Graphics Circle Demo": TurtleGraphicsCircleDemo,
    "🪲 Turtle Graphics Square Demo": TurtleGraphicsSquareDemo,
    "🪲 Turtle Graphics Spiral Demo": TurtleGraphicsSpiralDemo,
    }

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

MESSAGE = "\033[34mTurtle Graphics Demo Nodes: \033[92mLoaded\033[0m" 

# Print message into the terminal window.
print(MESSAGE)
