#!/usr/bin/python


# BEGIN XML
from xml.dom import minidom
import urllib

def load(rssURL):
    return minidom.parse(urllib.urlopen(rssURL))

DEFAULT_NAMESPACES = \
    (None,
     'http://purl.org/rss/1.0',
     'http://my.netscape.com/rdf/simple/0.9'
     )

def getElementsByTagName(node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
    for namespace in possibleNamespaces:
        children = node.getElementsByTagNameNS(namespace, tagName)
        if len(children): return children
    return []

def first(node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
    children = getElementsByTagName(node, tagName, possibleNamespaces)
    return len(children) and children[0] or None

def textOf(node):
    return node and "".join([child.data for child in node.childNodes]) or ""

def getContents(node, category):
    return textOf(first(node, category)).encode("utf8")


from threading import Timer

def setInterval(fn, ms):
    def fnwrapper():
        fn()
        setInterval(fn, ms)
    t = Timer(ms / 1000, fnwrapper)
    t.start()
    return t

def setTimeout(fn, ms):
    t = Timer(ms / 1000, fn)
    t.start()
    return t


def printrss(item):
    print " -- article --"
    print "title: {0}".format(getContents(item, 'title'))
    print "link: {0}".format(getContents(item, 'link'))
    print "description: {0}".format(getContents(item, 'description'))
    print "\n"

def runrss(rssDocument):
    for item in getElementsByTagName(rssDocument, 'item'):
        printrss(item)


if __name__ == '__main__':
    import sys
    rssDocument = load(sys.argv[1])

    def wrapped():
        runrss(rssDocument)

    timerRef = setInterval(wrapped, 1000)

    def cancel():
        timerRef.cancel()

    setTimeout(cancel, 10000)
