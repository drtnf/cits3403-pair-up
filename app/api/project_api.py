from app import app, db
from app.models import Student,Project,Lab
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request

@app.route('/api/projects/',methods=['GET'])
def list_projects():
  print('getting projects')
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
    projects.append({'pid':p.project_id,'team':team, 'description':p.description,'lab_id':p.lab_id,'lab':lab+' '+time})
  projects.sort(key = lambda p: p['lab_id'])  
  return jsonify({'projectList':projects})

@app.route('/api/labs/',methods=['GET'])
def get_available_labs():
  lab_id = request.args.get('lab_id')
  labs = Lab.get_available_labs()
  choices=[]
  for l in labs:
    choices.append({'lab_id':l.lab_id, 'lab': l.lab+' '+str(l.time)}) 
  return jsonify({'available_labs':choices})


