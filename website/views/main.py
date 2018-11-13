#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-09-11 23:58:02
# @Author  : Racter (vivi.450@hotmail.com)
# @Link    : https://racterub.me

from flask import request, flash, session, render_template, redirect, url_for, make_response
from website import app
from lxml import etree
import requests
from website.views.lib.crawler import login, getdata

uid = ''


@app.route('/', methods=['POST', 'GET'])
def index():
    global uid, content
    if request.method == "POST":
        if request.form:
            stdid = request.form['stdid']
            stdpwd = request.form['stdpwd']
            status = login(stdid, stdpwd)
            if status == True:
                uid = request.form['stdid']
                session['user'] = request.form['stdid']
                flash('登入成功')
                return render_template('index.html', stdid=uid)
            else:
                info = '帳號密碼錯誤，請再次確認'
                return render_template('index.html', info=info)
        else:
            return "no data" #Create a 400 error template
    else:
        if 'redirect' in session:
            info = session['redirect']
            session.pop('redirect', None)
            return render_template('index.html', info=info)
        elif 'logout' in session:
            info = session['logout']
            session.pop('logout', None)
            return render_template('index.html', info=info)
        else:
            return render_template('index.html', stdid=uid)

@app.route('/scoreboard/<int:counter>')
def scoreboard(counter):
    global uid
    if 'user' in session:
        content = getdata()
        if content == False:
            return render_template('errordata.html', stdid=uid)
        if (counter <= 0 or counter > 3): #Also Harcoded..
            return render_template('errordata.html')
        body = []
        for i in content:
            body.append(i[counter-1])
        #Hardcoded table header :(
        return render_template('scoreboard.html', head=['科目', '成績', '全班平均', '班級排名', '班級人數'], body=body, stdid=uid, count=counter)

    else:
        session['redirect'] = '請先登入系統'
        return redirect(url_for('index'))

@app.route('/logout/')
def logout():
    global uid
    uid = ''
    session.pop('user', None)
    session['logout'] = '已登出系統'
    return redirect(url_for('index'))

@app.route('/api/v1/login', methods=['POST'])
def api_login():
    if request.json:
        stdid = request.json['user']
        stdpwd = request.json['pass']
        if (stdid != None and stdpwd != None):
            if login(stdid, stdpwd):
                return "logged in w/ User: %s Pass: %s" % (stdid, stdpwd)
            else:
                return "error"
        else:
            return "JSON"
    else:
        return "no data"

