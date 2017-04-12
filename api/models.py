from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from . import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False, index=True)
    #users = db.relationship('User', backref='role', lazy='dynamic')

    def to_json(self):
        json_task = {'url': url_for('api.get_task', task_id=self.id, 
                                                    _external=True),
                     'id': self.id,
                     'title': self.title,
                     'description': self.description,
                     'done': self.done
                    }
        return json_task

    @staticmethod
    def from_json(json_task):
        title = json_task.get('title')
        description = json_task.get('description','')
        if title is None or title == '':
            raise ValidationError('task does not have a title')
        return Task(title=title,
                    description=description)

    def __repr__(self):
        return '<Task %r>' % self.title

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        json_user = {'url': '',
                     'id': self.id,
                     'username': self.username}
        return json_user

    @staticmethod
    def from_json(json_user):
        username = json_user.get('username')
        if not username:
            raise ValidationError('user does not have a name')
        return User(username=username)

    def __repr__(self):
        return '<User %r>' % self.username


