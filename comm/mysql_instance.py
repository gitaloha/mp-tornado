#!/usr/bin/python
#coding: utf-8

import os
import sys
import torndb

from conf import config
from lib import singleton


@singleton.singleton
class MySQLMgr(object):
    """ MySQL Database manager instance, global unique. """
    
    def __init__(self):
        """ Initialize torndb instance. """
        self.__db = torndb.Connection(config.MYSQL_DB_HOST, config.MYSQL_DB_DBNAME, config.MYSQL_DB_USER, config.MYSQL_DB_PASSWD)

    def getdb(self):
        """ Return db handler. """
        return self.__db

