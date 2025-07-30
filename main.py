import datetime

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnlog.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
bcrypt = Bcrypt(app)

jwt = JWTManager(app)
db = SQLAlchemy()
db.init_app(app)

from backend.models import User,Subject,Log
with app.app_context():
    db.create_all()
    print('Tables created')

@app.route('/')
def func():
    print('Done')
    return "Hello"

@app.route('/register',methods=['POST'])
def register():
    data= request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    user =User(name=name,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'Success'})

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    print(user)
    if user and password==user.password:
        return jsonify({'message':'Logged in'})
    return jsonify({'message':'Error , check your email and password'})

@app.route('/getUsers', methods=['GET'])  # Usually use GET for fetching data
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })
    return jsonify({'users': user_list})


@app.route('/subject', methods=['POST'])
def add_sub():
    subject = request.get_json()

    name = subject.get("name")
    user_id = subject.get("user_id")

    if not name or not user_id:
        return jsonify({'error': 'Name and user_id are required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    new_sub = Subject(name=name, user_id=user_id)
    db.session.add(new_sub)
    db.session.commit()

    return jsonify({'message': 'Subject added successfully', 'subject_id': new_sub.id})

@app.route('/add_log',methods=['POST'])
def add_log():
    log = request.get_json()
    content = log.get('content')
    date = log.get('date')
    subject_id = log.get('subject_id')
    new_log = Log(content=content,date=date,subject_id=subject_id)
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message':'success'})

@app.route('/remainder/')
def remainder():
    user  = User.query.get_or_404(1)
    for subject in user.subjects:
        today = datetime.date.today()
        for log in subject.logs:
           format_string = "%Y-%m-%d"

            # Convert the string to a datetime object

           log_date = log.date
           if isinstance(log_date,str):
               log_date = datetime.datetime.strptime(log_date,format_string).date()
           if (today - log_date).days>3:
                print(subject.name,': Please revise this one')

    return jsonify({'message':
                    'ok'})

@app.route('/revision/<int:log_id>',methods=['POST'])
def revision(log_id):
    log = Log.query.get_or_404(log_id)
    user = log.subject.user

    data = request.get_json()
    answers = data.get('answers')
    log.was_revised=True

    today = datetime.date.today()
    if( today- log.date).days==1:
        user.xp+=10
        user.streak+=1

    return jsonify({'message':'Revised'})

