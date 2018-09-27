#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

################################################################################
## General Site Config
################################################################################

LOCALE = ("en_US", "usa")

AUTHOR = 'Fi Dot'
SITENAME = 'B-Log'
SITESUBTITLE = 'Building Stuff'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

DESCRIPTION = "Steen Skybolt N79FT builder's log, blog, and website. "
KEYWORDS = "eaa,e/ab,test,check";

SITEURL = 'http://fix.me'

################################################################################
## Source, output paths, URLs and similar
################################################################################

PATH = 'sample_content'
#PATH = 'minimal'
#ARTICLE_PATHS = ['mock']
PAGE_PATHS = ['pages']
STATIC_PATHS = ['logos']

B_LOG_LOG_EXTENSION = 'log'

OUTPUT_PATH = '../test_site'

B_LOG_BLOG_CATEGORY = 'blog'
B_LOG_DEFAULT_PROJECT = 'Default Project'

# URL and pages options
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Where to save build logs for projects
B_LOG_LOGS_URL = 'logs'

################################################################################
## B-Log Theme Settings
################################################################################

THEME = '../b-log/theme'
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives', '404'));

B_LOG_DATE_FORMAT = "%b %d, %Y"

################################################################################
## Navigation
################################################################################

MENU_MAIN = (
               ( 'Home', '/'), 
               ( 'About', '/pages/about/'), 
               ( 'Blog', '/category/blog.html'), 
               ( 'Archive', '/archives.html'), 
               ( 'Subscribe (RSS)', '/rss.xml'),
            );

MENU_INCLUDE_TAGS = 1

# Note - at the moment collapsible projects are NOT supported. 
# Doing this would require re-building Bootstrap config I used, and 
# I unfortunately do  not have it :( So basically, the second
# element of the tuple is ignored

B_LOG_PROJECTS_MENU = ( 
                        (B_LOG_DEFAULT_PROJECT, "COLLAPSED"),
                        ("project.one", "OPEN"),
                        ("project.two", "ALWAYS_OPEN"),
                      )

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

################################################################################
## Pelican Options
################################################################################

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_RSS = "rss.xml"

AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Plugins

PLUGIN_PATHS = ['../b-log/plugins']

PLUGINS = ['image_copy', 'figure_process', 'b_log', 'qotd', 'sitemap' ]

# Date formats for articles and pages
DATE_FORMATS = { 'en' : '%b %d, %Y' };

# Figure Processing Options
FIG_PROC_REGEN_THUMBS = 0

# Path and Filename Processiog
USE_FOLDER_AS_CATEGORY = 0
PATH_METADATA = '(?P<category>[^/].*)/(?P<slug>.*)/(.*)'

# Misc

DEFAULT_PAGINATION = 10

# DO NOT REENABLE -- GIT WILL SCREW ITSELF UP AND OVER!!
#DELETE_OUTPUT_DIRECTORY= 0
DELETE_OUTPUT_DIRECTORY=0
# FIXME it's possible to prevent deleting .git dir - check this

ARTICLE_URL = 'entries/{category}-{slug}/'
ARTICLE_SAVE_AS = 'entries/{category}-{slug}/index.html'

PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

# Have to have these
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
