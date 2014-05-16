import os;
import logging;
import shutil;
import re;

from pelican import signals;

from pprint import pprint;

from docutils.parsers.rst import directives;
from docutils.parsers.rst import roles;
from docutils import nodes
from docutils.parsers.rst import Directive

from PIL import Image;

REGEN_THUMBS = 0;

class Figure(Directive):
   required_arguments = 0;
   optional_arguments = 1;
   option_spec = {'descrabove' : int};
   has_content = True;

   def run(self):
     no_lines = len(self.content);

     if (no_lines > 1):
      raise self.warning('Error in "%s" directive: multi-line descriptions not supported' % self.name);

     (source_img, img_path) = self.get_src_image();
     if not os.path.isfile(img_path):
       msg = 'Error in "%s" directive: Image referenced: "%s": is not a file!' % (self.name, source_img);
       raise(self.warning(msg));
     
     # CHEATING!!!
     html = "";
     thumb = self.create_thumb(img_path);
     html = html.join(('<div class="b-log-fig">\n',
                       ' <a ', 
                            'class="fancybox fancybox-thumb" ', 
                            'rel="figures" ', 
                            'href="{article}/', source_img, '" ', 
                            'title="', self.content[0], '" ', 
                            '>\n',
                       '   <img class="b-log-fig-img" src="{article}/',
                       thumb,
                       '">\n',
                       ' </a>',
                       '</div>\n'));

     attributes = {'format': 'html' };

     ret = nodes.raw('', html , **attributes);
     return [ret];

   def create_thumb(self, image_path):
     thumb_path = os.path.splitext(image_path)[0] + '-thumb.jpg';
     thumb_name = os.path.basename(thumb_path);

     if os.path.exists(thumb_path) and (not REGEN_THUMBS):
       return thumb_name;

     im = Image.open(image_path)
     im.thumbnail((570,570), resample=Image.ANTIALIAS);
     im.save(thumb_path, quality="maximum");

     return  thumb_name;

   def get_src_image(self):
     image_link = self.arguments[0];
     (src_file, line_no) = self.state_machine.get_source_and_line();
     image_path = os.path.join(os.path.dirname(src_file), image_link);
     return (image_link, image_path);

def init(pelican):
  directives.register_directive('fig', Figure);
  global REGEN_THUMBS;
  REGEN_THUMBS = pelican.settings['FIG_PROC_REGEN_THUMBS'];

def register():
  signals.initialized.connect(init);
  
  


