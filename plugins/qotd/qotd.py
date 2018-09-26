import os
import glob
import sys
import logging
from pprint import pprint 
import pelican.generators
from pelican import signals 
import inspect
import logging
import subprocess
import re
import io
import random

logger = logging.getLogger(__name__)

plugin_path = os.path.dirname(os.path.realpath(__file__))
qotd_path = f"{plugin_path}/quotes"


def add_qotd(generator):
  quotes = load_quotes()
  random.shuffle(quotes)

  idx = 0
  n = len(quotes)

  for article in generator.articles:
    article.qotd = quotes[ idx % n ]
    idx += 1

def load_quotes():
  ret = []

  for fn in glob.glob(f"{qotd_path}/*.txt"):
    quotes = ''
    with open(fn, 'r') as fh:
      quotes = fh.read()
    ret.extend([ add_html_tags(x) for x in quotes.split("\n%\n")])

  return(ret)


def add_html_tags(str):
  str = re.sub("\n", "<br>\n", str)
  return(str)
      

def register():
  signals.article_generator_finalized.connect(add_qotd)
