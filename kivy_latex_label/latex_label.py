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
import warnings

# Kivy imports #

from kivy.uix.stacklayout import StackLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    ListProperty,
    AliasProperty,
)
from kivy.clock import Clock

# Dependencies #

from PIL import Image
import matplotlib
matplotlib.set_loglevel("warning")
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

    try:
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
    except ValueError:
        warnings.warn(
            "Unsupported latex command in the given string: " + latex_str, category=SyntaxWarning)
        img = Image.new("RGBA", (5, 10))
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
    font_name = StringProperty("Roboto")
    color = ColorProperty((1, 1, 1, 1))
    line_height = NumericProperty(2)
    _latex_cache = {}
    _state_cache = {}
    variables_in_state_cache = ["text", "font_size",
                                "color", "line_height", "font_name"]
    update_id = NumericProperty(0)
    _is_in_bold_part = False
    _is_in_italic_part = False

    def __init__(self, markup=False, **kwargs):
        self.markup = markup
        super().__init__(**kwargs)
        self.bind(
            text=self.plan_update_content,
            font_size=self.plan_update_content,
            color=self.change_color,
            line_height=self.plan_update_content,
            font_name=self.plan_update_content,
        )
        self.update_content()
        self.change_color()

    def plan_update_content(self, *_, **__):
        Clock.schedule_once(self.update_content, 0.1)

    def remove_content(self):

        # Clean children widget
        children_list = self.children[:]
        for child in children_list:
            self.remove_widget(child)

    def change_color(self, *_, **__):
        for child in self.children:
            child.color = self.color

    def update_content(self, *_, **__):
        # Check if state has changed and skip if not
        do_continue = False
        for variable in self.variables_in_state_cache:
            if variable not in self._state_cache:
                do_continue = True
                break
            else:
                if self._state_cache[variable] != getattr(self, variable):
                    do_continue = True
                    break
        if not do_continue:
            return

        # Remove previous content
        self.remove_content()

        # Split text and equations
        content = split_text_and_equations(self.text)

        # Iterate over the parts
        for content_type, content_str in content:

            if content_type == "text":

                # Split the words
                words_list = content_str.split(" ")

                # Iterate over the words
                for word in words_list:

                    # Build text of the label
                    text = word + " "

                    # Deal with font effects
                    if self.markup:
                        if "[b]" in word:
                            self._is_in_bold_part = True
                        if "[i]" in word:
                            self._is_in_italic_part = True

                        # Apply effect
                        if self._is_in_bold_part:
                            if "[b]" not in text:
                                text = "[b]" + text
                            if "[/b]" not in text:
                                text = text + "[/b]"
                        if self._is_in_italic_part:
                            if "[i]" not in text:
                                text = "[i]" + text
                            if "[/i]" not in text:
                                text = text + "[/i]"

                        if "[/b]" in word:
                            self._is_in_bold_part = False
                        if "[/i]" in word:
                            self._is_in_italic_part = False

                    # Create a label
                    label = CroppedLabel(
                        text=text,
                        color=self.color,
                        height=self.font_size * self.line_height,
                        font_size=self.font_size,
                        font_name=self.font_name,
                        markup=self.markup
                    )

                    # Add the label
                    self.add_widget(label)

            elif content_type == "equation":

                # Create a texture if not in cache
                if content_str not in self._latex_cache:
                    img = render_latex_string(
                        content_str, self.font_size * 0.9)
                    buf2 = io.BytesIO()
                    img.save(buf2, format="png")
                    buf2.seek(0)
                    texture = CoreImage(buf2, ext="png").texture
                    self._latex_cache[content_str] = texture
                else:
                    texture = self._latex_cache[content_str]

                # Create the image
                image = KivyImage(
                    texture=texture,
                    fit_mode="contain",
                    size_hint=(None, None),
                    width=texture.size[0],
                    height=self.font_size * self.line_height,
                    color=self.color
                )

                # Add the image
                self.add_widget(image)

        # Update the state cache
        for variable in self.variables_in_state_cache:
            self._state_cache[variable] = getattr(self, variable)

        # Schedule update id
        Clock.schedule_once(self.increase_update_id)

    def increase_update_id(self, *_):
        self.update_id += 1

    def get_total_width(self, *_):
        """
        Return the sum of the width of all elements of the latex label.

        This is equivalent to the width of the widget if there is no line break.

        Returns
        -------
        int
            Width in pixels.
        """

        total_width = 0
        for child in self.children:
            total_width += child.texture_size[0]

        return total_width

    total_width = AliasProperty(get_total_width, None, bind=[
                                "update_id"], cache=False, rebind=False)
