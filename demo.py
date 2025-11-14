"""
Demo app for the LatexLabel.
"""

###########
# Imports #
###########

# Kivy imports #

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window, Clock

# Local imports #

from kivy_latex_label import LatexLabel

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

    def print_total_width(self, *_):
        print("total width :",
              self.root_window.children[0].ids.sindy.total_width)

    def on_start(self):
        Clock.schedule_once(self.print_total_width, 1)
        return super().on_start()


# Run the application
if __name__ == "__main__":
    DemoApp().run()
