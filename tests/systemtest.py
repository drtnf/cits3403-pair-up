import unittest, os, time
from app import app, db
from app.models import Student, Project, Lab
from selenium import webdriver

#To do, find simple way for switching from test context to development to production.


class SystemTest(unittest.TestCase):
  driver = None
  
  def setUp(self):
    self.driver = webdriver.Firefox(executable_path=r'/home/drtnf/Dropbox/Tim/teaching/2019/CITS3403/pair-up/geckodriver')

    if not self.driver:
      self.skipTest('Web browser not available')
    else:
      db.init_app(app)
      db.create_all()
      s1 = Student(id='22222222',first_name='Test',surname='Case',cits3403=True)
      s2 = Student(id='11111111',first_name='Unit',surname='Test',cits3403=True)
      lab = Lab(lab='test-lab',time='now')
      db.session.add(s1)
      db.session.add(s2)
      db.session.add(lab)
      db.session.commit()
      self.driver.maximize_window()
      self.driver.get('http://localhost:5000/')

  def tearDown(self):
    if self.driver:
      self.driver.close()
      db.session.query(Student).delete()
      db.session.query(Project).delete()
      db.session.query(Lab).delete()
      db.session.commit()
      db.session.remove()
 
  def test_register(self):
    s = Student.query.get('22222222')
    self.assertEqual(s.first_name,'Test',msg='student exists in db')
    self.driver.get('http://localhost:5000/register')
    self.driver.implicitly_wait(5)
    num_field = self.driver.find_element_by_id('student_number')
    num_field.send_keys('22222222')
    pref_name = self.driver.find_element_by_id('prefered_name')
    pref_name.send_keys('Testy')
    new_pin = self.driver.find_element_by_id('new_pin')
    new_pin.send_keys('0000')
    new_pin2 = self.driver.find_element_by_id('new_pin2')
    new_pin2.send_keys('0000')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    submit = self.driver.find_element_by_id('submit')
    submit.click()
    #check login success
    self.driver.implicitly_wait(5)
    time.sleep(1)
    logout = self.driver.find_element_by_partial_link_text('Logout')
    self.assertEqual(logout.get_attribute('innerHTML'), 'Logout Testy', msg='Logged in')


if __name__=='__main__':
  unittest.main(verbosity=2)
