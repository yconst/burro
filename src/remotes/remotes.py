#-*- coding:utf-8 -*-

'''

remotes.py

Websocket server for car telemetry

'''

import json
import threading
import logging
import os.path

from tornado import ioloop, web, websocket, escape
from tornado.options import define, options

import methods

WS_HANDLERS = []

define("port", default=80, help="run on the given port", type=int)

class MainHandler(web.RequestHandler):
    '''
    Main Tornado handler
    '''
    def get(self):
        '''
        Serves the index file
        '''
        self.render('index.html')


class SocketHandler(websocket.WebSocketHandler):
    '''
    Handler for Websocket connections
    '''
    def check_origin(self, origin):
        '''
        Check origin
        '''
        return True

    def open(self):
        '''
        Called when the Websocket connection opens
        '''
        if self not in WS_HANDLERS:
            WS_HANDLERS.append(self)
            self.send_settings()
            self.send_status()
            logging.info("WS Open")

    def on_message(self, message):
        '''
        Called when the Websocket connection receives a message
        '''
        logging.info("WS Message")
        parsed = escape.json_decode(message)
        if parsed['action'] == "get" and parsed['value'] == "status":
            self.send_status()
        if parsed['action'] == "get" and parsed['value'] == "settings":
            self.send_settings()
        elif parsed['action'] == "update-index" and parsed['target'] == "pilot":
            self.application.vehicle.set_pilot(parsed["value"]["index"])
            self.write_message(json.dumps({'ack': 'ok'}))
        elif parsed['action'] == "update-data" and parsed['target'] == "record":
            self.application.vehicle.record = parsed["value"]["record"]
            self.write_message(json.dumps({'ack': 'ok'}))

    def on_close(self):
        '''
        Called when the Websocket connection closes
        '''
        if self in WS_HANDLERS:
            WS_HANDLERS.remove(self)
            logging.info("WS Close")

    def send_status(self):
        '''
        Collects and sends status via a websocket message
        '''
        vehicle = self.application.vehicle
        img64 = vehicle.vision_sensor.capture_base64()
        status = {
            "image": img64,
            "controls": {"angle": vehicle.pilot_angle,
                         "yaw": str(methods.angle_to_yaw(vehicle.pilot_angle)),
                         "throttle": str(vehicle.pilot_throttle)},
            "pilot": {"pilots" : vehicle.list_pilot_names(), 
                      "index" : vehicle.selected_pilot_index()},
            "record": vehicle.record,
            "is_recording": vehicle.recorder.is_recording
        }
        self.write_message(json.dumps(status))

    def send_settings(self):
        '''
        Collects and sends frontend settings via a websocket message
        '''
        settings = {
            "test": "foo"
        }
        self.write_message(json.dumps(settings))


class WebRemote(web.Application):
    '''
    Tornado application
    '''
    def __init__(self, vehicle):
        self.thread = None
        self.loop = None
        self.vehicle = vehicle
        base_dir = os.path.dirname(__file__)
        web_dir = os.path.join(base_dir, "./frontend")
        settings = {
            'template_path' : web_dir,
            'debug' : True # TODO: Change this!!!
        }
        web.Application.__init__(self, [
            web.url(r'/', MainHandler, name="main"),
            web.url(r'/api/v1/ws', SocketHandler, name="ws"),
            web.url(r'/static/(.*)', web.StaticFileHandler, {'path': web_dir}),
        ], **settings)

    def start(self):
        '''
        Start the Tornado server
        '''
        self.listen(options.port)
        self.loop = ioloop.IOLoop.instance()
        self.thread = threading.Thread(target=self.loop.start)
        self.thread.daemon = True
        self.thread.start()
