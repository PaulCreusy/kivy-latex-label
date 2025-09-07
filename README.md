# Kivy LaTeX Label

![PyPI - Version](https://img.shields.io/pypi/v/kivy-latex-label)![PyPI - Downloads](https://img.shields.io/pypi/dm/kivy-latex-label)

This is a simple package that provides a special LatexLabel class to display text containing equations with kivy. No LaTeX installation is required, the rendering is performed using matplotlib.

## Installation

To use this widget, you can simply copy and paste the "kivy_latex_label" folder in your code and import the widget. A pip installation will possible in the future.

## How to use it

You can use the LatexLabel as any other Label in kivy (although all options may not be available), your equations just need to be delimited by dollar symbols ($) like in any LaTeX document.

Here is a short demo with a python and kv files. To run it, the python should be pasted in a file called "demo.py" and the kv in "demo.kv".

```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy_latex_label import LatexLabel

class DemoApp(App, Widget):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)

if __name__ == "__main__":
    DemoApp().run()
```

```kv
#:kivy 2.0.0

FloatLayout:
    size_hint: (1,1)

    LatexLabel:
        pos_hint: {"top":1,"x":0.05}
        size_hint:(0.9,1)
        text: r"The SINDy method is a recently developed technique that leverages sparse regression to identify the governing equations from a given time series (Figure 1). We consider a system with state $\boldsymbol{x}(t)=\left[x_{1}(t), x_{2}(t), \ldots x_{d}(t)\right]^{\top} \in$ $\mathbb{R}^{d}$ governed by the differential equation: $\dot{\boldsymbol{x}}=\boldsymbol{f}(\boldsymbol{x})$."
        color: (0,0,0,1)
        text_size: root.size
        valign: "top"
        font_size: 20
```

Here is how it looks like: 

<img width="820" height="655" alt="image" src="https://github.com/user-attachments/assets/dc86ffd9-0316-4a73-9810-69a027c00dce" />

