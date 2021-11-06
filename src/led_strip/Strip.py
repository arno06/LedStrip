from .set_interval import set_interval
from .Led import Led
import logging

class Strip:

    def __init__(self, led_count):
        self.leds = []
        #self.neo_pixel = Adafruit_NeoPixel(led_count, 18, 800000, 10, False, 255, 0)
        #self.neo_pixel.begin()
        for i in range(led_count):
            l = Led()
            l.i = i
            self.leds.append(l)
        self.mode = 'default'
        self.running = False
        self.date = ''
        self.params = None

    @set_interval(.1)
    def tick(self):
        if not self.running:
            return
        for l in self.leds:
            l.tick()
            #self.neo_pixel.setPixelColorRGB(l.i, l.r, l.g, l.b, 255)
        #self.neo_pixel.show()
        logging.debug("tick")


    def set_mode(self, mode):
        if self.date == mode['date']:
            return
        self.running = False
        self.reset()
        self.date = mode['date']
        self.mode = mode['mode']['name']
        self.params = mode['mode']['params']
        if self.mode == Led.MODE_ROTATION:
            for l in self.leds:
                l.color_rotation((l.i/(len(self.leds)-1)) * 360, self.params['speed'], self.params['direction'])
        self.running = True


    def reset(self):
        #for l in self.leds:
            #self.neo_pixel.setPixelColorRGB(l.i, 0, 0, 0, 0)
        #self.neo_pixel.show()
        logging.debug("reset")