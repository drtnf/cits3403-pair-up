from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
  password_hash = db.Column(db.String(128))#overkill to hash a four digit pin, but included for learning.
  project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'),nullable=True) #assigned when project registered

  def registered(number):
    student = Student.query.filter_by(number = id.data).first()
    if student.password_hash is not None:
        raise validationError('Student is already registered')
    return True

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def is_committed(self):
    return self.project_id is not None

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

  def __repr__(self):
    return '[PID:{}, Desc:{},LabId:{}]'.format(\
        self.project_id,\
        self.description,\
        self.lab_id)
   
  def __str__(self):
    return 'Project {}: {}'.format(self.project_id,self.description)

  '''returns a list of students involved in the project'''
  def get_team(self):
    return Student.query.filter_by(project_id=self.project_id).all()

  def get_lab(self):
    lab = Lab.query.filter_by(project_id=self.project_id)\
        .add_columns(Lab.lab,Lab.time).first()
    return lab

    
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




