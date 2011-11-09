#!/bin/python

"""
Parses code civil TOC to build sections
"""

import urllib
import re
import HTMLParser

date="dateTexte=20100101"
url='http://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006070721'
toremove = re.compile(r"""[\r\n\t]""")
src=re.sub(toremove,'',urllib.urlopen(url+'&'+date).read()) # stripped html

### regexp trials
### pattern1 = re.compile(r"""a href=\"(afficheCode.do[^"]+)\"""")
### pattern1.1 = r"""a
### href=\"affich[^\?]+\?([^"]+)\"?>Articles.([0-9]+)....([0-9]+)"""

#src = open("/home/dummy/articles").read()

pattern2 = re.compile(r"""
a.            # tag
href=         # attr
\"            # quote
affich        #
[^\?]+\?      # url
([^\"]+)      # query!
\"?>Articles. # garbage
([0-9]+)      # begin!
....          # sep
([0-9]+)      # end!
""", re.VERBOSE)

h = HTMLParser.HTMLParser() # to unescape html entities

class Section:
    home = "http://www.legifrance.gouv.fr/affichCode.do"

    def __init__(self,q,b,e):
        self.query = str(h.unescape(q))
        self.begin = str(b)
        self.end   = str(e)
        
    def __repr__(self):
        return "Section@" + self.query + '[' + self.begin + ':' + self.end + ']'

    def __str__(self):
        return self.home + '?' + self.query

# objectify & pretty print
sections = [ str(Section(q,b,e)) for q,b,e in re.findall(pattern2, src) ]
print '\n'.join(sections)

# old shit
# m = re.findall(r"href=\"[^\?]+\?([^\"]+)\" >Articles ([0-9]+) .. ([0-9]+)",src)
# sections = [ Section(q,b,e) for q,b,e in m ]
# print sections
# print len(sections)
