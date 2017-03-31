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
