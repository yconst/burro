#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import threading

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)
       
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        v = self.application.vehicle
        img64 = v.vision_sensor.capture_base64()
        status = {
            "yaw" : str(v.pilot_yaw),
            "throttle" : str(v.pilot_throttle),
            "image" : img64,
            "pilots" : v.list_pilot_names(),
            "selected_pilot" : v.selected_pilot_index()
        }
        self.write(json.dumps(status))

class PilotHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        self.application.vehicle.set_pilot(data["index"])
        self.write(json.dumps({ 'req' : 'ok' }))

class OptionsHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        self.application.vehicle.record = data["record"]
        self.write(json.dumps({ 'req' : 'ok' }))

class WebRemote(tornado.web.Application):
    def __init__(self, vehicle):
        self.vehicle = vehicle
        base_dir = os.path.dirname(__file__)
        web_dir = os.path.join(base_dir, "./frontend")
        settings = {
            'template_path' : web_dir,
            'debug' : True # TODO: Change this before production!!!
        }
        tornado.web.Application.__init__(self, [
            tornado.web.url(r'/', MainHandler, name="main"),
            tornado.web.url(r'/api/v1/status', StatusHandler, name="status"),
            tornado.web.url(r'/api/v1/setpilotindex', PilotHandler, name="setpilot"),
            tornado.web.url(r'/api/v1/setoptions', OptionsHandler, name="setoptions"),
            tornado.web.url(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': web_dir}),
        ], **settings)

    def start(self):
        self.listen(options.port)
        self.loop = tornado.ioloop.IOLoop.instance()
        self.thread = threading.Thread(target=self.loop.start)
        self.thread.daemon = True
        self.thread.start()
        

if __name__ == "__main__":
    main()
