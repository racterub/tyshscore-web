#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-04 23:42:56
# @Author  : Racter (vivi.450@hotmail.com)
# @Profile    : https://racterub.me


import datetime
import os

#For development
#DEBUG = True
DEBUG = False

SECRET_KEY = os.urandom(24)


if DEBUG:
	PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=1000)
else:
	PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=5)

