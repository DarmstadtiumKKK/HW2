# -*- encoding: utf-8 -*-
import collections
import re


def otchistka_url(url, www):
    url = re.match(r'\w*://(www\.)?([\w\.]*)(/([\w\.\/-]*)/?)', url).group()
    request = re.match(r'\w*', url).group()
    url = url[len(request) + 3:]
    first_domen = re.match(r'\w*', url).group()
    url = url[len(first_domen) + 1:]
    if url[len(url) - 1] == '/':
        excfile = False
    else:
        excfile = True
    if request == 'https':
        request = 'http'
    shablon = {
        'request': request,
        'slash': '://',
        'domen': first_domen,
        'hvost': url,
        'dot': '.'
    }
    if www is True and first_domen == 'www':
        url = "%(request)s%(slash)s%(hvost)s" % shablon  # request+'://'+url
    else:
        url = "%(request)s%(slash)s%(domen)s%(dot)s%(hvost)s" % shablon  # request+'://'+first_domen+'.'+url
    return url, excfile


def logcreation(stroka, www):
    vhod_data = stroka.split(' ')
    url, excistfile = otchistka_url(vhod_data[3], www)
    log = {
        "data": vhod_data[0][1:],
        "requesttype": vhod_data[2][1:],
        "url": url,
        "excistfile": excistfile,
        "responsetime": int(vhod_data[6][:- 1])
    }
    return log


def proverkanalog(stroka):
    sentencehttp = re.compile(
        '.\w{2}/\D{3}/\w{4} (\w{2}:)*\w{2}] "\w* (([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))? \w*/(\d*.)*\d*" \d* \d*')
    result = sentencehttp.match(stroka)
    if result:
        return True
    return False


def proverka(log, ignfile, reqtype, start, stop, ignorlist):
    for ignorurl in ignorlist:
        if log['url'] == ignorurl:
            return False
    if ignfile is True:
        if log['excistfile'] == True:
            return False
    if reqtype is not None:
        if reqtype != log['requesttype']:
            return False
    if start is not None:
        if start > log['data']:
            return False
    if stop is not None:
        if stop < log['data']:
            return False
    return True


def poisk(ignfile, reqtype, start, stop, www, ignorlist, check):
    f = open('log.log', 'r')
    logs = []
    mas_times = []
    for line in f:
        if proverkanalog(line):
            log = logcreation(line, www)
            if proverka(log, ignfile, reqtype, start, stop, ignorlist):
                if check:
                    logs.append(log)
                else:
                    logs.append(log['url'])
                    mas_times.append(log['responsetime'])
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
    logs = poisk(ignore_files, request_type, start_at, stop_at, ignore_www, ignore_urls,slow_queries)
    if slow_queries is False:
        mass_znach = collections.Counter(logs)
        itog = list(dict(mass_znach.most_common(5)).values())
        itog.sort(reverse=True)
        return itog
    else:
        mass_znach = collections.defaultdict(int)
        mass_vremeny_oj = collections.defaultdict(int)
        for log in logs:
            mass_vremeny_oj[log['url']] += log['responsetime']
            mass_znach[log['url']] += 1
        list_znach = list(mass_znach.values())
        list_vremeny = list(mass_vremeny_oj.values())
        itog = []
        for i in range(0, len(list_znach)):
            itog.append(int(list_vremeny[i] / list_znach[i]))
        itog.sort(reverse=True)
        return (itog[:5])
