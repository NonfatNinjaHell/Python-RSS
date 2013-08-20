# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 21:16:19 2013

@author: Jonathan
"""

import os
import urllib2
import webbrowser
from BeautifulSoup import BeautifulSoup

from mechanize import Browser


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


def testToG():
    testv, testc = map(int, siteDict[(r"http://www.batoto.net/read/"
                                      "_/188265/tower-of-god")].split())
    f = urllib2.urlopen((r"http://www.batoto.net/read/"
                         "_/188265/tower-of-god_v{0}_ch{1}_by_the-company")
                        .format(testv, testc))
    g = urllib2.urlopen((r"http://www.batoto.net/read/"
                         "_/188265/tower-of-god_v{0}_ch{1}_by_the-company")
                        .format(testv, testc + 1))
    h = urllib2.urlopen((r"http://www.batoto.net/read/"
                         "_/188265/tower-of-god_v{0}_ch{1}_by_the-company")
                        .format(testv+1, 1))
    fsoup = BeautifulSoup("".join(f))
    gsoup = BeautifulSoup("".join(g))
    hsoup = BeautifulSoup("".join(h))
    print fsoup.find("title")
    print gsoup.find("title")
    print hsoup.find("title")
    if hsoup.find("title") != gsoup.find("title"):
        webbrowser.open(h.geturl())
        print "New Tower of God"
        print ""
        incDict[(r"http://www.batoto.net/read/"
                 "_/188265/tower-of-god")] = (1, -1*testc + 1)
    elif gsoup.find("title") != fsoup.find("title"):
        webbrowser.open(g.geturl())
        print "New Tower of God"
        print ""
        incDict[(r"http://www.batoto.net/read/"
                 "_/188265/tower-of-god")] = (0, 1)
    else:
        incDict[(r"http://www.batoto.net/read/"
                 "_/188265/tower-of-god")] = (0, 0)


def testWebDip():
    br = Browser()
    br.open("http://webdiplomacy.net/logon.php")
    br.select_form(nr=0)
    br['loginuser'] = "USERNAMEHERE"
    br['loginpass'] = "PASSWORDHERE"
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
        print "You have mail in WebDiplomacy"
        print ""

if __name__ == "__main__":
    #Creates the necessary dictionaries
    with open(os.getcwd() + "\RSSsites.txt") as f:
        siteDict = {}
        for i, line in enumerate(f.readlines()):
            if i % 2 == 0:
                temp = line[:-1]
            else:
                siteDict[temp] = line[:-1]
        del i, line, temp
    incDict = {k: 0 for k in siteDict.keys()}

    #Tests the different websites, comment out those you don't want to check
    print ""
    testXKCD()
    testJL8()
    testHxH()
    testWebDip()
    testToG()

    #Creates the new text file
    with open(os.getcwd() + "\RSSsites.txt", "w") as f:
        for k, v in siteDict.iteritems():
            f.write(k + "\n")
            try:
                f.write(str(int(v) + incDict[k]) + "\n")
            except ValueError:
                try:
                    v = map(int, v.split())
                    f.write("{0} {1}\n".format(v[0] + incDict[k][0],
                                               v[1] + incDict[k][1]))
                except TypeError:
                    f.write(v + "\n")
