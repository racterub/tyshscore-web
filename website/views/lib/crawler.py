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

#score defs
total_col = 16
per_col = 4

def login(stdid, stdpwd):
    loginData = {'txtid': stdid, 'txtpwd': stdpwd, 'check': 'confirm'}
    r = main.get(url+'main.asp', data=loginData)
    r.encoding = 'big5'
    if 'f_left.asp' in str(r.content):
        return True
    else:
        return False


def chunk(l, size):
    for i in range(0, len(l), size):
        yield l[i:i+size]
def get_score():
    '''
    THIS BETA IS A 2.x VERSION OF TYSHSCORE.

    I'm trying to replace lxml with bs4
    Reason is mentioned inside beta_get_score function

    THIS IS WORKING!!!!!!!!!!!!!
    '''
    scoredata = {'fncid': '010090', 'std_id': '', 'local_ip': '', 'contant': ''}
    main.get(url + 'f_left.asp')
    res = main.post(url + 'fnc.asp', data=scoredata)
    res.encoding = 'big5'
    if u"alert('本學期沒開課或學生身上沒有開課!!');" in res.text:
        return False
    else:
        exam_score = []
        # soup = BS(res.text, "lxml") #Not working
        soup = BS(res.text, "html5lib")
        table = soup.find_all('table')
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
            for l in font:
                tmp = l.string
                if tmp == None or tmp == '':
                    text.append('')
                else:
                    text.append(tmp)
            below_subject = list(chunk(text, 4))
            for i in below_subject:
                for k in range(1, 3):
                    i[k] = float(i[k])
        return exam_score, below_subject