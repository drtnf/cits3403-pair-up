from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    projects = [{
            'id':'00',
            'name':'Pair up!',
            'team':'Tim and Miguel',
            'demonstration':{
                'location':'CSSE:2.01',
                'datetime':'Wednesday March 20, 2pm'
                }
            }]
    return render_template('index.html', projects=projects)
