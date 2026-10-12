
import math


class GridRenderer:
    def __init__(self, canvas, viewport):
        self.canvas = canvas
        self.viewport = viewport

    def format_coordinate(self, value):
        if abs(value) < 1e-10:
            return "0"

        return f"{value:.10g}"

    def draw(self):
        self.canvas.delete("all")

        self.draw_grid_lines()
        self.draw_axes()
        self.draw_labels()

    def get_grid_indices(self):
        left, right, bottom, top = (
            self.viewport.get_visible_bounds()
        )

        spacing = self.viewport.get_grid_spacing()

        start_x = math.ceil(left / spacing)
        end_x = math.floor(right / spacing)

        start_y = math.ceil(bottom / spacing)
        end_y = math.floor(top / spacing)

        return (
            spacing,
            range(start_x, end_x + 1),
            range(start_y, end_y + 1)
        )

    def draw_grid_lines(self):
        spacing, x_indices, y_indices = (
            self.get_grid_indices()
        )

        for i in x_indices:
            x = i * spacing

            screen_x, _ = (
                self.viewport.math_to_screen(x, 0)
            )

            self.canvas.create_line(
                screen_x, 0,
                screen_x, self.viewport.height,
                fill="#334155"
            )

        for i in y_indices:
            y = i * spacing

            _, screen_y = (
                self.viewport.math_to_screen(0, y)
            )

            self.canvas.create_line(
                0, screen_y,
                self.viewport.width, screen_y,
                fill="#334155"
            )

    def draw_axes(self):
        origin_x, origin_y = (
            self.viewport.math_to_screen(0, 0)
        )

        self.canvas.create_line(
            0, origin_y,
            self.viewport.width, origin_y,
            fill="white",
            width=2
        )

        self.canvas.create_line(
            origin_x, 0,
            origin_x, self.viewport.height,
            fill="white",
            width=2
        )

    def draw_labels(self):
        spacing, x_indices, y_indices = (
            self.get_grid_indices()
        )

        origin_x, origin_y = (
            self.viewport.math_to_screen(0, 0)
        )

        width = self.viewport.width
        height = self.viewport.height

        label_y = max(
            15,
            min(height - 15, origin_y + 18)
        )

        label_x = max(
            25,
            min(width - 25, origin_x - 20)
        )

        for i in x_indices:
            if i == 0:
                continue

            x = i * spacing
            screen_x, _ = (
                self.viewport.math_to_screen(x, 0)
            )

            self.canvas.create_text(
                screen_x,
                label_y,
                text=self.format_coordinate(x),
                fill="white",
                font=("Arial", 10)
            )

        for i in y_indices:
            if i == 0:
                continue

            y = i * spacing
            _, screen_y = (
                self.viewport.math_to_screen(0, y)
            )

            self.canvas.create_text(
                label_x,
                screen_y,
                text=self.format_coordinate(y),
                fill="white",
                font=("Arial", 10),
                anchor="e"
            )

        if 0 <= origin_x <= width and 0 <= origin_y <= height:
            self.canvas.create_text(
                origin_x + 12,
                origin_y + 15,
                text="0",
                fill="white",
                font=("Arial", 10)
            )
