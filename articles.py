from HTMLParser import HTMLParser

class Typee():
    def eat(self,thing):
        print thing

    def __str__(self):
        return 'Typee()'

    def __repr__(self):
        return self.__str__()

class Titre(Typee):
    titre = None
    def eat(self,thing):
        self.titre = thing

    def __str__(self):
        return "T(%s)" % str(self.titre)

class Intervalle(Typee):
    inter = None

    def __init__(self, url):
        self.url = url

    def eat(self,thing):
        self.inter = thing

    def __str__(self):
        return "[%s]" % str(self.inter)

class Code(Typee):
    code = None

    def eat(self,thing):
        self.code = thing

    def __str__(self):
        return "C[%s]" % str(self.code)

class Articles(HTMLParser):
    flag = False
    res = []
    typee = None
    def candidate(self, tag, attrs):
        if ( (tag == 'span') & ( ('class','TM1Code') in attrs ) ):
            self.typee = Titre()
#        elif ( (tag == 'span') & ( ('class', 'codeLienArt') in attrs) ):
#            print attrs
#            self.typee = Intervalle('http://')
        elif ( (tag == 'a')
        elif ( (tag == 'div') & ( ('id','titreTexte') in attrs ) ):
            self.typee = Code()

    def handle_starttag(self, tag, attrs):
        self.candidate(tag, attrs)

    def handle_endtag(self, tag):
        if not self.typee == None:
            self.res.append(self.typee)
        self.typee=None
        
    def handle_data(self, data):
        if not self.typee == None:
            self.typee.eat(data)

    def results():
        return self.res

print 'work.'

url = 'http://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006070721&dateTexte=20111102'
import urllib

html = urllib.urlopen(url).read()
print len(html)

parser = Articles()
parser.feed(html)
print len(parser.res), 'infos trouvee(s).'
print parser.res
