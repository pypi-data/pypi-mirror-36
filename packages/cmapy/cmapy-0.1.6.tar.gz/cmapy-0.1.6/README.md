# cmapy

Use Matplotlib colormaps with OpenCV in Python.

Matplotlib provides a lot of [nice colormaps](https://matplotlib.org/tutorials/colors/colormaps.html). Cmapy exposes these colormaps as lists of colors that can be used with OpenCV to colorize images or for other drawing tasks in Python.

| Original image | ![](./examples/imgs/gradient.png) | ![](./examples/imgs/jupiter.png) | ![](./examples/imgs/woman.png) |
| -- | -- | -- | -- |
|viridis|![](./docs/imgs/gradient_viridis.png)|![](./docs/imgs/jupiter_viridis.png)|![](./docs/imgs/woman_viridis.png)|

See all of the available colormaps as of Matplotlib 2.2.3 in this [all colormaps example](./docs/colorize_all_examples.md).

## Requirements

* Python 3.
* Matplotlib.
* OpenCV >= 3.3.0 (to use cv2.applyColorMap()).

## Installation

```bash
pip3 install cmapy
```

## How to use

### Colorize images

Colorize means to apply a colormap to an image. This is done by calling the cv2.applyColorMap() function with a colormap, like this:

```.py
cv2.applyColorMap(img, cmapy.cmap('viridis'))
```

See the full [colorize example](./examples/colorize.py).

### Draw with colors

TODO: make an example.
