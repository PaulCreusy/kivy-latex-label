"""
Demo app for the LatexLabel.
"""

###########
# Imports #
###########

# Kivy imports #

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

# Local imports #

from latex_label.latex_label import LatexLabel

#########
# Class #
#########


class DemoApp(App, Widget):
    """
    Demo application for the latex label.
    """

    def build(self):
        """
        Build the application.
        """

        Window.clearcolor = (1, 1, 1, 1)


# Run the application
if __name__ == "__main__":
    DemoApp().run()
