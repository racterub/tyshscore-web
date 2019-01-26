#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-09-11 23:58:02
# @Author  : Racter (vivi.450@hotmail.com)
# @Link    : https://racterub.me

from flask import request, flash, session, render_template, redirect, url_for, make_response, send_from_directory
from website import app
from lxml import etree
import requests
from website.views.lib.crawler import login, get_score

#Initial globs
uid = u''
parent_mode=False
content = []

@app.route('/', methods=['POST', 'GET'])
def index():
    global uid
    global content
    global parent_mode
    if request.method == "POST":
        if request.form:
            stdid = request.form['stdid']
            stdpwd = request.form['stdpwd']
            status = login(stdid, stdpwd)
            if status == True:
                if stdid[-1] == "p":
                    stdid = stdid[:-1]
                    parent_mode = True
                uid = request.form['stdid']
                session['user'] = request.form['stdid']
                content = get_score()
                flash(u"登入成功")
                flash(u"將使用家長模式登入")
                return render_template('index.html', stdid=uid, parent_mode=parent_mode)
            else:
                info = u"帳號密碼錯誤，請再次確認"
                return render_template('index.html', info=info)
        else:
            error_header = u"資料無法處理"
            error_context = u"您的登入資料無法處理，請重新登入"
            return render_template('error.html', stdid=uid, error_header=error_header, error_context=error_context),400
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
            return render_template('index.html', stdid=uid, parent_mode=parent_mode)

@app.route('/scoreboard/<int:counter>')
def scoreboard(counter):
    global uid
    global content
    global parent_mode
    if 'user' in session:
        if (counter <= 0 | counter > 3): #Also Harcoded..
            error_header = u"資料無法處理"
            error_context = u"您所選的資料目前無法處理或是校方系統資料已清空，請稍後再試"
            return render_template('error.html', stdid=uid, error_header=error_header, error_context=error_context, parent_mode=parent_mode), 400
        if content:
            pass
        else:
            content = get_score()
        if content == False:
            return render_template('error.html', stdid=uid, parent_mode=parent_mode)
        body = []
        for i in content:
            body.append(i[counter-1])
        #Hardcoded table header :(
        return render_template('scoreboard.html', head=[u'科目', u'成績', u'全班平均', u'班級排名', u'班級人數'], body=body, stdid=uid, count=counter, parent_mode=parent_mode)

    else:
        session['redirect'] = u'請先登入系統'
        return redirect(url_for('index'))

@app.route('/logout/')
def logout():
    global uid
    uid = ''
    session.pop('user', None)
    session['logout'] = u'已登出系統'
    return redirect(url_for('index'))

@app.route('/robots.txt')
def robotstxt():
    return send_from_directory('static', 'robots.txt')
