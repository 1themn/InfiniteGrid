
import tkinter as tk
from viewport import Viewport
import math
from grid import GridRenderer

WIDTH = 1500
HEIGHT = 1000
SCALE = 50

viewport = Viewport(WIDTH, HEIGHT, SCALE)



root = tk.Tk()
root.title("Infinite Grid")
root.geometry(f"{WIDTH}x{HEIGHT}")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="#101827",
    highlightthickness=0
)

canvas.pack(fill=tk.BOTH, expand=True)



origin_x = WIDTH / 2
origin_y = HEIGHT / 2

renderer = GridRenderer(canvas, viewport)


def draw_grid():
    renderer.draw()




def handle_resize(event):
    viewport.width = event.width
    viewport.height = event.height

    draw_grid()


def format_coordinate(value):
    if abs(value) < 1e-10:
        return "0"

    return f"{value:.10g}"


draw_grid()



last_mouse_x = 0
last_mouse_y = 0


def start_pan(event):
    global last_mouse_x, last_mouse_y

    last_mouse_x = event.x
    last_mouse_y = event.y


def drag_pan(event):
    global last_mouse_x, last_mouse_y

    dx = event.x - last_mouse_x
    dy = event.y - last_mouse_y

    viewport.pan(dx, dy)

    last_mouse_x = event.x
    last_mouse_y = event.y

    draw_grid()






def normalize_delta(delta):
    value = delta & 0xFFFF

    if value >= 32768:
        value -= 65536

    return value


def handle_touchpad_zoom(event):
    delta = normalize_delta(event.delta)

    if delta == 0:
        return

    # Limit unusually large movements
    delta = max(-20, min(20, delta))

    # Smooth proportional zoom
    factor = 1.003 ** delta

    viewport.zoom(event.x, event.y, factor)
    draw_grid()







def handle_mouse_zoom(event):
    if getattr(event, "num", None) == 4:
        factor = 1.1

    elif getattr(event, "num", None) == 5:
        factor = 1 / 1.1

    elif getattr(event, "delta", 0) > 0:
        factor = 1.1

    elif getattr(event, "delta", 0) < 0:
        factor = 1 / 1.1

    else:
        return

    viewport.zoom(event.x, event.y, factor)
    draw_grid()






canvas.bind("<ButtonPress-1>", start_pan)
canvas.bind("<B1-Motion>", drag_pan)

canvas.bind("<TouchpadScroll>", handle_touchpad_zoom)
canvas.bind("<MouseWheel>", handle_mouse_zoom)

# Linux mouse wheel support
canvas.bind("<Button-4>", handle_mouse_zoom)
canvas.bind("<Button-5>", handle_mouse_zoom)

canvas.bind("<Configure>", handle_resize)
root.mainloop()
