import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'sshh!'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  ENV='production'

class DevelopmentConfig(Config):
  ENV='development'
  DEBUG=True

class TestingConfig(Config):
  ENV='testing'
  TESTING=True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'tests/test.db')
  #SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' #in memory database
