"""
Package to create labels that combine both text and equations.
"""

###########
# Imports #
###########

# Python imports #

import os

# Kivy imports #

from kivy.lang import Builder

# Local imports #

from .latex_label import (
    CroppedLabel,
    LatexLabel
)

#############
# Constants #
#############

__version__ = "1.0.9"

#########
# Build #
#########


Builder.load_file(os.path.join(os.path.dirname(__file__),
                  "latex_label.kv"), encoding="utf-8")
