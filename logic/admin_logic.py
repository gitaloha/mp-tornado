#!/usr/bin/python
#coding: utf-8

import datetime
import hashlib
import json 
import os
import time
import sys

from conf import retcode
from lib.log_helper import MyLogger
from model import user_model


def view_user(id):
    """"""
    MyLogger().getlogger().info("ENTRANCE id: %d", id)
    
    result = user_model.UserModel().get_one(id)    
    if result is None:        
        ret = retcode.USER_ID_NOT_EXIST        
        data = {}        
        MyLogger().getlogger().error("player not exist:%d", id)        
        return (ret, data)

    ret = 0
    data = result

    MyLogger.getlogger().info("RETURN ret:%s, data:%s", ret, str(data))
    return (ret, data)
    

