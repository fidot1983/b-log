import os
import logging
import shutil
import pprint
 
from pelican import signals
from pelican.generators import Generator
from pelican.readers import BaseReader
from pelican.utils import mkdir_p
 
logger = logging.getLogger(__name__)
 
class ImgTraverser(BaseReader):

     def read(self, source_path):
       metadata = { 'path' : source_path};
       content = "Article path: " + source_path;
       return content, metadata;
