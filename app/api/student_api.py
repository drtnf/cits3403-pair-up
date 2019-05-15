from app import app, db
from app.models import Student,Project,Lab
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request, g, abort
from app.api.auth import token_auth


@app.route('/api/students/<id>',methods=['GET'])
@token_auth.login_required
def get_student(id):
  print(g.current_user)
  if g.current_user.id != id:
    abort(403)
  return jsonify(Student.query.get_or_404(id).to_dict())

@app.route('/api/students',methods=['POST'])
def register_student():
  data = request.get_json() or {}
  if 'id' not in data or 'pin' not in data:
    return bad_request('Must include student number and pin')
  student = Student.query.get(data['id'])
  if student is None:
    return bad_request('Unknown student')
  if student.password_hash is not None:
    return bad_request('Student already registered')
  student.from_dict(data)
  db.session.commit()
  response =jsonify(user.to_dict())
  response.status_code = 201 #creating a new resource should chare the location....
  response.headers['Location'] = url_for('get_student',id=student.id)
  return response

@app.route('/api/students/<id>',methods=['PUT'])
@token_auth.login_required
def update_student(id):
  if g.current_user.id != id:
    abort(403)
  data = request.get_json() or {}
  student = Student.query.get(id)
  if student is None:
    return bad_request('Unknown student')
  if student.password_hash is None:
    return bad_request('Student not registered')
  student.from_dict(data)
  db.session.commit()
  return jsonify(student.to_dict())

@app.route('/api/students/<id>/project',methods=['GET'])
@token_auth.login_required
def get_student_project(id):
  if g.current_user.id != id:
    abort(403)
  student = Student.query.get(id)
  if student is None:
    return error_response(404,'Student not found.') 
  if student.project_id is None:
    return error_response(404,'Student has no project') 
  project = Project.query.get(student.project_id)
  t = project.get_team()
  if len(t)==2:
    team = t[0].prefered_name +' & '+t[1].prefered_name
  else:
    team = t[0].prefered_name
  data = project.to_dict()  
  data['team'] = team
  return jsonify(data)

@app.route('/api/students/<id>/project',methods=['POST'])
@token_auth.login_required
def new_student_project(id):
  if g.current_user.id != id:
    abort(403)
  data = request.get_json() or {}
  if 'description' not in data or 'lab_id' not in data:
    return bad_request('Must include description and lab_id')
  student = Student.query.get(id)
  if student is None:
    return bad_request('Unknown student, or wrong id')
  if student.project_id is not None:
    return bad_request('Student already committed')
  partner=None
  if 'partner' in data:
    partner = Student.query.get(data['partner'])
    if partner is None:
      return bad_request("Unknown partner")
    if partner.project_id is not None:
      return bad_request('Partner already committed')
  if partner is None and student.cits3403:
    return bad_request('CITS3403 students require a partner')
  lab = Lab.query.get(data['lab_id'])
  if lab is None or not lab.is_available():
    return bad_request('Lab not available')
  #all good, create project
  project=Project();
  project.description = description
  project.lab_id=lab.lab_id 
  db.session.add(project)
  db.session.flush() #generates pk for new project
  student.project_id = project.project_id
  if partner is not None:
    partner.project_id=project.project_id   
  db.session.commit()
  response =jsonify(project.to_dict())
  response.status_code = 201 #creating a new resource should chare the location....
  response.headers['Location'] = url_for('new_student_project',id=student.id)
  return response


@app.route('/api/students/<id>/project',methods=['PUT'])
@token_auth.login_required
def update_student_project(id):
  if g.current_user.id != id:
    abort(403)
  print(request.data)  
  data = request.get_json() or {}
  print(data)
  if 'description' not in data or 'lab_id' not in data:
    return bad_request('Must include description and lab_id')
  student = Student.query.get(id)
  if student is None:
    return bad_request('Unknown student')
  if student.project_id is None:
    return bad_request('Student has no project')
  project = Project.query.get(student.project_id)
  team = project.get_team()
  if not team[0].id==g.current_user.id:
    partner = team[0]
  elif len(team)>1:
    partner = team[1]
  else:
    partner=None
  lab = Lab.query.get(data['lab_id'])
  if lab is None or (not lab.is_available() and lab.lab_id != project.lab_id):
    return bad_request('Lab not available')
  #all good, create project
  project.description = data['description']
  project.lab_id=lab.lab_id 
  student.project_id = project.project_id
  if partner is not None:
    partner.project_id=project.project_id   
  db.session.commit()
  return jsonify(project.to_dict())


@app.route('/api/students/<id>/project',methods=['DELETE'])
@token_auth.login_required
def delete_student_project(id):
  if g.current_user.id != id:
    abort(403)
  student = Student.query.get(id)
  if student is None:
    return bad_request('Unknown student, or wrong number')
  if student.project_id is None:
    return bad_request('Student does not have a project')
  project = Project.query.get(student.project_id)
  if project is None:
    return bad_request('Project not found')
  for s in project.get_team():
    s.project_id = None
  db.session.delete(project)
  db.session.commit()
  return jsonify(project.to_dict())
