# -*- encoding: utf-8 -*-
def otchistkaURL(str, www):
    if str.find('?') > 0:
        s = str[:str.find('?')]
    else:
        s = str
    if s[len(s) - 1] == '/':
        excfile = 0
    else:
        excfile = 1
    s1 = s[:4]
    if s.find('https') > -1:
        s2 = s[5:]
    else:
        s2 = s[4:]
    if www:
        if s2.find('www') > 0:
            s3 = s2[:s2.find('www')]
            s4 = s2[(s2.find('www') + 4):]
            return s1 + s3 + s4, excfile
        else:
            return s1 + s2, excfile
    else:
        return s1 + s2, excfile


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
    if str[0] == '[' and str[21] == ']':
        return 1
    return 0


def proverka(log, ignfile, reqtype, start, stop):
    if ignfile > 0:
        if log['excistfile'] == 0:
            provfile = 1
        else:
            provfile = 0
    else:
        provfile = 1
    if reqtype == None:
        provtype = 1
    else:
        if reqtype == log['requesttype']:
            provtype = 1
        else:
            provtype = 0
    if start == None:
        provstart = 1
    else:
        if start < log['data']:
            provstart = 1
        else:
            provstart = 0
    if stop == None:
        provstop = 1
    else:
        if stop > log['data']:
            provstop = 1
        else:
            provstop = 0
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
    dict = {}
    if slow_queries == 0:
        for log in logs:
            if dict.get(log['url']) == None:
                dict[log['url']] = 1
            else:
                dict[log['url']] += 1
        l = dict.values()
        o = list(l)
        o.sort()
        o.reverse()
        return (o[:5])
    else:
        dict1 = {}
        for log in logs:
            if dict.get(log['url']) == None:
                dict[log['url']] = log['responsetime']
                dict1[log['url']] = 1
            else:
                dict[log['url']] += log['responsetime']
                dict1[log['url']] += 1
        l = dict.values()
        l1 = dict1.values()
        o = list(l)
        o1 = list(l1)
        itog = []
        for i in range(0, len(o), 1):
            itog.append(int(o[i] / o1[i]))
        itog.sort()
        itog.reverse()
        return (itog[:5])
