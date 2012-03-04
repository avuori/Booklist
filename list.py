#!/usr/bin/env python

import time, os
import booklist

data = "bookdata/books.xml"
mtime = os.stat(data).st_mtime

intro = u"<h1>My books</h1><p> \
    Here I have gathered some of the books I have read \
    during the 21st century. You might catch some \
    literature tips, especially, if you know me \
    and/or share my taste of thought. The topics \
    vary from historical essay to satire to \
    formal philosophical pondering. Most of them \
    are (as of Jun., 2007) actually in Finnish. \
    </p><p> \
    The ratio from one to five expresses my personal \
    feeling about the book. A book rated below three \
    did not satisfy me. A book with ratio of three was a good \
    one and I'd recommend it to others as well. Ratios of \
    four and five map to \"awesome\" and \"all time favourite\", \
    respectively.</p><p> \
    The year associated with the book indicates the year \
    I read it. \
    </p><p>Muokattu viimeksi %s.</p><hr />" \
	% time.strftime("%d.%m.%Y klo %H:%M", time.localtime(mtime))

t = time.time()
booklist.OutputHandler().run(data,
                             "Some of the books I have read during the 21st century",
                             intro,
                             "./books.css")
print u"\n<!-- Generation took %d milliseconds. -->" % ((time.time()-t) * 10**3)
