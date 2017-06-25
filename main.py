from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:1058@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key_string'


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password


# check if the user needs to log in for every incoming request
# run the function before the request handler is called
@app.before_request
def require_login():
    # add routes users don't need to log in to visit
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        redirect('/login')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.password == password:
            # the user has logged in
            session['email'] = email
            return redirect('/')
        else:
            return '<h1>Error</h1>'

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'email' in session:
        del session['email']
    return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        # validate user data
        existing_user = User.query.filter_by(email = email).first()
        if not existing_user:
            if password == verify:
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email
                return redirect('/')
            else:
                return '<h1>Password Error</h1>'
        else:
            return '<h1>Duplicate User</h1>'

    return render_template('register.html')   


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['task']
        new_task=Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html', title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)


@app.route('/delete-task', methods=['POST'])
def delete_task():
    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()