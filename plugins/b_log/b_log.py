import os;
import logging;
import shutil;
import sys;
import re;

import pelican 
from pelican import signals;
from pprint import pprint;
import inspect
import logging
import re

from pelican.utils import strftime

from sys import exit

logger = logging.getLogger(__name__)

DEFAULTS = {
             'B_LOG_LOG_EXTENSION': 'log', 
             'B_LOG_LOG_SEPARATOR': '|',

             'B_LOG_DEFAULT_PROJECT': 'Misc', 

             'B_LOG_BLOG_CATEGORY': 'Blog',
             'B_LOG_LOGS_URL': 'logs',
           } 

# Reader and parser for log files. 
# Note: this breaks with Pelican convention ... a bit. 
# There's basically no content - it will be generated 
# by the template (because some Articles log time, too) 
# So this just returns Metadata.. 
# Note: I tried to do this right, but apparently 
# this reader gets "found" and called 
# when processing articles, resulting in every .log
# file being processed as an "article" and added to the "article"
# list. Since we're using concept of "article" as a Log Entry here, 
# we can't really use the Reader; which'd be nice. 
# Therefore, the log files are actually read and parsed in the Generator. 
class LogsReader(pelican.readers.BaseReader):
  enabled = False

#  def __init__(self, *a, **kv):
#    super(LogsReader, self).__init__(*a, **kv)
#    pprint(inspect.trace())
#    raise Exception('INIT in Logs Reader')

  def read(self, filename):

    logger.debug(f"Log reader: reading {filename}")
    meta =  {
              'title': filename, 
              'date': '1900-1-1', 
              'slug': filename,
            }

    parsed = {}
    for k,v in meta.items():
      parsed[k] = self.process_metadata(k, v)

    return "", parsed


# Generates data structures necessary for the 
# Totals template in generate_context(); 
# and writes out the totals HTML using 
# the template in generate_output()
class TotalsGenerator(pelican.generators.Generator):
  files_root = None
  # I need this for process_metadata() call
  base_pelican_reader = pelican.readers.BaseReader({})

  def __init__(self, *args, **kwargs):
    super(TotalsGenerator, self).__init__(*args, **kwargs)
    self.files_root = self.settings['PATH']


  def generate_context(self):
    logger.debug("Totals generator generate_context() called")
    
    log_entries = self.generate_log_entries()
    project_logs = self.generate_project_logs(log_entries)
    self.context['B_LOG_PROJECT_LOGS'] = project_logs

  def generate_project_logs(self, log):
    ret = {}

    for cat, logs in log.items():
      if (cat.find('/') > 0):
        (project, category) = cat.split('/')
        self.append_log_entries(ret, project, log[cat], category) 
      else:
        # This prevents logging time in default project
        # Again, for now. 
        pass
    
    # Finally, sort log entries on a per-project basis
    for project in ret.values():
      project['entries'] = sorted(project['entries'], 
                                   key= lambda k: k['date'], 
                                   reverse=True)
    return(ret)

  def append_log_entries(self, target, project, logs, category):
    if project not in target:
      target[project] = cat_log_blank()
      target[project]['by_category'] = {}
      target[project]['url'] = ( self.context['B_LOG_LOGS_URL'] + "/" + 
                                 pelican.utils.slugify(f"{project}") + 
                                "-log.html")

    self.merge_logs(target[project], logs)
    target[project]['by_category'][str_to_title(category)] = logs['total']
     
  def merge_logs(self, target, source):
    target['count'] += source['count']
    target['total'] += source['total']
    target['entries'].extend(source['entries'])
    
  def generate_log_entries(self):
    ext = self.settings['B_LOG_LOG_EXTENSION']
    files = self.get_files(self.files_root, extensions=ext)

    article_log_entries = self.context['B_LOG_LOG_ENTRIES_FROM_ARTICLES']
    ret = {}

    for item in files:
      cat = os.path.dirname(item)
      logger.debug(f"Processing log: {item}")
      logger.debug(f" > Category: {cat}")

      log_entries = self.read_log_file(item)
      ret[cat] = log_entries

    # Add entries from articles to cats that also have logfiles
    for cat, log in ret.items():
      if(cat not in article_log_entries):
        continue
      logger.debug(f"  !! found articles in {cat}")
      self.merge_logs(log, article_log_entries[cat])

    # Now, add entries that ONLY have articles and no logfiles
    for cat, log in article_log_entries.items():
      if(cat not in ret):
        logger.debug(f"  !! found articles in {cat} that doesnt have logfiles")
        ret[cat] = log

    return(ret)

  def read_log_file(self, f):
    logger.debug(" > reading from file")
    full_path = f"{self.files_root}/{f}"
    line_no = 0
    log_sep = self.settings['B_LOG_LOG_SEPARATOR']

    ret = cat_log_blank()

    with open(full_path, "r") as fh:
      for line in fh:
        line_no += 1
        try:
          (date, summary, time) = line.split(log_sep)
        except Exception as e:
          logger.error(f"While parsing {full_path} line {line_no}: {e}")
          continue

        # Cheating a bit; but I need this to "normalize" dates 
        # to Pelican's standards
        date = self.base_pelican_reader.process_metadata('date', date)
        summary = summary.strip()

        # Time will be cleaned up by log_entry()
        entry = log_entry(date, summary, time)

        ret['total'] += entry['logged']
        ret['count'] += 1
        ret['entries'].append(entry)

    return(ret)

  def generate_output(self, writer):
     for project, logs in self.context['B_LOG_PROJECT_LOGS'].items():

        b_log_context = { 
                          'B_LOG_FOO': 'foo',
                          'B_LOG_PROJECT': project, 
                          'B_LOG_PROJECT_TITLE': 
                                  self.context['B_LOG_PROJECT_TITLES'][project],
                          'logs': logs
                        }

        writer.write_file(
                          logs['url'], 
                          template=self.get_template('log'), 
                          context=self.context, 
                          override_output=True,
                          relative_urls=self.settings['RELATIVE_URLS'],
                          **b_log_context,
                          )

