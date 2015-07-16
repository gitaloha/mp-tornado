#!/usr/bin/python
#coding: utf-8

import os
# Change path to current file path
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import tornado.ioloop
import tornado.options
import tornado.web

from comm import mysql_instance
from conf import config
from lib.log_helper import MyLogger
from service import main_service


tornado.options.define('port', default=config.TORNADO_PORT, help='run on the given port', type=int)

def main():
    settings = {
        'cookie_secret': '66oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
        'login_url': config.CGI_BIN_ACCESS_PATH_PREFIX + r'/admin/login',
        'debug': True,
    }

    app = tornado.web.Application([
        (config.STATIC_FILE_ACCESS_PATH_PREFIX + r'/(.+)', tornado.web.StaticFileHandler, {'path':os.path.join(os.path.dirname(__file__), 'static')}),
        (config.STATIC_FILE_ACCESS_PATH_PREFIX + r'/', main_service.MainHandler),

        (config.CGI_BIN_ACCESS_PATH_PREFIX + r'/admin/login', main_service.LoginHandler),
        (config.CGI_BIN_ACCESS_PATH_PREFIX + r'/admin/logout', main_service.LogoutHandler),
        (config.CGI_BIN_ACCESS_PATH_PREFIX + r'/interface/main', main_service.InterfaceMainHandler),

        (config.CGI_BIN_ACCESS_PATH_PREFIX + r'/user/view', main_service.UserViewHandler),

        ], **settings)

    # Initialize mysql manager here to avoid connect database everytime. 
    mysql_instance.MySQLMgr()

    # Get port from command line
    tornado.options.parse_command_line()
    port = tornado.options.options.port

    # Init logger
    MyLogger().setlogger('fr.p%s' % port)

    # Start server
    app.listen(port, address=config.TORNADO_IP)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()


