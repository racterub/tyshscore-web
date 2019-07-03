#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-04 23:40:36
# @Author  : Racter (vivi.450@hotmail.com)
# @Profile    : https://racterub.me


from website import app
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        port = int(os.environ.get("PORT", 5000))
    else:
        if sys.argv[1] == 'dev':
            print('Running in Debug mode')
            app.config['DEBUG'] = True
            port = 6969
        else:
            print('Usage: ./%s (dev)' % sys.argv[0])
            sys.exit(1)
    app.run(host='0.0.0.0', port=port, threaded=True)

