#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

# see also http://www.tuxradar.com/content/python-pygtk-webkit-20-minutes

import gtk
import webkit

class PyGTKSimpleBrowser:
    def __init__(self):
        self.urlinput = gtk.Entry()
        self.urlinput.connect("activate", self.loadurl)

        self.gobutton = gtk.Button(stock = gtk.STOCK_APPLY)
        self.gobutton.connect("clicked", self.loadurl)

        self.refreshbutton = gtk.Button(stock = gtk.STOCK_REFRESH)
        self.refreshbutton.connect("clicked", self.refresh)

        self.stopbutton = gtk.Button(stock = gtk.STOCK_STOP)
        self.stopbutton.connect("clicked", self.stoploading)

        self.toolbar = gtk.HBox()
        self.toolbar.pack_start(self.urlinput)
        self.toolbar.pack_start(self.gobutton, False)
        self.toolbar.pack_start(self.refreshbutton, False)
        self.toolbar.pack_start(self.stopbutton, False)
        
        self.browser = webkit.WebView()
        self.browser.connect("title-changed", self.changetitle)
        self.browser.connect("load-progress-changed", self.changeprogress)
        self.browser.connect("load-started", self.loadstarted)
        self.browser.connect("load-finished", self.loadfinished)

        self.scroller = gtk.ScrolledWindow()
        self.scroller.add(self.browser)

        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.toolbar, False)
        self.vbox.pack_start(self.scroller)

        self.window = gtk.Window()
        self.window.add(self.vbox)
        self.window.connect("destroy", self.destroy)
        self.window.set_title("A simple browser using PyGTK")

        self.window.show_all()

        self.stopbutton.set_visible(False)

    def changeprogress(self, webview, amount):
        progress = amount / 100.0
        self.urlinput.set_progress_fraction(progress)

    def changetitle(self, webview, frame, title):
        self.window.set_title(title)

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def loadurl(self, button):
        url = self.urlinput.get_text()

        if not "://" in url:
            url = "http://" + url
            self.urlinput.set_text(url)

        self.browser.open(url)

    def loadstarted(self, webview, frame):
        self.refreshbutton.set_visible(False)
        self.stopbutton.set_visible(True)

        self.urlinput.set_progress_fraction(0)

    def loadfinished(self, webview, frame):
        self.refreshbutton.set_visible(True)
        self.stopbutton.set_visible(False)
        self.urlinput.set_progress_fraction(0)

    def refresh(self, button):
        self.browser.reload()

    def stoploading(self, button):
        self.browser.stop_loading()

    def main(self):
        gtk.main()

if __name__ == '__main__':
    Browser = PyGTKSimpleBrowser()
    Browser.main()
