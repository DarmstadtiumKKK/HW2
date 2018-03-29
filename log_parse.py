# -*- encoding: utf-8 -*-
from collections import defaultdict
import re
def otchistkaURL(URL, www):
    URL=re.match(r'\w*://(www\.)?([\w\.]*)(/([\w\.\/-]*)/?)',URL).group()
    request=re.match(r'\w*',URL).group()
    URL=URL[len(request)+3:]
    first_domen=re.match(r'\w*',URL).group()
    URL=URL[len(first_domen)+1:]
    if URL[len(URL) - 1] == '/':
        excfile = False
    else:
        excfile = True
    if request=='https':
        request='http'
    if www==True and first_domen=='www':
        URL=request+'://'+URL
    else:
        URL=request+'://'+first_domen+'.'+URL
    return URL,excfile



def logcreation(stroka, www):
    vhod_data = stroka.split(' ')
    data = vhod_data[0][: len(vhod_data[0])]
    requesttype = vhod_data[2][1:]
    url, excistfile = otchistkaURL(vhod_data[3], www)
    responsetime = int(vhod_data[6][:(len(vhod_data[6]) - 1)])
    log = {
        "data": data,
        "requesttype": requesttype,
        "url": url,
        "excistfile": excistfile,
        "responsetime": responsetime
    }
    return log


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
    return provfile and provstart and provstop and provtype


def poisk(ignfile, reqtype, start, stop, www):
    f = open('log.log', 'r')
    logs = []
    for line in f:
        if proverkanalog(line):
            log = logcreation(line, www)
            if proverka(log, ignfile, reqtype, start, stop):
                logs.append(log)
                print(log)
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
        print(MassZnach)
        ListZnach.sort(reverse=True)
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
        itog.sort(reverse=True)
        return (itog[:5])
