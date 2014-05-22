import os;
import logging;
import shutil;
import re;

from pelican import signals;
from pprint import pprint;

from sys import exit;

def calculate_totals(generator):

  out = [];
  total_time = 0;

  for (cat, articles) in generator.categories:
    if cat in generator.context['MENU_SKIP_CATEGORIES']: 
      continue;

    entry = {'Category' : cat, 'Total' : 0, 'Count' : 0, 'Articles': articles };
    for article in articles:
      if not 'logged' in article.metadata: continue;
      if not article.metadata['logged']: continue;
      entry['Total'] += float(article.metadata['logged']);
      entry['Count'] += 1;

    if entry['Count'] > 0:
      out.append(entry);
      total_time += entry['Total'];

  generator.context['TOTALS_BY_LOGTYPE'] = out;
  generator.context['TOTALS_TOTAL' ] = total_time;


def register():
  signals.article_generator_finalized.connect(calculate_totals);


  
  


