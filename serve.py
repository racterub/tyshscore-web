#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-04 23:40:36
# @Author  : Racter (vivi.450@hotmail.com)
# @Profile    : https://racterub.me


from website import app
import os

if __name__ == '__main__':
    if app.config['DEBUG']:
        port = 6969
    else:
        port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

