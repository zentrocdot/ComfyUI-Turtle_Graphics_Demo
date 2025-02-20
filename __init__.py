# Import the user defined Python modules of the node.
from .nodes.nodes import *

# Define the node class mappings.
NODE_CLASS_MAPPINGS = {
    "🪲 Turtle Graphics Spiral Demo": TurtleGraphicsSpiralDemo,
    "🪲 Turtle Graphics Circle Demo": TurtleGraphicsCircleDemo,
    "🪲 Turtle Graphics Helix Demo": TurtleGraphicsHelixDemo,
    "🪲 Turtle Graphics Square Demo": TurtleGraphicsSpuareDemo,
    "🪲 Turtle Graphics Propeller Demo": TurtleGraphicsPropellerDemo,
    }

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

# Define the message.
MESSAGE = "\033[34mTurtle Graphics Demo Nodes: \033[92mLoaded\033[0m" 

# Print message into the terminal window.
print(MESSAGE)
