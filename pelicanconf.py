#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'ZUBER Lionel'
SITENAME = 'Informatica Sapientaë'
#SITEURL = 'http://armaklan.org/blog'
SITEURL = ''

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'
LOCALE = ('fra',   # On Windows
    'fr_FR'     # On Unix/Linux
    )

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
FEED_ALL_RSS= 'feeds/all.rss'
CATEGORY_FEED_RSS= 'feeds/cat/%s.rss'
TAG_FEED_RSS= 'feeds/tag/%s.rss'
FEED_DOMAIN = SITEURL

# Blogroll
LINKS =  ()

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/armaklan'),
          ('G+', 'https://plus.google.com/115780595015515789252/posts'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#Theme
THEME="simple-bootstrap"
