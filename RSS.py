# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 21:16:19 2013

@author: Jonathan Finnell
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
    k = r"http://www.batoto.net/read/_/188265/tower-of-god"
    testv, testc = map(int, siteDict[k].split())
    br = Browser()
    br.open((r"http://www.batoto.net/read/_/188265/"
             "tower-of-god_v1_ch1_by_the-company"))
    resp = br.reload()
    html = resp.read()
    soup = BeautifulSoup("".join(html))
    title = str(soup.find("title")).split()[4:8]
    if title != ["vol", str(testv), "ch", str(testc)]:
        webbrowser.open((r"http://www.batoto.net/read/_/188265/"
                         "tower-of-god_v1_ch1_by_the-company"))
        print "New Tower of God"
        print ""
        incDict[(r"http://www.batoto.net/read/"
                 "_/188265/tower-of-god")] = (int(title[1])-testv,
                                              int(title[3])-testc)
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
    elif notices.find("img", {"src": "images/icons/alert.png"})):
        webbrowser.open(br.geturl())
        print "It's your turn in WebDiplomacy"
        print ""
    elif notices.find("img", {"src": "images/icons/mail.png"}):
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

    #Tests the different websites, comment out the ones you don't want
    print ""
    testXKCD()    # xkcd (webcomic)
    testJL8()     # Justice League 8 (webcomic)
    testHxH()     # Hunter x Hunter (anime)
    testWebDip()  # webDiplomacy (board game)
    testToG()     # Tower of God (manga)

    #Creates the new text file
    with open(os.getcwd() + "\RSSsites.txt", "w") as f:
        for k, v in siteDict.iteritems():
            f.write(k + "\n")
            try:
                f.write(str(int(v) + incDict[k]) + "\n")
            except ValueError:
                try:
                    v = map(int, v.split())
                    f.write("{0} {1}\n".format(str(v[0] + incDict[k][0]),
                                               str(v[1] + incDict[k][1])))
                except TypeError:
                    f.write("{0} {1}\n".format(str(v[0]), str(v[1])))
