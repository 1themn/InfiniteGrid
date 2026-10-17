# InfiniteGrid
InfiniteGrid is an interactive Cartesian coordinate grid built from scratch with **Python and Tkinter**. It supports dragging to move around the plane, zooming around the cursor, and automatically adjusting grid lines and coordinate labels as the view changes.

The goal of this project was to understand the mathematics and rendering logic behind an interactive graph, rather than rely on a plotting library to draw the grid.

## Features

- **Panning:** Drag the grid to explore different coordinates.
- **Cursor-centered zooming:** Zoom toward the position of the mouse pointer rather than the center of the window.
- **Coordinate transformations:** Convert between mathematical coordinates and Canvas pixel positions.
- **Adaptive grid spacing:** Select readable intervals using a `1–2–5` sequence.
- **Dynamic axes and labels:** Recalculate axis positions and coordinate markings as the view changes.
- **Visible-area rendering:** Draw only the grid lines needed for the current viewport.
- **Zoom bounds:** Limit extreme scales to avoid impractical rendering and numerical issues.

## How the Grid Works

The grid isn't stored as an endless collection of lines. Instead, the program maintains a **viewport**: the current origin and scale of the mathematical plane as seen through the Tkinter Canvas.

When the user pans or zooms, the program updates that viewport, determines which mathematical coordinates are visible, and draws the appropriate lines again.

### 1. Mathematical Coordinates vs. Screen Coordinates

In a Cartesian plane, positive `y` points **up**. On a Tkinter Canvas, pixel coordinates start at the **top-left**, so positive `y` points **down**.

The viewport bridges these two coordinate systems:

```python
# Mathematical coordinates -> screen pixels
def math_to_screen(self, x, y):
    screen_x = self.origin_x + x * self.scale
    screen_y = self.origin_y - y * self.scale
    return screen_x, screen_y

# Screen pixels -> mathematical coordinates
def screen_to_math(self, screen_x, screen_y):
    x = (screen_x - self.origin_x) / self.scale
    y = (self.origin_y - screen_y) / self.scale
    return x, y
```

Here, `origin_x` and `origin_y` tell us where `(0, 0)` appears on the screen, while `scale` tells us how many pixels represent one mathematical unit.

For example, with an origin at `(500, 350)` and a scale of `50` pixels/unit, the point `(3, 2)` appears at `(650, 250)` on the Canvas.

### 2. Panning

Panning doesn't change the mathematical coordinates themselves. It simply shifts the **screen position of the origin**.

```python
def pan(self, dx, dy):
    self.origin_x += dx
    self.origin_y += dy
```

The mouse-drag handler measures how far the pointer has moved in pixels and passes that difference to the viewport. The grid is then redrawn using the updated origin.

### 3. Zooming Around the Cursor

Zooming changes the number of pixels per mathematical unit. To make the interaction feel natural, the mathematical point under the cursor should stay under the cursor after zooming.

One way to achieve that is to find the mathematical coordinate beneath the cursor **before** changing the scale, then reposition the origin afterward:

```python
def zoom(self, mouse_x, mouse_y, factor):
    new_scale = self.scale * factor

    if new_scale < 0.01 or new_scale > 10000:
        return

    math_x, math_y = self.screen_to_math(mouse_x, mouse_y)

    self.scale = new_scale
    self.origin_x = mouse_x - math_x * self.scale
    self.origin_y = mouse_y + math_y * self.scale
```

A zoom factor greater than `1` zooms in; a factor between `0` and `1` zooms out. Mouse-wheel and trackpad events need to be converted into suitable factors. Handling macOS trackpad scroll values was one of the debugging challenges during development.

### 4. Adaptive Grid Spacing

If we always draw a line at every integer coordinate, the grid becomes too crowded when zoomed out and too sparse when zoomed in.

Instead, InfiniteGrid uses a **target spacing** of about `75` pixels and chooses a convenient mathematical interval from the `1–2–5` sequence:

`..., 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, ...`

```python
import math

def get_grid_spacing(scale, target_pixels=75):
    raw_spacing = target_pixels / scale
    magnitude = 10 ** math.floor(math.log10(raw_spacing))
    normalized = raw_spacing / magnitude

    for step in (1, 2, 5, 10):
        if normalized <= step:
            return step * magnitude
```

For example, at `50` pixels/unit:

```text
Ideal interval = 75 / 50 = 1.5 mathematical units
Selected interval = 2 mathematical units
Actual distance between lines = 2 × 50 = 100 pixels
```

The target stays at `75` pixels, but the **actual** spacing can be larger. As the scale changes, the chosen mathematical interval stays the same for a while, then switches when it crosses a threshold. This is why new lines appear as you zoom in.

### 5. Drawing Only Visible Lines

Rather than generate an enormous grid, we first convert the Canvas boundaries into mathematical coordinates. We can then calculate which multiples of the selected interval fall within that visible range.

```python
# Illustrative example for vertical grid lines
left, _ = viewport.screen_to_math(0, 0)
right, _ = viewport.screen_to_math(canvas_width, 0)

start = math.floor(left / spacing)
end = math.ceil(right / spacing)

for index in range(start, end + 1):
    math_x = index * spacing
    screen_x, _ = viewport.math_to_screen(math_x, 0)
    canvas.create_line(screen_x, 0, screen_x, canvas_height)
```

Horizontal lines follow the same idea using the visible `y` range. The axes and coordinate labels are drawn based on their updated screen positions.

### 6. Redrawing After Interaction

Each accepted zoom or pan event updates the viewport and triggers a redraw:

```text
Mouse / trackpad event
        ↓
Update scale or origin
        ↓
Find visible mathematical bounds
        ↓
Choose adaptive grid interval
        ↓
Calculate visible line positions
        ↓
Draw grid, axes, and labels
```

Even when the selected interval doesn't change, the pixel positions of the lines do, so the grid still needs to be redrawn.

## Technologies

- **Python** — application logic and mathematical calculations
- **Tkinter Canvas** — drawing the grid and handling interaction
- **Python `math` module** — logarithms, rounding, and grid intervals

## What's Next?

**MathVision** will use InfiniteGrid as its interactive coordinate plane for plotting mathematical equations.
