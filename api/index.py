import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

app = Flask(__name__)

   # XXX: The Database URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = *****
DB_PASSWORD = ******

DB_SERVER = *****
# postgresql://sa4129:Welcome201@w4111project1part2db.cisxo09blonu.us-east-1.rds.amazonaws.com/proj1part2
DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


# Here we create a test table and insert some values in it
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")



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
  return render_template("index.html")

 
#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/login_page')
def login_page():
  print(request.args)
  return render_template("login.html")

@app.route('/dues')
def dues():
  global uid
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM Dues")
  dues = []
  print("PRINTING DUES")
  for due in cursor:
    print(due)
    if due[3] == uid:
      dues.append(due)
  
  cursor.close()

  context = dict(due_list = dues)
  return render_template("dues.html", **context)

@app.route('/open_hours')
def open_hours():
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM Open_Hours")
  open_hours = []
  print("PRINTING open_hours")
  for hour in cursor:
    print(hour)
    open_hours.append(hour)
  
  cursor.close()

  context = dict(hour_list = open_hours)
  return render_template("open_hours.html", **context)

@app.route('/work_days')
def work_days():
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM Work_Days")
  work_days = []
  print("PRINTING work_days")
  for day in cursor:
    print(day)
    work_days.append(day)
  
  cursor.close()

  context = dict(day_list = work_days)
  return render_template("work_days.html", **context)

@app.route('/clone')
def clone():
  print(request.args)
  return render_template("index2.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print(name)
  cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
  g.conn.execute(text(cmd), name1 = name, name2 = name);
  return redirect('/')

uid = -1
@app.route('/login', methods=['POST'])
def login():
  global uid
  print(request.args)
  email = request.form['email']
  phone = request.form['phone']
  print("Submitted Email, Phone :",email,phone)
  cursor = g.conn.execute("SELECT * FROM Users")

  for result in cursor:
    # print(result)
    if result[3] == email and result[4] == phone:
      print("Successful login :",result)
      uid = result[0]
      context = dict(data = result)
      return render_template("user_home.html", **context)
  #   names.append(result['first_name'])  # can also be accessed using result[0]
  # cursor = g.conn.execute("SELECT name FROM test")
  # for result in cursor:
  #   names.append(result['name'])
  cursor.close()
  print("Login Unsuccessful!")
  return redirect('/login_page')



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
