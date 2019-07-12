#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-09-11 23:58:02
# @Author  : Racter (vivi.450@hotmail.com)
# @Link    : https://racterub.me

from flask import request, flash, session, render_template, redirect, url_for, make_response, send_from_directory
from website import app
from lxml import etree
import requests
from website.views.lib.crawler import login, get_term_score, get_history_pr
import json

#Initial globs
uid = u''
commit = ''

def getLastCommit():
    global commit
    r = requests.get('https://api.github.com/repos/racterub/tyshscore-web/commits/master')
    data = json.loads(r.text)
    commit = data['sha'][:6]


@app.route('/', methods=['POST', 'GET'])
def index():
    global uid, commit
    if not commit:
        getLastCommit()
    if request.method == "POST":
        if request.form:
            stdid = request.form['stdid']
            stdpwd = request.form['stdpwd']
            status = login(stdid, stdpwd)
            if status:
                uid = request.form['stdid']
                session['user'] = request.form['stdid']
                flash(u"登入成功")
                return render_template('index.jinja.html', stdid=uid, commit=commit)
            else:
                info = u"帳號密碼錯誤，請再次確認"
                return render_template('index.jinja.html', info=info, commit=commit)
        else:
            error_header = u"資料無法處理"
            error_context = u"您的登入資料無法處理，請重新登入"
            return render_template('error.jinja.html', stdid=uid, error_header=error_header, error_context=error_context, commit=commit),400
    else:
        if 'redirect' in session:
            info = session['redirect']
            session.pop('redirect', None)
            return render_template('index.jinja.html', info=info, commit=commit)
        elif 'logout' in session:
            info = session['logout']
            session.pop('logout', None)
            return render_template('index.jinja.html', info=info, commit=commit)
        else:
            return render_template('index.jinja.html', stdid=uid, commit=commit)

@app.route('/scoreboard/<int:counter>')
def scoreboard(counter):
    global uid
    if 'user' in session:
        if not commit:
            getLastCommit()
        if (counter <= 0 | counter > 5):
            error_header = u"資料無法處理"
            error_context = u"您所選的資料目前無法處理或是校方系統資料已清空，請稍後再試"
            return render_template('error.jinja.html',
                stdid=uid,
                error_header=error_header,
                error_context=error_context,
                commit=commit), 400
        exam_score_type, exam_score, below_subject = get_term_score()
        if exam_score == False:
            error_header = u"資料無法處理"
            error_context = u"您所選的資料目前無法處理或是校方系統資料已清空，請稍後再試"
            return render_template('error.jinja.html', stdid=uid, commit=commit)
        body = []
        if exam_score_type == 2:
            if counter == 4:
                subject = u'平時成績'
                head = [u'科目', u'成績']
                for i in exam_score:
                    body.append(i[3])
            elif counter == 5:
                subject = u'補考'
                head = [u'科目', u'學期成績', u'最後成績', u'第1次補考成績']
                body = below_subject
            else:
                subject = '第'+str(counter)+'次段考'
                for i in exam_score:
                    body.append(i[counter-1])
                head = [u'科目', u'成績', u'全班平均', u'班級排名', u'班級人數']
            return render_template('scoreboard.jinja.html',
                head=head,
                body=body,
                stdid=uid,
                count=counter,
                commit=commit,
                subject=subject)
        else:
            if counter == 3:
                error_header = u"資料無法處理"
                error_context = u"高三並無第三次段考"
                return render_template('error.jinja.html', error_context=error_context, error_header=error_header, commit=commit)
            else:
                if counter == 4:
                    subject = u'平時成績'
                    head = [u'科目', u'成績']
                    for i in exam_score:
                        body.append(i[2])
                elif counter == 5:
                    subject = u'補考'
                    head = [u'科目', u'學期成績', u'最後成績', u'第1次補考成績']
                    body = below_subject
                else:
                    subject = '第'+str(counter)+'次段考'
                    for i in exam_score:
                        body.append(i[counter-1])
                    head = [u'科目', u'成績', u'全班平均', u'班級排名', u'班級人數']
                return render_template('scoreboard.jinja.html',
                head=head,
                body=body,
                stdid=uid,
                count=counter,
                commit=commit,
                subject=subject)

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

@app.route('/history_pr/')
def history_pr():
    global uid
    if 'user' in session:
        if not commit:
            getLastCommit()
        pr_rew_chart_data, pr_pen_chart_data, pr_chart_total, d_pr_rew_chart_data, d_pr_pen_chart_data= get_history_pr()
        pen_result = [int(i) for i in pr_chart_total[5:-1]]
        sumcheck = 0
        for i in range(len(pen_result)):
            sumcheck += pen_result[::-1][i] * (3**i)
        if sumcheck >= 27:
            pen_check = False
        else:
            pen_check = True
        pr_rew_chart_header=[u'年度', u'學期', u'大功', u'小功', u'嘉獎', u'優點']
        pr_pen_chart_header=[u'年度', u'學期', u'大過', u'小過', u'警告', u'缺點']
        return render_template('history_pr.jinja.html',
            stdid=uid,
            pr_rew_chart_header=pr_rew_chart_header,
            pr_pen_chart_header=pr_pen_chart_header,
            pr_rew_chart_data=pr_rew_chart_data,
            pr_pen_chart_data=pr_pen_chart_data,
            d_pr_rew_chart_header=d_pr_rew_chart_data[0],
            d_pr_rew_chart_data=d_pr_rew_chart_data[1:],
            d_pr_pen_chart_header=d_pr_pen_chart_data[0],
            d_pr_pen_chart_data=d_pr_pen_chart_data[1:],
            pen_check=pen_check,
            t_p=pen_result[0],
            s_p=pen_result[1],
            f_p=pen_result[2],
            commit=commit,
            subject=u'歷年獎懲')
    else:
        session['redirect'] = u'請先登入系統'
        return redirect(url_for('index'))
