import unittest, os
from app import app, db
from app.models import Student, Project, Lab



class StudentModelCase(unittest.TestCase):

  def setUp(self):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'test.db')
    self.app = app.test_client()#creates a virtual test environment, with no server.
    db.create_all()
    s1 = Student(id='00000000',first_name='Test',surname='Case',cits3403=True)
    s2 = Student(id='11111111',first_name='Unit',surname='Test',cits3403=True)
    lab = Lab(lab='test-lab',time='now')
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(lab)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_password_hashing(self):
    s = Student.query.get('00000000')
    s.set_password('test')
    self.assertFalse(s.check_password('case'))
    self.assertTrue(s.check_password('test'))

  def test_is_committed(self):
    s = Student.query.get('00000000')
    self.assertFalse(s.is_committed())
    s2 = Student.query.get('11111111')
    lab = Lab.query.first()
    p = Project(description='test',lab_id=lab.lab_id)
    db.session.add(p)
    db.session.flush()
    s.project_id = p.project_id
    s2.project_id = p.project_id
    db.session.commit()
    self.assertTrue(s.is_committed())

if __name__=='__main__':
  unittest.main(verbosity=2)





