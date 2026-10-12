
import tkinter as tk
from viewport import Viewport
import math


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




def draw_grid():
    canvas.delete("all")

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    left, top = viewport.screen_to_math(0, 0)
    right, bottom = viewport.screen_to_math(width, height)

    spacing = viewport.get_grid_spacing()

    # Vertical grid lines
    start_x = math.ceil(left / spacing)
    end_x = math.floor(right / spacing)

    
    for i in range(start_x, end_x + 1):
        x = i * spacing

        screen_x, _ = viewport.math_to_screen(x, 0)

        # Draw vertical grid line
        canvas.create_line(
            screen_x, 0,
            screen_x, height,
            fill="#334155"
        )

        # Draw coordinate label
        if i != 0:
            label_y = max(
                15,
                min(height - 15, viewport.origin_y + 18)
            )

            canvas.create_text(
                screen_x,
                label_y,
                text=format_coordinate(x),
                fill="white",
                font=("Arial", 10),
                anchor="center"
            )



   

    # Horizontal grid lines
    start_y = math.ceil(bottom / spacing)
    end_y = math.floor(top / spacing)

    
    for i in range(start_y, end_y + 1):
        y = i * spacing

        _, screen_y = viewport.math_to_screen(0, y)

        # Draw horizontal grid line
        canvas.create_line(
            0, screen_y,
            width, screen_y,
            fill="#334155"
        )

        # Draw coordinate label
        if i != 0:
            label_x = max(
                25,
                min(width - 25, viewport.origin_x - 20)
            )

            canvas.create_text(
                label_x,
                screen_y,
                text=format_coordinate(y),
                fill="white",
                font=("Arial", 10),
                anchor="e"
            )



    # Draw axes
    origin_x, origin_y = viewport.math_to_screen(0, 0)

    if 0 <= origin_x <= width and 0 <= origin_y <= height:
        canvas.create_text(
            origin_x + 12,
            origin_y + 15,
            text="0",
            fill="white",
            font=("Arial", 10)
        )
    

    canvas.create_line(
        0, origin_y,
        width, origin_y,
        fill="white", width=2
    )

    canvas.create_line(
        origin_x, 0,
        origin_x, height,
        fill="white", width=2
    )



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


root.mainloop()
