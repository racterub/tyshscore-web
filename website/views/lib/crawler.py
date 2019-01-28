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

def get_score():
    scoredata = {'fncid': '010090', 'std_id': '', 'local_ip': '', 'contant': ''}
    main.get(url + 'f_left.asp')
    res = main.post(url + 'fnc.asp', data=scoredata)
    res.encoding = 'big5'
    if u"alert('本學期沒開課或學生身上沒有開課!!');" in res.text:
        return False
    else:
        result = []
        root = etree.HTML(res.text)
        table = root.xpath('//table')
        for i in table:
            tr = i.xpath('.//tr')
            for j in tr:
                td = j.xpath('.//td')
                for k in td:
                    font = k.xpath('.//font')
                    for d in font:
                        text = d.xpath('./text()')
                        if len(text) == 0:
                            result.append('')
                        else:
                            result.append(text[0].strip())
        formatter = []
        tmp = []
        score_table = []
        for i in range(29, result.index(u'總分') - 1, 24):
            recv = result[i:i+24]
            subject = recv[0][2:].strip()
            score = recv[4:]
            for k in range(0, 20, 4):
                tmp.append(subject)
                for j in score[k:k+4]:
                    tmp.append(j)
                for p in tmp[1:3]:
                    if p != '':
                        tmp[tmp.index(p)] = float(p)
                formatter.append(tmp)
                tmp = []
            score_table.append(formatter)
            formatter = []
        return score_table


def chunk(l, size):
    for i in range(0, len(l), size):
        yield l[i:i+size]
def beta_bs4_score():
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
        result = []
        # soup = BS(res.text, "lxml") #Not working
        soup = BS(res.text, "html5lib")
        font = soup.find_all('table')[2].find_all('font')[24:-60]
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
                    if j[k] != '':
                        j[k] = float(j[k])
                j.insert(0, subject)
                chunkd_score.append(j)
            chunkd_score = chunkd_score[:-1]
            result.append(chunkd_score)
        return result


def beta_get_score():
    '''
    THIS BETA CONTAINS A CRITICAL BUG WHICH WAS WAUSED BY SCHOOL-END

    source contains four tables
    table[3] is coded with broken html lang (starting `tr` element inside table is missing)
    , which cause lxml can't parse the source code properly :/
    '''
    scoredata = {'fncid': '010090', 'std_id': '', 'local_ip': '', 'contant': ''}
    main.get(url + 'f_left.asp')
    res = main.post(url + 'fnc.asp', data=scoredata)
    res.encoding = 'big5'
    if u"alert('本學期沒開課或學生身上沒有開課!!');" in res.text:
        return False
    else:
        result = []
        print(res.text)
        print('===')
        root = etree.HTML(res.text)
        table = root.xpath('//table')
        print(table[3].iterchildren())
        #Get subjects that needs to be re-exammed
        tr = table[3].xpath('.//tr')
        for i in tr:
            td = i.xpath('.//td')
            for j in td:
                font = j.xpath('.//font')
                for k in font:
                    text = k.xpath('./text()')
                    if len(text) == 0:
                        result.append('')
                    else:
                        result.append(text[0].strip())

        return result