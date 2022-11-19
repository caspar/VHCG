import os
from sqlalchemy import *
# from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, flash, session
# from flask_user import current_user, login_required, roles_required, UserManager, UserMixin #most of these are not yet implemented
from werkzeug.security import generate_password_hash, check_password_hash

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
SECRET_KEY=os.getenv('SECRET_KEY')
DB_SERVER=os.getenv('DB_SERVER')

# postgresql://sa4129:Welcome201@w4111project1part2db.cisxo09blonu.us-east-1.rds.amazonaws.com/proj1part2
DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"
app.secret_key = SECRET_KEY

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  # cursor = g.conn.execute("SELECT first_name FROM Users")
  # names = []
  # for result in cursor:
  #   names.append(result['first_name'])  # can also be accessed using result[0]
  # cursor = g.conn.execute("SELECT name FROM test")
  # for result in cursor:
  #   names.append(result['name'])
  # cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  # context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  # return render_template("index.html", **context)
  return render_template("cover.html")

 
#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
uid = -1
@app.route('/login')
def login():
  print(request.args)
  return render_template("login.html")

@app.route('/cover')
def cover():
  print(request.args)
  return render_template("cover.html")

@app.route('/register')
def register():
  print(request.args)
  return render_template("register.html")

@app.route('/dues')
def dues():
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM Dues")
  dues = []
  print("PRINTING DUES")
  i=1
  for due in cursor:
    if due[3] == session['uid']:
      print(due)
      managers = g.conn.execute("SELECT first_name, last_name FROM Users WHERE uid = " + str(due[4]))
      due_date = str(due[2].year) + "/" + str(due[2].month) + "/" + str(due[2].day)
      for manager in managers:
        pay = (i,due[1],due_date,manager[0]+" "+manager[1])
      dues.append(pay)
      i=i+1
  
  cursor.close()

  context = dict(due_list = dues)
  return render_template("dues.html", **context)

@app.route('/open_hours')
def open_hours():
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM Open_Hours")
  open_hours = []
  print("PRINTING open_hours")
  i=1
  for hour in cursor:
    slot = str(hour[1].year)+"/"+str(hour[1].month)+"/"+str(hour[1].day) + " - " + str(hour[1].hour)+":"+str(hour[1].minute) + " to " + str(hour[2].hour)+":"+str(hour[2].minute) #formatting
    print(slot)
    open_hours.append((i,slot))
    i = i+1
  
  cursor.close()

  context = dict(hour_list = open_hours)
  return render_template("open_hours.html", **context)

@app.route('/open_hours_attend')
def open_hours_attend():
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM Does")
  does = []
  print("PRINTING does")
  for done in cursor:
    print(done)
    does.append(done)
  
  cursor.close()

  context = dict(does_list = does)
  return render_template("open_hours_attend.html", **context)

@app.route('/workdays')
def workdays():
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM Work_Days")
  wd_signups = g.conn.execute("SELECT * FROM Work_Days W, Work_Day_Signups S, Users U WHERE W.work_date = S.work_date AND S.uid = U.uid")
  print("PRINTING SIGNUPS!!!!!!")

  work_day_signups = {}
  for signup in wd_signups:
    print(signup)
    signup_name = signup[5] + " " + signup[6] + " (" + str(signup[3]) + ")"
    if signup[0] in work_day_signups.keys():
      work_day_signups[signup[0]].append(signup_name)
    else:
      work_day_signups[signup[0]] = [signup_name]

  work_days = []
  print("PRINTING work_days")
  for day in cursor:
    print(day)
    if day[0] in work_day_signups.keys():
      workdate = str(day[0].year) + "/" + str(day[0].month) + "/" + str(day[0].day)
      work_days.append(((workdate,day[1]),work_day_signups[day[0]]))
    else:
      work_days.append((day,[]))
  
  cursor.close()

  context = dict(day_list = work_days)
  return render_template("workdays.html", **context)

@app.route('/register_work_date')
def register_work_date():
  print(request.args)
  work_date = request.args.get('work_date', None)
  print("PRINTING WORKDATE!!!")
  # print(work_date)
  # print(type(work_date))
  # print(str(work_date))
  try:
    cmd = 'INSERT INTO Work_Day_Signups VALUES '+"('"+str(work_date)+"',"+ str(session['uid'])+')';
    g.conn.execute(text(cmd));
  except:
    print("Error Signing up:",work_date,session['uid'])

  return redirect('/workdays')

@app.route('/plot_waitlist')
def plot_waitlist():
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM Plot_Waitlist P, Users U WHERE P.uid = U.uid")
  waitlist = []
  print("PRINTING waitlist")
  for rank in cursor:
    print(rank)
    rankname = str(rank[3]) + " " + str(rank[4]) + " (" + str(rank[0]) + ")"
    waitlist.append((rank[1],rankname))
  
  cursor.close()

  context = dict(wait_list = waitlist)
  return render_template("plot_waitlist.html", **context)

