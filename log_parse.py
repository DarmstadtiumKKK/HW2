# -*- encoding: utf-8 -*-
from collections import defaultdict
import re
def otchistkaURL(URL, www):
    find_Yak=URL.find('?')
    find_https=URL.find('https://')
    if find_Yak > 0:
        URL = URL[:find_Yak]
    if URL[len(URL) - 1] == '/':
        excfile = False
    else:
        excfile = True
    if find_https > -1:
        URL=URL[:4]+URL[5:]
    if www:
        find_www=URL.find('://www.')
        if find_www > -1:
            URL='http://'+URL[find_www+7:]
            print(URL)
            return URL, excfile
        else:
            return URL, excfile
    else:
        return URL, excfile


def logcreation(str, www):
    a = str.split(' ')
    data = a[0][: len(a[0])]
    requesttype = a[2][1:]
    url, excistfile = otchistkaURL(a[3], www)
    responsetime = int(a[6][:(len(a[6]) - 1)])
    dict = {
        "data": data,
        "requesttype": requesttype,
        "url": url,
        "excistfile": excistfile,
        "responsetime": responsetime
    }
    return dict


def proverkanalog(str):
    sentencehttp=re.compile('[[]\w{2}[/]\D{3}[/]\w{4}[ ]\w{2}[:]\w{2}[:]\w{2}[]][ ]["]\w*[ ][h][t][t][p][:s][:/][/]')
    result=sentencehttp.match(str)
    if result:
        return True
    return False


def proverka(log, ignfile, reqtype, start, stop):
    if ignfile == True:
        if log['excistfile'] == False:
            provfile = True
        else:
            provfile = False
    else:
        provfile = True
    if reqtype == None:
        provtype = True
    else:
        if reqtype == log['requesttype']:
            provtype = True
        else:
            provtype = False
    if start == None:
        provstart = True
    else:
        if start < log['data']:
            provstart = True
        else:
            provstart = False
    if stop == None:
        provstop = True
    else:
        if stop > log['data']:
            provstop = True
        else:
            provstop = False
    return provfile * provstart * provstop * provtype


def poisk(ignfile, reqtype, start, stop, www):
    f = open('log.log', 'r')
    logs = []
    for line in f:
        if proverkanalog(line):
            log = logcreation(line, www)
            if proverka(log, ignfile, reqtype, start, stop):
                logs.append(log)
    '''for log in logs:
        print(log)'''
    return logs


def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    logs = poisk(ignore_files, request_type, start_at, stop_at, ignore_www)
    MassZnach=defaultdict(int)
    if slow_queries == False:
        for log in logs:
            MassZnach[log['url']]+= 1
        ListZnach = list(MassZnach.values())
        ListZnach.sort()
        ListZnach.reverse()
        return (ListZnach[:5])
    else:
        MassVremenyOj = defaultdict(int)
        for log in logs:
            MassVremenyOj[log['url']] += log['responsetime']
            MassZnach[log['url']] += 1
        ListZnach = list(MassZnach.values())
        ListVremeny = list(MassVremenyOj.values())
        itog = []
        for i in range(0, len(ListZnach), 1):
            itog.append(int(ListVremeny[i] /ListZnach[i]))
        itog.sort()
        itog.reverse()
        return (itog[:5])
