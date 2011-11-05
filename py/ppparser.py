from HTMLParser import HTMLParser
import re

class pp(HTMLParser):
      actags = set([ "area","base","basefont","br","hr","input","img"]) #,"link","meta" ])
      igtags = set([ "br" ])
      depth=0
      indent=" | "

      # def open(s):
      #       return self.wrap(s,'<','>')

      # def close(s):
      #       return self.open('/'+s)

      # def wrap(s,pre,post):
      #       return pre + s + post

      def pp_attrs(self, list):
            return ' '.join([a+"=\""+b+'"' for (a,b) in list])
      
      def handle_starttag(self, tag, attrs):
            if tag in self.igtags:
                  return

            print self.depth*self.indent + '<' + tag + (' ' + self.pp_attrs(attrs) if not attrs == [] else '' ) + '>'
            if tag not in self.actags:
                  self.depth += 1
            
      def handle_endtag(self,tag):
            if tag in self.igtags:
                  return

            self.depth -= 1
            print self.depth*self.indent + "</" + tag + '>'

      def handle_data(self,data):
            matches = re.match("(?u)[\s^\w]+", unicode(data)).groups()
            empty = matches == ()
            if not empty:
                  chars = str([unicode(c) for c in data])
                  print self.depth*self.indent + '[' + data + "]::(" + str(len(data)) + ")" + "{" + str(matches) + "}" + str(matches == ())

import urllib

url = 'http://fasteez.free.fr/'
html = urllib.urlopen(url).read().replace("<br>","<br/>")
parser = pp()
parser.feed(html)
print str(len(html)) + " bytes"
