#!/usr/bin/env python

import time
import booklist

intro = u"<h1>Sannan kirjalista</h1>\
        <p> \
        Listan pito on aloitettu 18.8.2008. \
        </p><hr />"

t = time.time()
booklist.OutputHandler().run("/home/avuori/bookdata/sanna.xml",
                             "Sannan kirjalista",
                              intro,
                              "./style.css")
print u"\n<!-- Generation took %d milliseconds. -->" % ((time.time()-t) * 10**3)
