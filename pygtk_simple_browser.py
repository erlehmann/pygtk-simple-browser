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

class SimpleBrowser:
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("Interface.GtkBuilder")
        builder.connect_signals(self)

        self.window = builder.get_object("window")
        self.addressbar = builder.get_object("addressbar")
        self.refreshbutton = builder.get_object("refreshbutton")
        self.stopbutton = builder.get_object("stopbutton")
        self.tabs = builder.get_object("tabs")

        self.tablist = []

    def get_current_tab(self):
        return self.tablist[self.tabs.get_current_page()]

    def get_tab(self, page_num):
        return self.tablist[page_num]

    def get_url(self):            
        return self.addressbar.get_text()

    def loadurl(self):
        url = self.get_url()
        if not "://" in url:
            url = "http://" + url

        tab = self.get_current_tab()
        tab.loadurl(url)

    def on_addressbar_activate(self, widget):
        self.loadurl()

    def on_gobutton_clicked(self, button):
        self.loadurl()

    def on_refreshbutton_clicked(self, button):
        tab = self.get_current_tab()
        tab.refresh()

    def on_stopbutton_clicked(self, button):
        tab = self.get_current_tab()
        tab.stoploading()

    def on_tabaddbutton_clicked(self, button):
        self.tab_add("about:blank")

    def on_tabclosebutton_clicked(self, button):
        self.tab_close()

    def on_tabs_switch_page(self, notebook, page, page_num):
        self.update_url_from_tab(page_num)
        self.update_refreshbutton_from_tab(page_num)
        self.update_stopbutton_from_tab(page_num)

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def set_progress(self, progress):
        self.addressbar.set_progress_fraction(progress)

    def set_title(self, tab, title):
        self.tabs.set_tab_label_text(tab, title)

    def set_url(self, url):
        self.addressbar.set_text(url)

    def show_refreshbutton(self, visibility):
        self.refreshbutton.set_visible(visibility)

    def show_stopbutton(self, visibility):
        self.stopbutton.set_visible(visibility)

    def tab_add(self, url):
        newtab = SimpleTab(self, url)
        self.tablist.append(newtab)

        self.tabs.append_page(newtab.get_widget())
        self.tabs.show_all()

    def tab_close(self):
        tab = self.tabs.get_current_page()
        del self.tablist[tab]

        self.tabs.remove_page(tab)

    def update_stopbutton_from_tab(self, page_num):
        tab = self.get_tab(page_num)
        loadstatus = tab.get_loadstatus()

        if loadstatus.value_nick != "finished" and loadstatus.value_nick != "failed":
            self.show_stopbutton(True)
        else:
            self.show_stopbutton(False)

    def update_refreshbutton_from_tab(self, page_num):
        tab = self.get_tab(page_num)
        loadstatus = tab.get_loadstatus()

        if loadstatus.value_nick == "finished" or loadstatus.value_nick == "failed":
            self.show_refreshbutton(True)
        else:
            self.show_refreshbutton(False)

    def update_url_from_tab(self, page_num):
        tab = self.get_tab(page_num)
        url = tab.get_url()
        self.set_url(url)

    def main(self):
        self.window.show_all()
        self.tab_add("http://example.org")
        self.show_stopbutton(False)

        gtk.main()

class SimpleTab:
    def __init__(self, browser, url):
        self.webview = webkit.WebView()
        self.webview.connect("title-changed", self.changetitle)
        self.webview.connect("load-progress-changed", self.changeprogress)
        self.webview.connect("load-started", self.loadstarted)
        self.webview.connect("load-finished", self.loadfinished)

        self.webview.open(url)

        self.scroller = gtk.ScrolledWindow()
        self.scroller.add(self.webview)

        if not browser:
            raise RuntimeError()
        self.browser = browser

    def changetitle(self, webview, frame, title):
        self.browser.set_title(self.get_widget(), title)

    def changeprogress(self, webview, amount):
        progress = amount / 100.0
        self.browser.set_progress(progress)

    def get_url(self):
        return self.webview.get_property("uri")

    def loadfinished(self, webview, frame):
        self.browser.show_refreshbutton(True)
        self.browser.show_stopbutton(False)
        self.browser.set_progress(0)

    def loadstarted(self, webview, frame):
        self.browser.show_refreshbutton(False)
        self.browser.show_stopbutton(True)
        self.browser.set_progress(0)

    def loadurl(self, url):
        self.webview.open(url)

    def refresh(self):
        self.webview.reload()

    def stoploading(self):
        self.webview.stop_loading()

    def get_loadstatus(self):
        return self.webview.get_property("load-status")

    def get_widget(self):
        return self.scroller

if __name__ == '__main__':
    Browser = SimpleBrowser()
    Browser.main()
