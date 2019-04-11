from flask import render_template, flash, redirect, url_for
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, ProjectForm
from app.models import Student, Project, Lab
from flask import request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
  if current_user.is_authenticated:
    projects = get_all_projects()
  else:  
    projects = []
  return render_template('index.html', projects=projects)

@app.route('/login', methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit(): #will return false for a get request
    student = Student.query.filter_by(id=form.student_number.data).first()
    if student is None or not student.check_password(form.pin.data):
      flash('invalid username or data')
      return redirect(url_for('login'))
    login_user(student, remember=form.remember_me.data)
    next_page = request.args.get('next')
    print(next_page)
    if not next_page or url_parse(next_page).netloc !='':
      next_page = 'index'
    return redirect(url_for(next_page))
  return render_template('login.html',title="Sign in", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
  print('register')
  form= RegistrationForm()#??include current user data by default
  print(form.validate_on_submit())
  if form.validate_on_submit(): #will return false for a GET request
    student = Student.query.filter_by(id=form.student_number.data).first()
    if student is None:
      flash('Unrecognized student number')
      return redirect(url_for('index'))
    if current_user.is_authenticated:
      if not student.check_password(form.pin.data):
        flash('Incorrect pin')
        return redirect(url_for('index'))
    elif student.password_hash is not None:
      flash('Student already registered. Login to edit details')
      return redirect(url_for('index'))
    student.set_password(form.new_pin.data)
    student.prefered_name = form.prefered_name.data
    db.session.commit()
    login_user(student, remember=False)
    return redirect(url_for('index'))
  return render_template('register.html', title='Register', form=form)


@app.route('/new_project', methods=['GET','POST'])
@login_required
def new_project():
  if not current_user.is_authenticated:
    return redirect(url_for('login'))
  if not current_user.project_id==None:
    flash(current_user.prefered_name+' already has a project')
    return redirect(url_for('index'))
  form=ProjectForm()
  form.lab.choices=get_labs()
  if form.validate_on_submit():#for post requests
    project=Project();#generate id
    project.description = form.project_description.data
    partner = Student.query.filter_by(id=form.partner_number.data).first()
    #illegal scenarios
    if partner is None and current_user.cits3403:
      flash('Partner not found')      
      return redirect(url_for('index'))
    elif partner is not None and (partner.is_committed() or partner.id==current_user.id):
      flash(partner.prefered_name+' already has a project assigned')
      return redirect(url_for('index'))
    else:
      #check lab availability
      lab=Lab.query.filter_by(lab_id=form.lab.data).first()
      if lab is None or not lab.is_available():
        flash("Lab not available")
      else:
        #Everything is good, make commits
        project.lab_id=lab.lab_id 
        db.session.add(project)
        db.session.flush() #generates pk for new project
        if partner is not None:
          partner.project_id=project.project_id   
        current_user.project_id = project.project_id
        db.session.commit()
        print('Project '+str(project)+'added')
        return redirect(url_for("index"))
  return render_template('new_project.html', student=current_user, form=form)


@app.route('/edit_project', methods=['GET','POST'])
@login_required
def edit_project():
  if not current_user.is_authenticated:
    return redirect(url_for('login'))
  project=Project.query.filter_by(project_id=current_user.project_id).first()
  if project==None:
    flash(current_user.prefered_name+' does not have a project yet')
    redirect(url_for('new_project'))
  team = project.get_team()
  if not team[0].id==current_user.id:
    partner = team[0]
  elif len(team)>1:
    partner = team[1]
  else:
    partner=None
  form=ProjectForm()#initialise with parameters
  form.lab.choices= get_labs(project.lab_id)
  if form.validate_on_submit():#for post requests
      lab=Lab.query.filter_by(lab_id=form.lab.data).first()
      if lab is None or not (lab.lab_id==project.lab_id or lab.is_available()):
        flash("Lab not available")
      else:
        project.description = form.project_description.data
        project.lab_id=lab.lab_id 
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("index"))
  return render_template('edit_project.html', student=current_user, partner=partner, project=project, form=form)


@app.route('/delete_project', methods=['GET'])
@login_required
def delete_project():
  if not current_user.is_authenticated:
    return redirect(url_for('login'))
  project=Project.query.filter_by(project_id=current_user.project_id).first()
  if project is None:
    flash(current_user.prefered_name+' does not have a project')
  else:
    flash(current_user.prefered_name+"'s project "+project.description+' deleted.')
    for s in project.get_team():
      s.project_id=None
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("index"))

'''returns list of registered projects as a list of dictionaries, with elements "project", "team" and "lab". Used by index to display project list.'''
def get_all_projects():
  projectList = Project.query.all()
  projects = []
  for p in projectList:
    t = p.get_team()
    if len(t)==2:
      team = t[0].prefered_name +' & '+t[1].prefered_name
    else:
      team = t[0].prefered_name
    l = Lab.query.filter_by(lab_id = p.lab_id).first()
    time = str(l.time)
    lab = l.lab
    projects.append({'project_id':p.project_id,'description':p.description,'team':team,'lab':lab,'time':time})
  projects.sort(key = lambda p: p['lab']+p['time'])  
  return projects 

'''Returns available labs formatted for a select input'''
def get_labs():
    labs = Lab.get_available_labs()
    choices = []
    for l in labs:
      choices.append((str(l.lab_id), l.lab+' '+str(l.time))) 
    return choices

'''Returns available labs formatted for a select input, including the current lab'''
def get_labs(lab_id):
    labs = Lab.get_available_labs()
    lab = Lab.query.get(lab_id)
    choices = [(str(lab.lab_id),lab.lab+' '+str(lab.time))]
    for l in labs:
      choices.append((str(l.lab_id), l.lab+' '+str(l.time))) 
    return choices
