"""
Module to define a label able to plot both text and equations.
"""

###########
# Imports #
###########

# Python imports #

import re
import io
from typing import Literal

# Kivy imports #

from kivy.uix.stacklayout import StackLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty
)

# Dependencies #

from PIL import Image
import matplotlib.pyplot as plt
plt.rcParams.update({"mathtext.fontset": "cm"})


#############
# Functions #
#############

def split_text_and_equations(text: str) -> list[tuple[Literal["text", "equation"], str]]:
    """
    Split a text into its text and equations.

    Parameters
    ----------
    text : str
        Text.

    Returns
    -------
    list[tuple[Literal["text","equation"],str]]
        List of tuples containing a type and the content for each split.
    """

    # Pattern to match equations
    pattern = r'(\$.*?\$)'

    # Split the text while keeping the matches
    parts = re.split(pattern, text)

    res = []

    for part in parts:
        if part.startswith('$') and part.endswith('$'):
            # Remove the $ symbols and mark as equation
            res.append(('equation', part[1:-1]))
        elif part:
            # Non-empty text
            res.append(('text', part))

    return res


def render_latex_string(latex_str: str, font_size: float):
    """
    Render a latex string into an image.

    Parameters
    ----------
    latex_str : str
        LaTeX string to render.
    font_size : float
        Font size to use.

    Returns
    -------
    PIL.Image
        Pillow image
    """

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.text(0.5, 0.5, f"${latex_str}$", fontsize=font_size,
            ha="center", va="center", color=(1., 1., 1., 1.))
    buf = io.BytesIO()
    plt.savefig(
        buf,
        format="png",
        bbox_inches="tight",
        pad_inches=0.0,
        transparent=True
    )
    plt.close(fig)
    buf.seek(0)

    img = Image.open(buf).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    return img


###########
# Classes #
###########


class CroppedLabel(Label):
    """
    Class to define a label that is sized exactly like its text content.
    """


class LatexLabel(StackLayout):
    """
    Class to define a label that can display both text and equations.
    """

    text = StringProperty()
    font_size = NumericProperty(11)
    color = ColorProperty((1, 1, 1, 1))
    line_height = NumericProperty()
    _latex_cache = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            text=self.update_content,
            font_size=self.update_content,
            color=self.change_color,
        )

    def remove_content(self):
        children_list = self.children[:]
        for child in children_list:
            self.remove_widget(child)

    def change_color(self, *_, **__):
        for child in self.children:
            child.color = self.color

    def update_content(self, *_, **__):
        # Remove previous content
        self.remove_content()

        # Update line height
        self.line_height = self.font_size * 2

        # Split text and equations
        content = split_text_and_equations(self.text)

        # Iterate over the parts
        for content_type, content_str in content:

            if content_type == "text":

                # Split the words
                words_list = content_str.split(" ")

                # Iterate over the words
                for word in words_list:

                    # Create a label
                    label = CroppedLabel(
                        text=word + " ",
                        color=self.color,
                        height=self.line_height,
                        font_size=self.font_size
                    )

                    # Add the label
                    self.add_widget(label)

            elif content_type == "equation":

                # Create a texture if not in cache
                img = render_latex_string(
                    content_str, self.font_size * 0.9)
                buf2 = io.BytesIO()
                img.save(buf2, format="png")
                buf2.seek(0)
                texture = CoreImage(buf2, ext="png").texture

                # Create the image
                image = KivyImage(
                    texture=texture,
                    fit_mode="contain",
                    size_hint=(None, None),
                    width=texture.size[0],
                    height=self.line_height,
                    color=self.color
                )

                # Add the image
                self.add_widget(image)
