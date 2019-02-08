#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-09-11 23:58:02
# @Author  : Racter (vivi.450@hotmail.com)
# @Link    : https://racterub.me


from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

from website.views import main


@app.errorhandler(404)
def not_found(error):
    context = "404 Not Found"
    return render_template('errcode.html', context=context), 404
