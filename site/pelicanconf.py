#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

print("Haha!");

AUTHOR = 'Fi Dot'
SITENAME = 'N79FT'

TIMEZONE = 'America/Chicago'
LOCALE = ("en_US", "usa")

DEFAULT_LANG = 'en'

DELETE_OUTPUT_DIRECTORY= 'true'

# URL and pages options

SITEURL = 'http://localhost:8000'
ARTICLE_URL = 'b-log/{date:%Y}/{date:%b}/{date:%d}/{category}-{slug}/'
ARTICLE_SAVE_AS = 'b-log/{date:%Y}/{date:%b}/{date:%d}/{category}-{slug}/index.html'

YEAR_ARCHIVE_SAVE_AS = 'b-log/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'b-log/{date:%Y}/{date:%b}/index.html'
DAY_ARCHIVE_SAVE_AS = 'b-log/{date:%Y}/{date:%b}/{date:%d}/index.html'

# THEME

THEME = 'themes/notmyidea'
CSS_FILE = 'fidot.css'
#THEME = 'themes/plumage-master'

# TOP MENU

MENU_MAIN = (
               ( 'Home', '/'), 
               ( 'About', '/'), 
            );

MENU_INCLUDE_TAGS = 1

MENUITEMS = (
             ('Home', '/'),
             ('separator', ''), 
             ('About', '/fixme'),
             ('separator', ''), 
             ('Build', '/categories.html'),
             ('Build Log and Totals', '/totals.html'), 
             ('separator', ''), 
             ('Misc', '/misc.html'),
            );

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False


# TAGS
TAG_CLOUD_STEPS = 4;

# XXX

#DOCUTILS_SETTINGS = { 'xxx' : 1 }


#TODO re-enable with the theme
AUTHOR_SAVE_AS = '';
AUTHORS_SAVE_AS = '';


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

SITESUBTITLE = 'A Skybolt Story'

# Paths

PATH = 'content'
STATIC_PATHS = ['images']


# Plugins

PLUGIN_PATH = 'plugins'
PLUGINS = ['image_copy', 'figure_process']

# Figure Processing Options

FIG_PROC_REGEN_THUMBS = 0


# Extra menu items

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('Root', '/'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

