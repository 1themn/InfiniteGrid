import math

class Viewport:
    def __init__(self, width, height, scale=50):
        self.width = width
        self.height = height
        self.scale = scale

        self.origin_x = width / 2
        self.origin_y = height / 2

    def math_to_screen(self, x, y):
        screen_x = self.origin_x + x * self.scale
        screen_y = self.origin_y - y * self.scale

        return screen_x, screen_y

    def screen_to_math(self, screen_x, screen_y):
        x = (screen_x - self.origin_x) / self.scale
        y = (self.origin_y - screen_y) / self.scale

        return x, y
    
    def pan(self, dx, dy):
        self.origin_x += dx
        self.origin_y += dy


    def zoom(self, mouse_x, mouse_y, factor):
        old_scale = self.scale
        new_scale = old_scale * factor

        # Prevent extreme zoom levels
        if new_scale < 0.01 or new_scale > 10000:
            return

        ratio = new_scale / old_scale

        self.origin_x = mouse_x - (
            mouse_x - self.origin_x
        ) * ratio

        self.origin_y = mouse_y - (
            mouse_y - self.origin_y
        ) * ratio

        self.scale = new_scale

    def get_grid_spacing(self, target_pixels=75):
        # Ideal mathematical spacing
        raw_spacing = target_pixels / self.scale

        # Find the power of 10
        magnitude = 10 ** math.floor(
            math.log10(raw_spacing)
        )

        # Normalize to a number between 1 and 10
        normalized = raw_spacing / magnitude

        # Select a readable interval
        if normalized <= 1:
            nice_spacing = 1
        elif normalized <= 2:
            nice_spacing = 2
        elif normalized <= 5:
            nice_spacing = 5
        else:
            nice_spacing = 10

        return nice_spacing * magnitude
    

    def get_visible_bounds(self):
        left, top = self.screen_to_math(0, 0)

        right, bottom = self.screen_to_math(
            self.width,
            self.height
        )

        return left, right, bottom, top


