#!/usr/bin/python
#coding: utf-8

import json
import os
import sys
import time
import traceback

import tornado.ioloop
import tornado.options
import tornado.web

from conf import config
from conf import retcode
from lib.log_helper import MyLogger
from logic import admin_logic
from logic import interface_logic


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            MyLogger().getlogger().error(traceback.format_exc())
            # in debug mode, try to send a traceback
            if self.settings.get('debug'):
                for line in traceback.format_exception(*kwargs['exc_info']):
                    self.write(line + '<br />')
            self.finish()
        else:
            self.finish('Bad guy!!!!')

class MainHandler(BaseHandler):
    def get(self):
        self.redirect('./index.html')
        
class LoginHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('user', 'xxxxxxxx')
        resp = {}
        resp['ret'] = retcode.OK
        resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
        jsonstr = json.dumps(resp)
        self.set_header('Content-Type', 'application/json')
        self.write(jsonstr)

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('user')
        ret = 0
        resp = {}
        resp['ret'] = ret
        resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
        jsonstr = json.dumps(resp)
        self.set_header('Content-Type', 'application/json')
        self.write(jsonstr)

class InterfaceMainHandler(BaseHandler):
    def get(self):
        MyLogger().getlogger().critical('Ileggal intrution!')
        if ('signature' not in self.request.arguments or
           'timestamp' not in self.request.arguments or
           'nonce' not in self.request.arguments or
           'echostr' not in self.request.arguments):
            return

        # check signature
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        if not interface_logic.check_signature(signature, timestamp, nonce, config.OA_TOKEN):
            MyLogger().getlogger().critical('Ileggal intrution!')
            return

        self.write(echostr)

    def post(self):
        if ('signature' not in self.request.arguments or
           'timestamp' not in self.request.arguments or
           'nonce' not in self.request.arguments): 
            return

        # check signature
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        if not interface_logic.check_signature(signature, timestamp, nonce, config.OA_TOKEN):
            MyLogger().getlogger().critical('Ileggal intrution!')
            return

        # parse msg
        msg = self.request.body
        MyLogger().getlogger().info('Recv msg: ' + msg)
        msgdict = msg_helper.parse_input_msg(msg)

        # check if send to the right oa
        to_user_name = msg_helper.get_value_by_key(msgdict, 'ToUserName')
        if to_user_name != config.OA_USERNAME:
            MyLogger().getlogger().critical('Send to the wrong official account!')
            return

        # process msg
        reply_msg = interface_logic.process_msg(msgdict)
        if reply_msg != None:
            MyLogger().getlogger().info('Reply msg: ' + reply_msg)
            self.write(reply_msg)
            return

class UserViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if ('id' not in self.request.arguments):
            resp = {}
            resp['ret'] = retcode.MISS_ARGUMENT
            resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
            jsonstr = json.dumps(resp)
            self.set_header('Content-Type', 'application/json')
            self.write(jsonstr)
            return

        id = int(self.get_argument('id'))

        if (id < 0):
            resp = {}
            resp['ret'] = retcode.INVALID_ARGUMENT_VALUE
            resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
            jsonstr = json.dumps(resp)
            self.set_header('Content-Type', 'application/json')
            self.write(jsonstr)
            return

        ret, data = admin_logic.view_user(id)
        
        resp = {}
        resp['ret'] = ret
        resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
        resp['data'] = data 
        jsonstr = json.dumps(resp)
        self.set_header('Content-Type', 'application/json')
        self.write(jsonstr)
        

