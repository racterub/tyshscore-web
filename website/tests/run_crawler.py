#!/usr/bin/env python3

from ..views.lib.crawler import login, get_history_pr, get_term_score

username = ''
password = ''

login(username, password)

#print(beta_get_score()) #Issue mentioned in crawler module
# print(beta_bs4_score())
# print(get_score())

print(get_history_pr())
# print(get_term_score())