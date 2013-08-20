# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 21:16:19 2013

@author: Jonathan
"""

import urllib2
import webbrowser
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

def testXKCD():
    test = int(siteDict[r"http://xkcd.com/"]) + 1
    try:
        f = urllib2.urlopen(r"http://xkcd.com/{0}/".format(test))
        webbrowser.open(f.geturl())
        print "New XKCD"
        print ""
        incDict[r"http://xkcd.com/"] = 1
    except urllib2.HTTPError:
        pass


def testJL8():
    test = int(siteDict[r"http://limbero.org/jl8/"]) + 1
    f = urllib2.urlopen(r"http://limbero.org/jl8/{0}".format(test))
    g = urllib2.urlopen(r"http://limbero.org/jl8/{0}".format(test - 1))
    if f.geturl() != g.geturl():
        webbrowser.open(f.geturl())
        print "New JL8"
        print ""
        incDict[r"http://limbero.org/jl8/"] = 1


def testHxH():
    test = int(siteDict[(r"http://www.animefreak.tv/watch/"
                         "hunter-x-hunter-2011")]) + 1
    try:
        f = urllib2.urlopen((r"http://www.animefreak.tv/watch/"
                             "hunter-x-hunter-2011-episode-{0}-online")
                            .format(test))
        webbrowser.open(f.geturl())
        print "New Hunter x Hunter"
        print ""
        incDict[r"http://www.animefreak.tv/watch/hunter-x-hunter-2011"] = 1
    except urllib2.HTTPError:
        pass


def testWebDip():
    br = Browser()
    br.open("http://webdiplomacy.net/logon.php")
    br.select_form(nr=0)
    br['loginuser'] = "USERNAME HERE"
    br['loginpass'] = "PASSWORD HERE"
    br.submit()
    br.open("http://webdiplomacy.net/index.php")
    resp = br.reload()
    html = resp.read()
    soup = BeautifulSoup("".join(html))
    notices = soup.find("div", {"class": "gamelistings-tabs"})
    if notices is None:
        return
    if notices.find("img", {"src": "images/icons/mail.png"}):
        webbrowser.open(br.geturl())
        print "Your move in WebDiplomacy"
        print ""

if __name__ == "__main__":
    #Creates the necessary dictionaries
    with open("C:\Users\Jonathan\Documents\RSSsites.txt") as f:
        siteDict = {}
        for i, line in enumerate(f.readlines()):
            if i % 2 == 0:
                temp = line[:-1]
            else:
                siteDict[temp] = line[:-1]
        del i, line, temp
    incDict = {k: 0 for k in siteDict.keys()}

    #Tests the different websites
    print ""
    testXKCD()
    testJL8()
    testHxH()
    testWebDip()

    #Creates the new text file
    with open("C:\Users\Jonathan\Documents\RSSsites.txt", "w") as f:
        for k, v in siteDict.iteritems():
            f.write(k + "\n")
            f.write(str(int(v) + incDict[k]) + "\n")
