#!/usr/bin/env python
#
# A book list generator.
# Eats XML data and outputs XHTML + javascript.
# Input XML DTD: http://cs.helsinki.fi/u/avuori/books/books.dtd
#
# 6.10.2008
# Arto Vuori
#
# TODO: - sorting: author(DONE), rate, year
#
import cgi
import time
import xml.dom.minidom

class Book:
    def __init__(self, authors, title, year, rate, comment):
        self.author = authors
        self.title = title
        self.year = year
        self.rate = rate
        self.comment = comment

    def getAuthors(self):
        return self.authors

    def getTitle(self):
        return self.title

    def getYear(self):
        return int(self.year)

    def getRate(self):
        try:
            return float(self.rate)
        except:
            return 0

    def getComment(self):
        return self.comment

    def __cmp__(self, other):
        return cmp(self.getTitle().lower(), other.getTitle().lower())

class Authors:
    def __init__(self):
        self.names = []
        self.books = []

    def addName(self, name):
        self.names.append(name)

    def addBook(self, book):
        self.books.append(book)

    def getNames(self):
        return reduce(lambda x,y: x + " and " + y, self.names).encode("utf-8")

    def getBooks(self):
        return self.books
    
    def __cmp__(self, other):
        return cmp(self.getNames().lower(), other.getNames().lower())

class Parser:
    def __init__(self, path):
        self.path = path

    # Returns a list of Authors objects
    def parse(self):
        dom = xml.dom.minidom.parse(self.path)
        return self.collect(dom)

    def collect(self, node):
        literature = node.firstChild.nextSibling.nextSibling
        authors = []
        for author in literature.childNodes:
            if author.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                continue
            newAuthors = Authors()
            names = author.getElementsByTagName("names").item(0)
            for name in names.childNodes:
                if name.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                    continue
                newAuthors.addName(name.childNodes.item(0).nodeValue)
            booksEl = author.getElementsByTagName("books")
            if (len(booksEl) == 0):
                continue
            for book in booksEl.item(0).childNodes:
                if book.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                    continue
                metaData = {}
                metaEls = {"title": book.getElementsByTagName("title"),
                           "year": book.getElementsByTagName("readyear"),
                           "rate": book.getElementsByTagName("mystars"),
                           "comment": book.getElementsByTagName("comment")}
                for key in metaEls:
                    metaData[key] = (len(metaEls[key]) == 1) \
                            and metaEls[key].item(0).hasChildNodes()  \
                            and metaEls[key].item(0).firstChild.nodeValue.encode("utf-8") \
                            or ""
                newAuthors.addBook(Book(newAuthors, 
                                   metaData["title"], 
                                   metaData["year"], 
                                   metaData["rate"],
                                   metaData["comment"]))
            authors.append(newAuthors)
        return authors

