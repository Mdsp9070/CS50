from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db = SQL("sqlite:///lecture.db")

@app.route('/')
def index():
  rows = db.execute('select * from registrants')
  return render_template('index.html', rows=rows)

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  else:
    name = request.form.get('name')
    email = request.form.get('email')
    if not name:
      return render_template('apology.html', message='You must provide a name')
    if not email:
      return render_template('apology.html', message='You must provide an email address')
    db.execute('insert into registrants (name, email) values (?, ?)',name, email)
    return redirect('/')