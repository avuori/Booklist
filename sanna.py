#!/usr/bin/env python

import time, os
import booklist

data = "/home/avuori/bookdata/sanna.xml"

mtime = os.stat(data).st_mtime

intro = u"<h1>Sannan kirjalista</h1>\
        <p> \
        Listan pito on aloitettu 18.8.2008. \
        </p><p>Muokattu viimeksi %s.</p><hr />" \
		% time.strftime("%d.%m.%Y klo %H:%M", time.localtime(mtime))

t = time.time()
booklist.OutputHandler().run(data,
                             "Sannan kirjalista",
                              intro,
                              "./style.css")
print u"\n<!-- Generation took %d milliseconds. -->" % ((time.time()-t) * 10**3)
