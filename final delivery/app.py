from flask import *
import os
import ibm_db
import bcrypt
from functools import partial,wraps

conn = ibm_db.connect('DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=rwb71462;PWD=XGg6dmPJELe3XGEK','','')
app = Flask(__name__) 
app.secret_key = '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'
PEOPLE_FOLDER = os.path.join('static', 'people_photo')

#IN THIS FILE ONLY SPRINT-2 ACTIONS ARE AVAILABLE


@app.route("/")
def login():
   

    return render_template('login.html')

@app.route('/login_api',methods=['GET','POST'])
def login_api():
    query1_e = 'SELECT * FROM users WHERE email = ?'
    query2_e = 'SELECT * FROM orgusers WHERE email = ?'
    email = request.form['email']
    password = request.form['password']
    stm_e1 = ibm_db.prepare(conn,query1_e)
    ibm_db.bind_param(stm_e1,1,email)
    res = ibm_db.execute(stm_e1)
    d = ibm_db.fetch_assoc(stm_e1)
    stm_e2 = ibm_db.prepare(conn,query2_e)
    ibm_db.bind_param(stm_e2,1,email)
    res = ibm_db.execute(stm_e2)
    d1 = ibm_db.fetch_assoc(stm_e2)

    print(d)
    print(d1)
    print(email)
    print(password)
    if d!=False:
      if password == d['PASSWORD'] :
          return redirect(url_for('home'))
    if d1!=False:
      if password == d1['PASSWORD']:
          return redirect(url_for('jobpost'))
    return "<div style='margin: 300px;'><center><div><h2>Invalid Data</h2></div></center></div>"

@app.route("/register")
def register():
    return render_template('register.html')
    
@app.route("/register_api",methods=['GET','POST'])
def register_api():
  fname = request.form['firstname']
  lname = request.form['lastname']
  dob = request.form['dob']
  qlf = request.form['qlf']
  skills = request.form['skills']
  email = request.form['email']
  password = request.form['password']
  query = 'insert into users (fname,lname,dob,qlf,skills,email,password) VALUES(?,?,?,?,?,?,?)'
  stm = ibm_db.prepare(conn,query)
  ibm_db.bind_param(stm,1,fname)
  ibm_db.bind_param(stm,2,lname)
  ibm_db.bind_param(stm,3,dob)
  ibm_db.bind_param(stm,4,qlf)
  ibm_db.bind_param(stm,5,skills)
  ibm_db.bind_param(stm,6,email)
  ibm_db.bind_param(stm,7,password)
  ibm_db.execute(stm)

  return 'success'

@app.route("/orgregister")
def orgregister():
  return render_template('orgregister.html')

@app.route("/orgregister_api",methods=['GET','POST'])
def orgregister_api():
  email = request.form['email']
  password = request.form['password']
  query = 'INSERT INTO orgusers(email,password) VALUES(?,?)' 
  stm = ibm_db.prepare(conn,query)
  ibm_db.bind_param(stm,1,email)
  ibm_db.bind_param(stm,2,password)
  ibm_db.execute(stm)
  return 'success'

@app.route("/jobpost")
def jobpost():
  
  return render_template('jobpost.html')
#----------SPRINT-1-----------------#

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    return redirect(url_for('home'))

@app.route('/success')
def suc():
  return render_template('suc.html')

@app.route('/home')
def home():
  query = 'SELECT * FROM job'
  stm = ibm_db.prepare(conn,query)
  res = ibm_db.execute(stm)
  d = ibm_db.fetch_assoc(stm)
  title = d['TITLE']
  skills = d['SKILLS']
  loc = d['LOC']
  sal = d['SALARY']
  return render_template('home.html',title=title,skills=skills,loc=loc,sal=sal)

@app.route('/postmsg',methods=['GET','POST'])
def postmsg():
  tit = request.form['jobtitle']
  skills = request.form['keyskills']
  location = request.form['location']
  salary = request.form['salary']
  query = 'insert into job(title,skills,loc,salary) VALUES(?,?,?,?)'
  stm = ibm_db.prepare(conn,query)
  ibm_db.bind_param(stm,1,tit)
  ibm_db.bind_param(stm,2,skills)
  ibm_db.bind_param(stm,3,location)
  ibm_db.bind_param(stm,4,salary)
  ibm_db.execute(stm)
  return render_template('postmsg.html')

@app.route("/orgregister",methods=['GET','POST'])
#----------SPRINT-1-----------------#

@app.route("/user_dashboard")
#----------SPRINT-1-----------------#


@app.route("/login",methods=['GET','POST'])
#----------SPRINT-1-----------------#


@app.route('/browse')
def addMarker():
  if 'loggedin' in session:
    query = "SELECT * FROM jobpost;"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.execute(stmt)
    a=[]
    isUser = ibm_db.fetch_assoc(stmt)
    
    while(isUser!=False):
      a.append(isUser)
      isUser = ibm_db.fetch_assoc(stmt)
  else:
    return redirect(url_for('login'))
  return render_template("browse.html",result=a)


@app.route('/companies')
def companies():
  if 'loggedin' in session:
    query = "SELECT * FROM RECRUITER"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.execute(stmt)
    a=[]
    isUser = ibm_db.fetch_assoc(stmt)
    
    while(isUser!=False):
      a.append(isUser)
      isUser = ibm_db.fetch_assoc(stmt)
  else:
    return redirect(url_for('login'))
  return render_template("companies.html",result=a)


@app.route("/jobpost1",methods=['GET','POST'])
def jobpost1():
  if 'loggedin' in session:
      if request.method == 'POST':
          recruiterid=request.form['recruiter_id']
          jobtitle = request.form['jobtitle'] 
          jobtype = request.form['jobtype']
          jobexp=request.form['jobexperience']
          keyskill=request.form['keyskills']
          location=request.form['location']
          salary=request.form['salary']
          discription=request.form['discription']

          insert_sql = "INSERT INTO JOBPOST (RECRUITER_ID,JOBTITLE, JOBTYPE, EXPERIENCE, KEYSKILL, LOCATION, SALARY, DISCRIPTION) VALUES (?,?,?,?,?,?,?,?)"

          prep_stmt = ibm_db.prepare(conn, insert_sql)
          ibm_db.bind_param(prep_stmt, 1, recruiterid)
          ibm_db.bind_param(prep_stmt, 2, jobtitle)
          ibm_db.bind_param(prep_stmt, 3, jobtype)
          ibm_db.bind_param(prep_stmt, 4, jobexp)
          ibm_db.bind_param(prep_stmt, 5, keyskill)
          ibm_db.bind_param(prep_stmt, 6, location)
          ibm_db.bind_param(prep_stmt, 7, salary)
          ibm_db.bind_param(prep_stmt, 8, discription)
          ibm_db.execute(prep_stmt)
  else:
      return redirect(url_for('login'))
  return render_template("jobpost.html")

@app.route("/browse/searchjob",methods=['GET','POST'])
def searchjob():
    if request.method=='POST':
        searchopt=request.form['searchopt']
        srctitle=request.form['srctitle']
        query = "SELECT * FROM JOBPOST WHERE "+searchopt+"="+chr(39)+srctitle+chr(39)
        stmt = ibm_db.prepare(conn, query)
        ibm_db.execute(stmt)
        a=[]
        isUser = ibm_db.fetch_assoc(stmt)
    
        while(isUser!=False):
          a.append(isUser)
          isUser = ibm_db.fetch_assoc(stmt)
    return render_template('browse.html',result=a)

if __name__ == "__main__": #checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    app.run(debug=True,port=8080) #running flask (Initalised on line 4)