@app.route('/plot_assignments')
def plot_assignments():
  cursor = g.conn.execute("SELECT * From Plots P, Assigned A, Users U WHERE P.plot_id = A.plot_id AND A.uid = U.uid")
  assign = []
  for result in cursor:
    plot = "Plot #" + str(result[0])
    assigned = " assigned to " + result[7] + " " + result[8] + " (" + str(result[6]) + ") "
    assign.append(plot+assigned)
  
  cursor.close()
  context = dict(assign_list = assign)
  return render_template('plot_assignments.html',**context)

@app.route('/assign_plot', methods=['POST'])
def assign_plot():
  userid = request.form['uid']
  plot_id = request.form['plot_id']
  cmd = 'INSERT INTO Assigned VALUES (DEFAULT,' + str(userid) + ', ' + str(plot_id)+',null)';
  # try:
  g.conn.execute(text(cmd));
  # except:
  #   print("ERROR Assigning Plot to",uid)
  return redirect('/plot_assignments')

@app.route('/add_to_waitlist', methods=['POST'])
def add_to_waitlist():
  cursor = g.conn.execute("SELECT COUNT(*) FROM Plot_Waitlist")
  print("PRINTING WAITLIST LENGTH!!!")
  for num in cursor:
    print(num)
  cmd = 'INSERT INTO Plot_Waitlist VALUES (' + str(session['uid']) + ', ' + str(num[0]+1)+')';
  try:
    g.conn.execute(text(cmd));
  except:
    print("ERROR ADDING TO WAITLIST",session['uid'])
  return redirect('/plot_waitlist')

@app.route('/add_new_user', methods=['POST'])
def add_new_user():
  print(request.args)
  print("Registering New User :",request.form)
  first = request.form['first']
  last = request.form['last']
  email = request.form['email']
  phone = request.form['phone']
  address = request.form['address']
  password = generate_password_hash(request.form['password'],  method='sha256', salt_length=8)
  
  cmd = 'INSERT INTO Users VALUES (DEFAULT, (:v1), (:v2), (:v3), (:v4), (:v5), (:v6))';
  g.conn.execute(text(cmd), v1 = first, v2 = last, v3 = email, v4 = phone, v5 = address, v6 = password);
  return redirect('/login')

# Example of adding new data to the database
@app.route('/update_open_hours', methods=['POST'])
def update_open_hours():
  userid = request.form['uid']
  hours_id = request.form['hours_id']
  print("UPDATING OPEN HOURS :",userid,hours_id)
  cmd = 'INSERT INTO Does VALUES ((:v1), (:v2))';
  g.conn.execute(text(cmd), v1 = userid, v2 = hours_id);
  return redirect('/open_hours_attend')

@app.route('/check_login', methods=['POST'])
def check_login():
  global user_details
  print(request.args)
  email = request.form['email']
  password = request.form['password']
  print("Submitted Email, password :",email,password)
  users = g.conn.execute("SELECT * FROM Users")

  print("CHECKING LOGIN", flush=True)
  for user in users:
    print(user)
    if user[3] == email and (check_password_hash(user[6], password) or password == password): ##in the case of plain-text passwords
      print("Successful login :",user)
      session['uid'] = user[0]
      session['role'] = user[7]
      user_details = dict(data = user)
      return redirect('/home')

  users.close()
  print("Login Unsuccessful!")
  return redirect('/login')

@app.route('/home')
def home():
  global user_details
  if session['role'] in ['Leader', 'Owner', 'Admin']:
    return render_template("leader_home.html", **user_details)  

  if session['role'] == 'Member':
    return render_template("member_home.html", **user_details)  
  
  else:
    return render_template("user_home.html", **user_details)

@app.route('/admin_panel')
def admin_panel():
    users = []
    cursor = g.conn.execute("SELECT * FROM Users ORDER BY uid")
    for user in cursor:
      users.append(user)
    context = dict(user_list = users)
    return render_template("admin/admin_panel.html", **context)

@app.route('/change_role', methods=['GET','POST'])
def change_role():
  role = request.form.get('role')
  uid_update = request.form.get('uid')
  print(str(select))
  cmd = 'UPDATE Users SET Role = (:v1) WHERE uid = (:v2)';
  g.conn.execute(text(cmd), v1 = role, v2 = uid_update)
  return redirect('/admin_panel')

@app.route('/profile')
def profile():
  global user_details
  return render_template("auth/profile.html", **user_details)

@app.route('/update_info', methods=['POST'])
def update_info():
  uid = session['uid']
  first    = request.form.get('first')
  last     = str(request.form.get('last'))
  email    = request.form.get('email')
  phone    = request.form.get('phone')
  address  = str(request.form.get('address'))
  password = request.form.get('password')
  g.conn.execute(f'UPDATE USERS SET first_name = \'{first}\', last_name = \'{last}\', email =\'{email}\', phone = \'{phone}\', address =\'{address}\' WHERE uid = \'{uid}\'')
  if (password != ''):
    g.conn.execute(f'UPDATE USERS SET first_name = \'{generate_password_hash(password)}\' WHERE uid = \'{uid}\'')
  
  print('done')
  return redirect('/profile')

@app.route('/logout')
def logout():
    session.pop('uid', None)
    return redirect('/')

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
