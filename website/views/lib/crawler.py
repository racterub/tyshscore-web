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

#WORST PARSER EVERRRRRRRRRRRRR
#Comment out the unused part of the parser to gain resource resource
def getdata():
    scoredata = {'fncid': '010090', 'std_id': '', 'local_ip': '', 'contant': ''}
    main.get(url + 'f_left.asp')
    res = main.post(url + 'fnc.asp', data=scoredata)
    res.encoding = 'big5'
    if "alert('本學期沒開課或學生身上沒有開課!!');" in res.text:
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
        # info = result[0:5]
        # head = result[5:29]
        # top_row = []
        # head = head[4:]
        # for i in head:
        #     if i == '本次':
        #         head[head.index(i)] = '本次班平均'
        # for i in range(0, len(head), 4):
        #     top_row.append(head[i+1:i+4])


        formatter = []
        tmp = []
        bodycontent = []
        for i in range(29, result.index('總分') - 1, 24):
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
            bodycontent.append(formatter)
            formatter = []


        # footerupper = []
        # for i in range(461, 483, 6):
        #     footerupper.append(result[i:i+6])
        # footerlower = []
        # for i in range(485, 508, 11):
        #     footerlower.append(result[i:i+11])
        #     for i in footerlower:
        #         for k in i:
        #             if '(' in k and '名次' not in k:
        #                 i.remove(k)

        # bottom = []
        # for i in range(518, 524, 2):
        #     bottom.append(result[i:i+2])
        # return info, head, bodycontent, footerupper, footerlower, bottom
        return bodycontent
