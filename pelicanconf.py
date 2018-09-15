#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

LOCALE = ("en_US", "usa")

AUTHOR = 'Fi Dot'
SITENAME = 'N79FT'
SITESUBTITLE = 'A Skybolt Story'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# DO NOT REENABLE -- GIT WILL SCREW ITSELF UP AND OVER!!
DELETE_OUTPUT_DIRECTORY= 0

DESCRIPTION = "Steen Skybolt N79FT builder's log, blog, and website. "
KEYWORDS = "eaa,e/ab,test,check";

# Paths

PATH = 'sample_content'
PAGE_PATHS = ['__static']
OUTPUT_PATH = '../test_site'

#ARTICLE_EXCLUDES = ([PAGE_DIR])

# URL and pages options
SITEURL = 'http://fix.me'
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

ARTICLE_URL = 'build/{category}-{slug}/'
ARTICLE_SAVE_AS = 'build/{category}-{slug}/index.html'

#YEAR_ARCHIVE_SAVE_AS = 'b-log/{date:%Y}/index.html'
#MONTH_ARCHIVE_SAVE_AS = 'b-log/{date:%Y}/{date:%b}/index.html'
#DAY_ARCHIVE_SAVE_AS = 'b-log/{date:%Y}/{date:%b}/{date:%d}/index.html'

# Have to have these
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

# THEME

THEME = 'theme'

DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives', 'buildlog'));
EXTRA_TEMPLATES_PATHS = (['buildlog']);

# TOP MENU

MENU_MAIN = (
               ( 'Home', '/'), 
               ( 'About', '/'), 
               ( 'Blog', '/category/blog.html'), 
            );

MENU_INCLUDE_TAGS = 1

MENU_SKIP_CATEGORIES = ['blog'];

MENU_INCLUDE_LINKS = 1
MENU_LINKS =  (
          ('Biplane Forum', 'http://www.biplaneforum.com/'),
          ('Steen Aerolab', 'http://www.steenaero.com/'),
          ('separator', ''), 
          ("Beej's SkyBolt", 'http://65degrees.net'), 
          ("South Jersey SkyBolt", 'http://southjerseypilot.com/'), 
          ('separator', ''), 
          ('TX EAA 187 (web)', 'http://eaa187.org'),
          ('TX EAA 187 (facebook)', 'https://www.facebook.com/eaa187'),
         );


# TAGS

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None


# Plugins

PLUGIN_PATHS = ['../b-log/plugins']
PLUGINS = ['image_copy', 'figure_process', 'totals' ]

# Figure Processing Options

FIG_PROC_REGEN_THUMBS = 0

# Path and Filename Processiog
USE_FOLDER_AS_CATEGORY = 0
PATH_METADATA = '(?P<category>[^/].*)/(?P<slug>.*)/(.*)'
# FIXME test
SLUGIFY_SOURCE = 'basename'
#FILENAME_METADATA = '(?P<slug>[^.]*).*'

# Misc

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing


