#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-11 23:58:02
# @Author  : Racter (vivi.450@hotmail.com)
# @Link    : https://racterub.me


from lxml import etree
import requests

main = requests.Session()
url = 'http://skyweb.tysh.tyc.edu.tw/skyweb/'

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
