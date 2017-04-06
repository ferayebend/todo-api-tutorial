from flask import url_for#current_app, request
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
    name = db.Column(db.String(32), unique=True)

    def to_json(self):
        json_user = {'url': '',
                     'id': self.id,
                     'name': self.name}
        return json_user

    @staticmethod
    def from_json(json_user):
        name = json_user.get('name')
        if not name:
            raise ValidationError('user does not have a name')
        return User(name=name)

    def __repr__(self):
        return '<User %r>' % self.name


