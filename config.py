import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'sshh!'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  SECRET_KEY = os.environ.get('SECRET_KEY')
#  SQLALCHEMY_DATABASE_URI = Postgres remote 

class DevelopmentConfig(Config):
  DEBUG=True

class TestingConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'tests/test.db')
  #SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' #in memory database
