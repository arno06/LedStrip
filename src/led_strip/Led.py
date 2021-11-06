from .color_utils import hsl2rgb

class Led:

    MODE_ALTERNATION = 'color_alternation'
    MODE_ROTATION = 'color_rotation'
    MODE_BRIGHTNESS = 'brightness_rotation'
    MODE_OFF = 'off'

    def __init__(self, hue = 0, distance = 6, direction = 1):
        self.hue = hue
        self.i = 0
        self.val = 'O'
        self.brightness = 1
        self.distance = distance
        self.set_hue(self.hue)
        self.direction = direction
        self.colors = []
        self.index = 0
        self.mode = Led.MODE_ROTATION

    def color_alternation(self, colors = [], start_index = 0):
        self.mode = Led.MODE_ALTERNATION
        self.colors = colors
        self.index = start_index
        self.set_hue(self.colors[self.index])

    def brightness_rotation(self, r, g, b, brightness=1):
        self.r = r
        self.g = g
        self.b = b
        self.brightness = brightness
        self.mode = Led.MODE_BRIGHTNESS

    def color_rotation(self, hue = 0, distance = 6, direction = 1):
        self.set_hue(hue)
        self.direction = direction
        self.distance = distance
        self.mode = Led.MODE_ROTATION

    def tick(self):
        self.val = "\x1b[38;2;"+str(self.r)+";"+str(self.g)+";"+str(self.b)+"m" + "O"
        if self.mode == Led.MODE_ROTATION:
            self.set_hue(self.hue + (self.distance * self.direction))
        if self.mode == Led.MODE_ALTERNATION:
            if self.index > len(self.colors) -1:
                self.index = 0
            self.set_hue(self.colors[self.index])
            self.index += 1
        if self.mode == Led.MODE_BRIGHTNESS:
            self.brightness = self.brightness + 0.05
            if self.brightness > 1:
                self.brightness = 0


    def set_hue(self, hue):
        self.hue = hue
        if self.hue > 360:
            self.hue = 0
        if self.hue < 0:
            self.hue = 360
        c = hsl2rgb(self.hue / 360, 1, .5)
        self.r = round(c['r'])
        self.g = round(c['g'])
        self.b = round(c['b'])