class UI:
    __id = 0
    # It's a PNG :-) (the star symbol)
    STAR_DATA = "iVBORw0KGgoAAAANSUhEUgAAABkAAAAUCAIAAAD3FQHqAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAL" \
                "EwAACxMBAJqcGAAAAoZJREFUOMullFFIU2EUx//f7mxeackaeTcykbS6xB5cREFhrSjWMEyGN6KH" \
                "ngymwYZkBEKRUIGLuqmLqKd6KL1qa2+X0S4zCCZMGQkpY4TCxpAi4t4EmbbdHhyhbW5lf87D953z" \
                "8TvfOd/hg1pOXV1dJpNpaWmp7EmUDs/NzVEUpaXg9Xr/i5XL5RwOR1Mj7nWApumFhYWts0RR1Ggw" \
                "+RQ/JeyvRWdn5xZZy8vLVqvVeQLqBNQJDN8GISQSiWyF5fP5ttP49DLPyoVx9jDsdvs/sBYXF8fH" \
                "x10uF8MwNy7lQWv2wQdKg9HR0c1YZK2cqampYDAoSVI0Gq2gsgY96k14exeMAevV8QDBj7U2mw0F" \
                "ommaOJ3OUCikKMqBPTh/DLYmnD6EKh2KKvUV3uENnu8/MCwhm0Nzc7M2k8koinLuCJ50Y68ZpVW7" \
                "C4Pu/FpVMfgGd16ghjEPDAxwHEfF43GLxeIXZx6//kZRaNqHCi3KSpqG8xaE95We7puCIFit1jW8" \
                "qqqqLMu9vb16vZ6tQ+jRhpb/YfMjuGIHIaS1tXV2dnbTd0yn0y0tLYSQC8exKhUBTT9HlQ4sy/r9" \
                "/r+aL0EQAMyPFGElXqFyG4aGhorOhKawF4qiMAbU1eS3mVWMTWDmMwA07oanHf39/bIsF+liIZ7j" \
                "uPaT+Yu8e4h6E7RarUaDi6eQGsOXAJid6OnpKV9jNps1m83PrmN+BI6jIAQcxyWTyUAgwLKscQfu" \
                "XwV/DTRNJ5PJMqxYLAbg8hnQOlgsFkmSfodkWe7r66uurj5Yn89RhsXzPACj0cjz/MrKSmEhiUSi" \
                "ra2NEEIIiUajpViiKLrd7lQqVfqrCofDDQ0NHo9nvfMX1XK0JgZWs+cAAAAASUVORK5CYII="

    HALFSTAR_DATA \
              = "R0lGODlhGQAUAMZ2AAAAAAEBAAEBAQICAAMCAAQDAAMDAwQEBAgGAAkHAAoHAAgICAwJAAkJCRAM" \
                "AA0NDRINAA4ODhMOAA8PDxcRABcSABkTABMTExcXFyAYABgYGBkZGRwcHCcdACgeACogACMjIy8j" \
                "ADAkACcnJygoKDkrACwsLDExMUg2AEk3ADg4OE87AD09PVI+AFQ/AFpEAEdHR0lJSUtLS05OTlBQ" \
                "UFJSUlVVVXNXAHVYAFxcXGVlZWhoaItpAGlpaWpqam5ubm9vb5lzAHR0dHp6ent7e4GBgbOHAIqK" \
                "iruNALyOAI+Pj5OTk5SUlMiXAJubm9WhAN2nAN+oAKmpqaqqqqurq6ysrK6uruivALCwsLe3t/W5" \
                "APi7APu9AL29vf2+AL+/v//AAMLCwsfHx8vLy8/Pz9bW1tfX19vb2+Dg4OPj4+Tk5Obm5ujo6PDw" \
                "8PHx8fPz8/T09Pb29vf39/r6+v39/f7+/v///////////////////////////////////////yH5" \
                "BAEKAH8ALAAAAAAZABQAAAepgHaCg4R2Pn+IiYqJhYVmBouRiI2DdTEikpGUglkDTZmLm3InLWCg" \
                "iptMDE+mp5OEbFU7GDhgra52cWFEKgYIFiVXtq6INREAHTdGWrbNxH8yAChQzdW3p3VUIxA8zNbP" \
                "gm5DDx5J38SEazICK1zO6IVSAFHvuIVOFF62W+CFNi62kGToN4jOhiBRUgSwQVAQGQAvEpjoYqeh" \
                "HSUALiiZI8hilh9qCD0LBAA7"

    def getStars(self, rate, id):
        try:
            return "<script type='text/javascript'>\n" \
                   "//<![CDATA[\nprintStars('%s', %.1f);\n//]]></script>" % (id, rate)
        except:
            return ""

    def get(self, authors, pageTitle, introText, cssPath):
        self.printHtmlHeader(pageTitle, cssPath)

        print introText
 
        print u"<table>"
        print u"<tr><th>Author(s)</th><th>Title</th><th>Year</th>" \
                "<th style='width:75px'>Rate (1-5)</th><th>Comment</th></tr>"

        authors.sort()

        for a in authors:
            self.printAuthor(a)
        print u"</table><hr />"

        self.printStats(authors)

        self.printHtmlFooter()

    def printStats(self, authors):
        print "<h2>Reading statistics</h2>"
        yearMap = {}
        yearRateMap = {}
        authorMap = {}

        for a in authors:
            if a.getNames() not in authorMap:
                authorMap[a.getNames()] = True
            for b in a.getBooks():
                if b.getYear() not in yearMap:
                    yearMap[b.getYear()] = 1
                    yearRateMap[b.getYear()] = b.getRate()
                else:
                    yearMap[b.getYear()] += 1
                    yearRateMap[b.getYear()] += b.getRate()

        years = yearMap.keys()
        years.sort()
        print "<table>"
        print "<tr><th style='padding-right: 1em;'>Year</th>\
                <th style='text-align:right'>Number of books</th>\
                <th style='text-align:right'>Avg. rate</th></tr>"
        for y in years:
            print "<tr><td>%d</td>\
                       <td style='text-align:right'>%d</td>\
                       <td style='text-align:right'>%.3f /5</td>\
                       </tr>" % (y, yearMap[y], float(yearRateMap[y])/yearMap[y])
        print "<tr><td colspan='3'>%s</td></tr>" % ("_"*45)
        print "<tr><td>In ~%d years</td>\
                   <td style='text-align:right'>%d</td>\
                   <td style='text-align:right'>%.3f /5</td>\
                   </tr>" \
                % (len(years), 
                   reduce(lambda x,y:x+y, yearMap.values()),
                   float(reduce(lambda x,y:x+y, yearRateMap.values())) \
                           / reduce(lambda x,y:x+y, yearMap.values()))
        print "<tr><td colspan='3'>from %d authors</td></tr>" % len(authorMap)
        print "</table>"

    def generateId(self):
        n = self.__id
        self.__id += 1
        return n

    def printAuthor(self, author):
        books = author.getBooks()
        books.sort()
        count = 0
        for book in author.getBooks():
            id = self.generateId()
            # The getNames() is already utf-8 encoded, 
            # that's why the literal is not re-encoded.
            print "<tr><td>%s</td><td><a type='amzn' category='books'>%s</a></td><td>%s</td><td id='stars_%d'>%s</td><td>%s</td></tr>" \
                % (cgi.escape(author.getNames()), 
                   cgi.escape(book.getTitle()), 
                   book.getYear(), 
                   id,
                   self.getStars(book.getRate(), "stars_%d" % id), 
                   cgi.escape(book.getComment()))
            count += 1
            if (len(author.getBooks()) == count):
                print "<tr><td colspan='5'>&nbsp;</td></tr>"

    def printHtmlHeader(self, pageTitle, cssPath):
        print u"<?xml version='1.0'?>\n" \
               "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' " \
               "'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>\n" \
               "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>" \
               "<head>" \
               "<meta http-equiv='Content-Type' content='application/xhtml+xml; " \
                    "charset=UTF-8' />" \
               "<title>%s</title>\n" \
               "<script type='text/javascript'>" \
                   "//<![CDATA[\n" \
                   "star_data = \"%s\";\n" \
                   "halfstar_data = \"%s\";\n" \
                   "stars = function(n) {\n" \
                     "if (n == 0) return '';\n" \
                     "if (n < 1) { " \
                        "return \"<img width='15' alt='' " \
                            "src='data:image/gif;base64,\"+halfstar_data+\"' />\"; }\n" \
                     "var tag = \"<img width='15' alt='' " \
                                      "src='data:image/png;base64,\"+star_data+\"' />\";\n" \
                     "return tag + stars(n-1);" \
                   "}\n" \
                   "printStars = function(id, n) {\n" \
                     "document.getElementById(id).innerHTML = stars(n);" \
                   "}\n" \
                   "//]]>\n" \
               "</script>" \
               "<link href='%s' rel='stylesheet' type='text/css' />" \
               "</head><body>" % (pageTitle, UI.STAR_DATA, UI.HALFSTAR_DATA, cssPath)

    def printHtmlFooter(self):
        print u"<SCRIPT charset=\"utf-8\" type=\"text/javascript\" " \
                "src=\"http://ws.amazon.com/widgets/q?ServiceVersion=20070822" \
                "&MarketPlace=US&ID=V20070822/US/kirjalista-20/8005/0dff475d-c893-4300-886e-f97bc59cac1b\"> "\
                "</SCRIPT> <NOSCRIPT><A HREF=\"http://ws.amazon.com/widgets/q?ServiceVersion=20070822&MarketPlace=US" \
                "&ID=V20070822%2FUS%2Fkirjalista-20%2F8005%2F0dff475d-c893-4300-886e-f97bc59cac1b&Operation=NoScript\">" \
                "Amazon.com Widgets</A></NOSCRIPT>" \
                "</body></html>"

class OutputHandler:
    def printHttpHeaders(self):
        print u"Content-type: text/html; charset=UTF-8"
        print ""
    
    def run(self, path, pageTitle, introText, cssPath):
        self.printHttpHeaders()
        UI().get(Parser(path).parse(), pageTitle, introText, cssPath)
