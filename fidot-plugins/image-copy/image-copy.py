from pelican import signals

def copy_images(instance):
  print("Article generator finalized!");
  

def register():
  signals.article_generator_finalized.connect(copy_images);

