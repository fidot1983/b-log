import os
import logging
import shutil
import re

from pprint import pprint

from sys import exit;
 
from pelican import signals
from pelican.generators import Generator
from pelican.readers import BaseReader
from pelican.utils import mkdir_p, copy

 
logger = logging.getLogger(__name__)
 
INLINE_STATIC_EXTENSIONS = ('png', 'jpeg', 'jpg');
ARTICLE_TAG = '{article}';

def process_images(src, generator):

  for item in src:
    path = os.path.dirname(item.source_path);

    out_path = os.path.join(item._context['OUTPUT_PATH'], 
                            item.save_as);
    out_dir = os.path.dirname(out_path);

    prefix = '/';

    base_url = os.path.join(prefix, 
                            os.path.dirname(item.save_as));

    base_url = base_url.replace('\\', '/');

    if not os.path.exists(out_dir):
         os.makedirs(out_dir);

    for f in generator.get_files(path, 
                                 extensions=INLINE_STATIC_EXTENSIONS):
         src = os.path.join(item._context['PATH'], f);
         if not os.path.exists(os.path.join(out_dir, os.path.basename(src))):
           shutil.copy(src, out_dir);

    item._content = item._content.replace(ARTICLE_TAG, base_url);

def wrapper_articles(generator):
  process_images(generator.articles, generator)

def wrapper_pages(generator):
  process_images(generator.pages, generator)

def register():
#  def wrapper_articles(g):
#    process_images('articles', g)
#  def wrapper_pages(g):
#    process_images('pages', g)

#  signals.article_generator_finalized.connect(process_images)
  signals.article_generator_finalized.connect(wrapper_articles)
  signals.page_generator_finalized.connect(wrapper_pages)
