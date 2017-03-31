import os
from api import create_app, db
from api.models import Task
from flask_script import Manager, Shell
#from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app=app)#, Task=Task, db=db)

def make_shell_context():
    return dict(app=app)#, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
