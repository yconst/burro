#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import threading
import logging
from time import sleep
import os.path

from tornado import httpserver, ioloop, web, websocket, options, escape
from tornado.options import define, options

cl = []

define("port", default=80, help="run on the given port", type=int)
    
class MainHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')


class SocketHandler(websocket.WebSocketHandler): 
    def initialize(self):
        self.thread = None
        self._stop = False

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)
            self.conditional_start_loop()
            logging.info("WS Open")

    def on_message(self, message):
        logging.info("WS Message")
        parsed = escape.json_decode(message)
        if parsed['action'] == "update-index" and parsed['target'] == "pilot":
            self.application.vehicle.set_pilot(parsed["value"]["index"])
            #self.write_message(json.dumps({ 'req' : 'ok' }))
        elif parsed['action'] == "update-data" and parsed['target'] == "record":
            self.application.vehicle.record = parsed["value"]["record"]
            #self.write_message(json.dumps({ 'req' : 'ok' }))
            
    def on_close(self):
        if self in cl:
            cl.remove(self)
            self.stop_loop()
            logging.info("WS Close")

    def conditional_start_loop(self):
        if self.thread is None:
            self.thread = threading.Thread(target = self.loop)
            self._stop = False
            self.thread.start()

    def stop_loop(self):
        if self._stop == False and self.thread is not None:
            self._stop = True

    def loop(self):
        while self._stop == False:
            v = self.application.vehicle
            img64 = v.vision_sensor.capture_base64()
            status = {
                "image" : img64,
                "controls" : { "yaw" : str(v.pilot_yaw), "throttle" : str(v.pilot_throttle)},
                "pilot": { "pilots" : v.list_pilot_names(), "index" : v.selected_pilot_index()},
                "record" : self.application.vehicle.record
            }
            self.write_message(json.dumps(status))
            sleep(0.5)
        self.thread = None
        self._stop = False


class WebRemote(web.Application):
    def __init__(self, vehicle):
        self.vehicle = vehicle
        base_dir = os.path.dirname(__file__)
        web_dir = os.path.join(base_dir, "./frontend")
        settings = {
            'template_path' : web_dir,
            'debug' : True # TODO: Change this before production!!!
        }
        web.Application.__init__(self, [
            web.url(r'/', MainHandler, name="main"),
            web.url(r'/api/v1/ws', SocketHandler, name="ws"),
            web.url(r'/static/(.*)', web.StaticFileHandler, {'path': web_dir}),
        ], **settings)

    def start(self):
        self.listen(options.port)
        self.loop = ioloop.IOLoop.instance()
        self.thread = threading.Thread(target=self.loop.start)
        self.thread.daemon = True
        self.thread.start()
        

if __name__ == "__main__":
    main()