# Extract totals out of the *articles*.
# This apparently is called BEFORE my Generator due to 
# Articles generator being called *first*. That's perfect.
# Also, organize Articles by Project
def process_articles(generator):
  logs = {}
  projects = {}
  pel_cat_map = { generator.context['B_LOG_BLOG_CATEGORY'] : "[Blog]" }
  default_project = generator.context['B_LOG_DEFAULT_PROJECT']

  for (pel_cat, articles) in generator.categories:
    catstr = stringify(pel_cat)
    if catstr.lower() == generator.context['B_LOG_BLOG_CATEGORY'].lower():
      logger.debug("!! FOUND BLOG CAT SKIPPING")
      continue;

    category_entry = cat_log_blank()

    if(catstr.find('/') > 0):
      (project, category) = catstr.split('/')
      add_project_cats(projects, project, category,  pel_cat)
      pel_cat_map[catstr] =("[" + str_to_title(project) + "]" + 
                            " " + str_to_title(category))
    else:
      add_project_cats(projects, default_project, catstr, pel_cat)
      pel_cat_map[catstr] = ("[" + str_to_title(default_project) + "]" + 
                             " " + str_to_title(catstr))

    for article in articles:
      if not 'logged' in article.metadata: continue;
      if not article.metadata['logged']: continue;

      entry = log_entry(article.metadata['date'], 
                        clean_summary(article), 
                        article.metadata['logged'])

      entry['article'] = article

      category_entry['total'] += entry['logged']
      category_entry['count'] += 1
      category_entry['entries'].append(entry)

    if category_entry['count'] > 0:
      logs[catstr] = category_entry;

  generator.context['B_LOG_LOG_ENTRIES_FROM_ARTICLES'] = logs
  generator.context['B_LOG_PROJECTS'] = projects
  generator.context['B_LOG_PROJECT_TITLES'] = cleanup_project_titles(projects.keys())
  generator.context['B_LOG_PEL_CAT_MAP'] = pel_cat_map

def cleanup_project_titles(projects):
  ret = dict((x, str_to_title(x)) for x in projects)
  return(ret)

def str_to_title(str):
  title = str
  title = re.sub("\W+", " ", title)
  title = re.sub("\s+", " ", title)
  return(title.title())

def add_project_cats(projects, project, category, pelican_cat):
  if project not in projects:
    projects[project] = []
  projects[project].append((str_to_title(category), pelican_cat))

def stringify(cat):
  return(f"{cat}")

def cat_log_blank():
  return({'total': 0, 'count': 0, 'entries': []})

def log_entry(date, summary, logged):
  return({'date': date, 
          'summary': summary, 
          'logged': float(logged)})

def clean_summary(article):
  summary = re.sub("<.*?>", "", article.summary).rstrip()
  return(summary)

def configure_b_log(pelican):
  for var, default in DEFAULTS.items():
    if var not in pelican.settings:
      pelican.settings[var] = default

# Hookups

def get_generators(pelican_object):
  return TotalsGenerator

def register():
  signals.initialized.connect(configure_b_log)
  signals.article_generator_finalized.connect(process_articles)
  signals.get_generators.connect(get_generators)
#  signals.readers_init.connect(add_readers)
