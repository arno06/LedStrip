#!/usr/bin/python3
import os
import logging
import sys
import http.client
import json
import time
from rpi_ws281x import *
from led_strip import Led

class LedStrip():
    def __init__(self):
        self.leds = []
        self.led_count = 300
        self.pixel = Adafruit_NeoPixel(self.led_count, 18, 800000, 10, False, 255, 0)
        self.pixel.begin()
        self.reset()
        for i in range(self.led_count):
            l = Led()
            l.i = i
            l.color_rotation((l.i / (self.led_count - 1)) * 360, 6, 1)
            self.leds.append(l)
        self.mode = 'off'
        self.running = False
        self.date = ''
        self.params = None
        self.runner = []
        self.timer = 0

    def checkState(self):
        conn = http.client.HTTPSConnection('api.arnaud-nicolas.fr')
        try:
            conn.request('GET', '/storage/ledstrip.setup')
            response = conn.getresponse()
        except:
            conn.close()
            logging.debug("Error in query")
            return
        data = response.read()
        conn.close()
        mode = json.loads(data.decode())
        if self.date == mode['date']:
            return
        self.running = False
        self.date = mode['date']
        self.mode = mode['mode']['name']
        if self.mode == Led.MODE_OFF:
            self.reset()
            self.running = False
            return

        self.params = mode['mode']['params']
        if self.mode == Led.MODE_ROTATION:
            for l in self.leds:
                l.color_rotation((l.i / (len(self.leds) - 1)) * 360, self.params['speed'], self.params['direction'])
        self.running = True

    def tickHandler(self):
        while True:
            self.tick()
            self.timer += 0.1
            if self.timer>= 3:
                self.checkState()
                self.timer = 0
            time.sleep(.1)

    def tick(self):
        if not self.running:
            return
        for l in self.leds:
            self.pixel.setPixelColorRGB(l.i, l.r, l.g, l.b, 255)
            l.tick()
        self.pixel.show()

    def reset(self):
        for l in self.leds:
            self.pixel.setPixelColorRGB(l.i, 0, 0, 0, 0)
        self.pixel.show()


if __name__ == '__main__':
    logfile = os.path.join(os.getcwd(), "LedStrip.log")

    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    d = LedStrip()
    try:
        d.tickHandler()
    except KeyboardInterrupt:
        d.reset()
