from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

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

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('login requested for student {}, remember_me={}'.format(form.studentNumber.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',title="Sign in", form = form)
