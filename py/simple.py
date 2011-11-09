#!/bin/python

"""
Parses code civil TOC to build sections
"""

import urllib
import re
import HTMLParser

codes = { "civil" : "LEGITEXT000006070721" }

class Code:
    cache = ""

    def __init__(self,id,date):
        self.id   = id
        self.date = date
        self.url  = 'http://www.legifrance.gouv.fr/affichCode.do'
    
    def __src__(self):
        toremove = re.compile(r"""[\r\n\t]""")
        if self.cache == "":
            self.cache = re.sub(toremove,'', urllib.urlopen(self.url+'?'
                                                            + "cidTexte="  + self.id + '&'
                                                            + "dateTexte=" + self.date
                                                            ).read())
        return self.cache
    
    def sections(self):
        section = re.compile(r"""
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
        return [ str(Section(q,b,e)) for q,b,e in re.findall(section, self.__src__()) ]

    def __repr__(self):
        return "Code " + self.id + '@' + self.date

    def __str__(self):
        return self.__repr__()

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
#sections = [ str(Section(q,b,e)) for q,b,e in re.findall(sections, src) ]
#print '\n'.join(sections)

class Article:
    def __init__(self, num, titre, texte):
        self.num   = num
        self.titre = titre
        self.texte = texte

    def __repr__(self):
        return "Article #" + self.num + " : " + self.titre
    
    def __str__(self):
        return __repr__(self)

cc = Code(codes["civil"],"20100101")
print cc.sections()
print len(cc.sections())
print len(cc.sections())
print len(cc.sections())
