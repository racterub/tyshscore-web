#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-11 23:58:02
# @Author  : Racter (vivi.450@hotmail.com)
# @Link    : https://racterub.me


from lxml import etree
from bs4 import BeautifulSoup as BS
import requests


main = requests.Session()
url = 'http://skyweb.tysh.tyc.edu.tw/skyweb/'

## Module IDs
term_score = "010090"
year_score = "010100"
history_term_score = "010110"
history_year_score = "010120"
term_pr = "010040"
history_pr = "010050"
history_pc = "010060"

def login(stdid, stdpwd):
    '''
    Login to school system
    All process relies on school-end
    This func only passes the input to server. And for now, I'm not implementing some sec-related stuff.
    '''
    loginData = {'txtid': stdid, 'txtpwd': stdpwd, 'check': 'confirm'}
    r = main.get(url+'main.asp', data=loginData)
    r.encoding = 'big5'
    if 'f_left.asp' in str(r.content): #Verify if login works or not
        return True
    else:
        return False

def chunk(l, size):
    '''
    chunk func
    l -> type:list
    size -> the size of each chunks
    '''
    for i in range(0, len(l), size):
        yield l[i:i+size]

def get_term_score():
    '''
    Due to broken html tag from school-end, I'm using html5lib to parse the page.
    Etree will be removed and no longer used in the project.
    def:
        table[2] -> score
        table[3] -> subjects under 60
    '''
    scoredata = {'fncid': term_score, 'std_id': '', 'local_ip': '', 'contant': ''}
    main.get(url + 'f_left.asp')
    res = main.post(url + 'fnc.asp', data=scoredata)
    res.encoding = 'big5'
    if u"alert('本學期沒開課或學生身上沒有開課!!');" in res.text:
        return False
    else:
        '''
        This will be simplfied in the future
        '''
        exam_score = []
        soup = BS(res.text, "html5lib")
        table = soup.find_all('table')
        top =  table[2].find_all('tr')[0].find_all('font')
        check = []
        for i in top:
            check.append(i.string)
        if len(check) == 20:
            '''高三'''
            exam_score_type = 3
            font = table[2].find_all("font")[20:-50]
            text = []
            for i in font:
                tmp = i.string
                if tmp == None or tmp == ' ' or tmp == '\xa0':
                    text.append('')
                else:
                    text.append(tmp)
            chunkd = chunk(text, 20)
            for i in chunkd:
                subject = i[0][2:]
                score = chunk(i[4:] ,4)
                chunkd_score = []
                for j in score:
                    for k in range(2):
                        if j[k]:
                            j[k] = float(j[k])
                    j.insert(0, subject)
                    chunkd_score.append(j)
                del chunkd_score[2][2:]
                exam_score.append(chunkd_score)
        else:
            '''高二'''
            exam_score_type = 2
            font = table[2].find_all('font')[24:-60]
            text = []
            for i in font:
                tmp = i.string
                if tmp == None or tmp == ' ':
                    text.append('')
                else:
                    text.append(tmp)
            chunkd = chunk(text, 24)
            for i in chunkd:
                subject = i[0][2:]
                score = chunk(i[4:], 4)
                chunkd_score = []
                for j in score:
                    for k in range(0,2):
                        if j[k]:
                            j[k] = float(j[k])
                    j.insert(0, subject)
                    chunkd_score.append(j)
                chunkd_score = chunkd_score[:-1]
                chunkd_score[-1] = chunkd_score[-1][:-3]
                exam_score.append(chunkd_score)
        if len(table) != 4:
            below_subject = False
        else:
            font = table[3].find_all('font')[5:]
            text = []
            for i in font:
                tmp = i.string
                if tmp == None or tmp == '':
                    text.append('')
                else:
                    text.append(tmp)
            below_subject = list(chunk(text, 4))
            for i in below_subject:
                for k in range(1, 3):
                    i[k] = float(i[k])
        return exam_score_type, exam_score, below_subject

def get_history_pr():
    '''
    Get rewards and punichments from school system
    def:
        table[2] -> chart
        table[3] -> detail
        table[4] -> special(assume useless)
    '''
    scoredata = {'fncid': history_pr, 'std_id': '', 'local_ip': '', 'contant': ''}
    main.get(url + 'f_left.asp')
    res = main.post(url + 'fnc.asp', data=scoredata)
    res.encoding = 'big5'
    soup = BS(res.text, "html5lib")
    table = soup.find_all('table')
    for i in soup.find_all('br'):
        i.extract()
    text = list(table[2].stripped_strings)
    text_chunkd = list(chunk(text, 10))
    chart_chunkd = text_chunkd[1:-1]
    pr_chart_total = text_chunkd[-1]
    pr_pen_chart = []
    pr_rew_chart = []
    for i in chart_chunkd:
        time = i[0:2]
        data = list(chunk(i[2:], 4))
        for i in range(2):
            data[i] = time + data[i]
        pr_pen_chart.append(data[1])
        pr_rew_chart.append(data[0])
    text = table[3].find_all('font')
    d_chart = []
    for i in text:
        tmp = i.string
        if tmp == '' or tmp == None:
            d_chart.append('')
        else:
            d_chart.append(tmp)
    pin = d_chart[2:].index(u'簽呈日期')
    d_pr_rew_chart = list(chunk(d_chart[1:pin+1], 12))
    d_pr_pen_chart = list(chunk(d_chart[pin+2:], 12))
    return pr_rew_chart, pr_pen_chart,pr_chart_total, d_pr_rew_chart, d_pr_pen_chart