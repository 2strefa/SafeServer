#-*- encoding: utf-8 -*-

def parser_1(x):
    a = dict({
        '1': u' jeden',
        '2': u' dwa',
        '3': u' trzy',
        '4': u' cztery',
        '5': u' pięć',
        '6': u' sześć',
        '7': u' siedem',
        '8': u' osiem',
        '9': u' dziewięć'
    })
    try:
        return '%s' % a[x]
    except:
        return ''


def parser_11_19(x):
    a = dict({
        '1': u' jedenaście',
        '2': u' dwanaście',
        '3': u' trzynaście',
        '4': u' czternaście',
        '5': u' piętnaście',
        '6': u' szesnaście',
        '7': u' siedemnaście',
        '8': u' osiemnaście',
        '9': u' dziewiętnaście'
    })
    try:
        return a[x]
    except:
        return ''


def parser_10(x):
    a = dict({
        '1': u' dziesięć',
        '2': u' dwadzieścia',
        '3': u' trzydzieści',
        '4': u' czterdzieści',
        '5': u' pięćdziesiąt',
        '6': u' sześćdziesiąt',
        '7': u' siedemdziesiąt',
        '8': u' osiemdziesiąt',
        '9': u' dziewięćdziesiąt'
    })
    try:
        return a[x]
    except:
        return ''


def parser_100(x):
    a = dict({
        '1': u' sto',
        '2': u' dwieście',
        '3': u' trzysta',
        '4': u' czterysta',
        '5': u' pięćset',
        '6': u' sześćset',
        '7': u' siedemset',
        '8': u' osiemset',
        '9': u' dziewięćset'
    })
    try:
        return a[x]
    except:
        return ''


def parser_1000(x):
    a = dict({
        '1': u' tysiąc',
        '2': u' dwa tysiące',
        # '3': u' trzy tysiące',
        # '4': u' cztery tysiące',
        # '5': u' pięć tysięcy',
        # '6': u' sześć tysięcy',
        # '7': u' siedem tysięcy',
        # '8': u' osiem tysięcy',
        # '9': u' dziewięć tysięcy'
    })
    try:
        return a[x]
    except:
        return ''


def liczba(a):
    # rozdzielam wzgledem przecinka
    x = str(a).split('.')
    # czesc całkowita i ułamek
    z = x[0]
    s = x[1]
    if len(s) == 1:
        s += '0'
    # dwie ostatnie liczby, do sprawdzania przedziału 11-19
    k = int(z[-2:])

    if len(z) == 1:
        a1 = parser_1(z[0])
        return u'%s złotych %s/100' % (a1, s)

    if len(z) == 2:
        if k > 10 and k < 20:
            return u'%s złotych %s/100' % (parser_11_19(z[-1]), s)
        else:
            a10 = parser_10(z[0])
            a1 = parser_1(z[1])
            return u'%s%s złotych %s/100' % (a10, a1, s)

    if len(z) == 3:
        if k > 10 and k < 20:
            a100 = parser_100(z[0])
            a10 = parser_11_19(z[-1])
            return u'%s%s złotych %s/100' % (a100, a10, s)
        else:
            a100 = parser_100(z[0])
            a10 = parser_10(z[1])
            a1 = parser_1(z[2])
        return u'%s%s%s złotych %s/100' % (a100, a10, a1, s)

    elif len(z) == 4:
        if k > 10 and k < 20:
            a1000 = parser_1000(z[0])
            a100 = parser_100(z[1])
            a10 = parser_11_19(z[-1])
            return u'%s%s%s złotych %s/100' % (a1000, a100, a10, s)
        else:
            a1000 = parser_1000(z[0])
            a100 = parser_100(z[1])
            a10 = parser_10(z[2])
            a1 = parser_1(z[3])
            return u'%s%s%s%s złotych %s/100' % (a1000, a100, a10, a1, s)
