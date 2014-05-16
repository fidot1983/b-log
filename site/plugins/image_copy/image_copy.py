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

    os.makedirs(out_dir);

    from pprint import pprint;
#    pprint(article.metadata);
#    exit(1);

    for f in generator.get_files(article_path, 
                                 extensions=INLINE_STATIC_EXTENSIONS):
#         print(f);
         src = os.path.join(article._context['PATH'], f);
#         print(" ", src, "\n", out_dir);
         shutil.copy(src, out_dir);



    article._content = article._content.replace(ARTICLE_TAG, base_url);

def register():
  signals.article_generator_finalized.connect(process_images);
#  signals.page_generator_finalized.connect(process_images);

 
'''
class InlineStaticGenerator(Generator):
    def generate_output(self, writer):
        self._generate_output_for(writer, 'articles')
        self._generate_output_for(writer, 'pages')
 
    def _generate_output_for(self, writer, domain):

        for article in self.context[domain] :
          article_path = os.path.dirname(article.source_path);

          out_path = os.path.join(article._context['OUTPUT_PATH'], 
                                  article.save_as);
          out_dir = os.path.dirname(out_path);

          base_url = os.path.join(article._context['SITEURL'], 
                                  os.path.dirname(article.save_as));
          base_url = base_url.replace('\\', '/');

          for f in self.get_files(article_path, 
                                  extensions=INLINE_STATIC_EXTENSIONS):
            src = os.path.join(article._context['PATH'], f);
            shutil.copy(src, out_dir);

          self.rewrite_urls_in_file(out_path, base_url);

    def rewrite_urls_in_file(self, fn, url):
#      print("File: ", fn);
#      print("URL: ", url);

      content = open(fn).read();

      if ARTICLE_TAG in content:
        content = content.replace(ARTICLE_TAG, url);
#        print(content);

#      print("----");
#      exit(1);



 
#def get_generators(pelican):
#    return InlineStaticGenerator

#def register():
#    pass
 
#signals.get_generators.connect(get_generators)
'''
