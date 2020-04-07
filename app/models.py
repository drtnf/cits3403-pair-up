import base64
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
from datetime import datetime, timedelta
import os

#allows login to get student from database, given id
#will be stored as current_user?
@login.user_loader
def load_student(id):
  return Student.query.get(int(id))

#student database will be prepopulated with 
# student numbers, firstname, surname, CITS3403 boolean
#students can add/edit pin and project id
class Student(UserMixin, db.Model):
  __tablename__='students'
  id = db.Column(db.String(8), primary_key = True)#prepopulate
  first_name = db.Column(db.String(64))#prepopulate
  surname = db.Column(db.String(64))#prepopulate
  prefered_name = db.Column(db.String(64))#defaults to first_name if empty
  cits3403 = db.Column(db.Boolean)#prepopulate
  password_hash = db.Column(db.String(128))#overkill to hash a four digit pin....
  project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'),nullable=True) 
  #token authetication for api
  token = db.Column(db.String(32), index=True, unique = True)
  token_expiration=db.Column(db.DateTime)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  ###Token support methods for api

  def get_token(self, expires_in=3600):
    now = datetime.utcnow()
    if self.token and self.token_expiration > now + timedelta(seconds=60):
      return self.token
    self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
    self.token_expiration = now+timedelta(seconds=expires_in)
    db.session.add(self)
    return self.token

  def revoke_token(self):
    self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

  @staticmethod
  def check_token(token):
    student = Student.query.filter_by(token=token).first()
    if student is None or student.token_expiration < datetime.utcnow():
      return None
    return student


  def is_committed(self):
    return self.project_id is not None

  def get_project(self):
    return Project.query.get(self.project_id)

  def get_partners(self):
    project = self.get_project()
    if not project:
      return None
    team = project.get_team()
    team.remove(self)
    return team

  '''Adding in dictionary methods to convert to JSON
     Format
     {
     'id':'19617810',
     'first_name':'Timothy',
     'surname': 'French',
     'prefered_name':'Tim',
     'cits3403':False,
     'pin':'0000',
     '_links':{
       'project': 'api/student/19617810/project'
      }
    }'''

  def to_dict(self):
    data = {
        'id': self.id,
        'first_name':self.first_name,
        'surname': self.surname,
        'prefered_name': self.prefered_name,
        'cits3403':self.cits3403,
        '_links': {'project':url_for('get_student_project',id = self.id)}
    }
    return data

  def from_dict(self, data):
    if 'prefered_name' in data:
      self.prefered_name=data['prefered_name']
    if 'pin' in data :
      self.set_password(data['pin'])

  def __repr__(self):
    return '[Number:{}, Name:{}, CITS3403:{}]'.format(self.id, \
      self.__str__(), \
      self.cits3403)
    
  def __str__(self):
    return self.first_name+' '+self.surname

#Projects are created editted by students
class Project(db.Model):
  __tablename__='projects'
  project_id = db.Column(db.Integer, primary_key = True)
  description = db.Column(db.String(64))
  lab_id = db.Column(db.Integer,db.ForeignKey('labs.lab_id'),nullable=True)

  '''returns a list of students involved in the project'''
  def get_team(self):
    return Student.query.filter_by(project_id=self.project_id).all()

  def get_lab(self):
    lab = Lab.query.filter_by(project_id=self.project_id)\
        .add_columns(Lab.lab,Lab.time).first()
    return lab

  def to_dict(self):
    data = {
        'id': self.project_id,
        'description': self.description,
        'lab_id':self.lab_id,
        'lab_name':str(Lab.query.get(self.lab_id))
        }
    return data

  def from_dict(self, data):
    if 'description' in data:
      self.description = data['description']
    if 'lab_id' in data and Lab.query.get(data['lab_id']).is_available():
      self.lab_id = data['lab_id']

  def __repr__(self):
    return '[PID:{}, Desc:{},LabId:{}]'.format(\
        self.project_id,\
        self.description,\
        self.lab_id)
   
  def __str__(self):
    return 'Project {}: {}'.format(self.project_id,self.description)

    
#demonstration lab times are prepopulated and intended to be immutable
class Lab(db.Model):
  __tablename__='labs'
  lab_id = db.Column(db.Integer, primary_key=True)
  lab = db.Column(db.String(64))
  time = db.Column(db.String(64))

  def get_project(self):
    return Project.query.filter_by(lab_id=self.lab_id).first()

  def is_available(self):
    return self.get_project() is None

  def get_available_labs():
    labs = Lab.query.\
        outerjoin(Project, Lab.lab_id==Project.lab_id).\
        add_columns(Project.project_id,Lab.lab_id, Lab.lab, Lab.time).\
        filter(Project.project_id==None).all()
    return labs

  def __repr__(self):
    return '[LID:{}, Lab:{}, time:{}]'.format( \
        self.lab_id, \
        self.lab, \
        self.time)
   
  def __str__(self):
    return 'Lab {}: {}'.format(self.lab,self.time)




