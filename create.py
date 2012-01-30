#/bin/env python2.7
# -*- coding: utf-8 -*-
# Post script for Web Calendar2 Ver0.22
# author: Michisu, Toshikazu <michisu@marici.co.jp>
import re
import sys
import time
import urllib
import mechanize

common_data = {
    'name': u'',
    'email': u'',
    'passwd': u'',
}
cgi_url_base = ''
tsv_format = ('year', 'month', 'day', 'hour_s', 'min_s', 'hour_e', 'min_e',
        'shubetsu', 'title', 'place', 'content')
types = {
}
form_tag = re.compile('<FORM', re.I)


class Poster(object):

    def __init__(self):
        self.br = mechanize.Browser()

    def post(self, year, month, day, schedule):
        params = {
            'form': 1,
            'year': year,
            'mon': month,
            'day': day,
        }
        print '%s/%s/%s' % (year, month, day)

        url = cgi_url_base + '?' + urllib.urlencode(params)
        response = self.br.open(url)
        html = response.read()
        nr = len(form_tag.findall(html)) - 1
        self.br.select_form(nr=nr)

        schedule.update(common_data)
        for name, value in schedule.iteritems():
            print '%s: %s' % (name, value)
            if name == 'shubetsu':
                value = types.get(value, value)
            value = value.encode('sjis')
            try:
                self.br[name] = value
            except TypeError, e:
                if str(e) == 'ListControl, must set a sequence':
                    self.br[name] = [value]
                else:
                    raise

        print 'delfile', self.br['delfile']
        self.br.submit()
        print 'submit OK'


def main():
    poster = Poster()
    for line in sys.stdin:
        line = line.strip('\n')
        if not line: continue
        data = [d.decode('utf-8') for d in line.split('\t')]
        if len(data) != len(tsv_format): continue
        if data[0] == 'year': continue
        schedule = {}
        for i in xrange(len(data)):
            schedule[tsv_format[i]] = data[i]
        poster.post(schedule.pop('year'), schedule.pop('month'),
                schedule.pop('day'), schedule)
        time.sleep(1)

if __name__ == '__main__':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()
