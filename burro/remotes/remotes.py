#-*- coding:utf-8 -*-

import json
import threading
import logging
from time import sleep
import os.path

from tornado import httpserver, ioloop, web, websocket, options, escape
from tornado.options import define, options

import methods

cl = []

define("port", default=80, help="run on the given port", type=int)


class MainHandler(web.RequestHandler):

    def get(self):
        self.render('index.html')


class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)
            self.send_settings()
            self.send_status()
            logging.info("WS Open")

    def on_message(self, message):
        parsed = escape.json_decode(message)
        if parsed['action'] == "get" and parsed['target'] == "status":
            self.send_status()
        if parsed['action'] == "get" and parsed['target'] == "settings":
            self.send_settings()
        elif parsed['action'] == "set" and parsed['target'] == "pilot":
            self.application.vehicle.set_pilot(parsed["value"]["index"])
            self.write_message(json.dumps({'ack': 'ok'}))
        elif parsed['action'] == "set" and parsed['target'] == "record":
            self.application.vehicle.record = parsed["value"]["record"]
            self.write_message(json.dumps({'ack': 'ok'}))

    def on_close(self):
        if self in cl:
            cl.remove(self)
            logging.info("WS Close")

    def send_status(self):
        v = self.application.vehicle
        img64 = v.vision_sensor.base64()
        status = {
            "image": img64,
            "controls": {
                "angle": v.pilot_angle,
                "yaw": str(
                    methods.angle_to_yaw(
                        v.pilot_angle)),
                "throttle": str(
                    v.pilot_throttle)},
            "pilot": {
                "pilots": v.list_pilot_names(),
                "index": v.selected_pilot_index()},
            "record": v.record,
            "is_recording": v.recorder.is_recording,
            "f_time": v.f_time
        }
        self.write_message(json.dumps(status))

    def send_settings(self):
        settings = {
            "test": "foo"
        }
        self.write_message(json.dumps(settings))


class WebRemote(web.Application):

    def __init__(self, vehicle):
        self.vehicle = vehicle
        base_dir = os.path.dirname(__file__)
        web_dir = os.path.join(base_dir, "./frontend")
        settings = {
            'template_path': web_dir,
            'debug': True  # TODO: Change this!!!
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
