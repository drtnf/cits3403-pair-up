from app import app, db
from app.models import Student, Project, Lab

@app.shell_context_processor
def make_shell_context():
  return {'db':db, 'Student':Student, "Project":Project, 'Lab':Lab}
