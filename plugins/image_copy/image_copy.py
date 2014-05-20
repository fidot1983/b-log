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

def process_images(generator):
#  print("Image processing generator called");

  for article in generator.articles:
    article_path = os.path.dirname(article.source_path);

    out_path = os.path.join(article._context['OUTPUT_PATH'], 
                            article.save_as);
    out_dir = os.path.dirname(out_path);

    base_url = os.path.join(article._context['SITEURL'], 
                            os.path.dirname(article.save_as));
    base_url = base_url.replace('\\', '/');

    if not os.path.exists(out_dir):
         os.makedirs(out_dir);

    from pprint import pprint;
    for f in generator.get_files(article_path, 
                                 extensions=INLINE_STATIC_EXTENSIONS):
         src = os.path.join(article._context['PATH'], f);
         if not os.path.exists(os.path.join(out_dir, os.path.basename(src))):
           shutil.copy(src, out_dir);



    article._content = article._content.replace(ARTICLE_TAG, base_url);

def register():
  signals.article_generator_finalized.connect(process_images);
