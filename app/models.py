from app import db

class Student(db.Model):
    number = db.Column(db.String(8), primary_key = True)
    firstName = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    cits3403 = db.Column(db.Boolean)
    project_id = db.Column(db.Integer, db.ForeignKey('project.pid'),nullable=True)

    def __repr__(self):
        return '[Number:{}, Name:{}, CITS3403:{}]'.format(number, self.str(), cits34403)
    
    def __str__(self):
        return firstName+' '+surname

class Project(db.Model):
    pid = db.Column(db.Integer, primary_key = True)
    team = db.relationship('Student', backref='project', lazy='dynamic')
    description = db.Column(db.String(64))
    demoLab = db.Column(db.String(64))
    demoTime = db.Column(db.DateTime)

    def __repr__(self):
      return '[PID:{}, Team:{}, Desc:{},Lab:{},Time:{}]'.format(pid,team,description,demoLab,demoTime.str())
   
    def __str__(self):
      return 'Project {}: {}'.format(pid,description)





