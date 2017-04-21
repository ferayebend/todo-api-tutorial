import os
import sys
import subprocess
from api import create_app, db
from api.models import Task, User
from flask_script import Manager, Command, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app=app)
migrate = Migrate(app, db)

class CeleryWorker(Command):
    """Starts the celery worker."""
    name = 'celery'
    capture_all_args = True

    def run(self, argv):
        ret = subprocess.call(
            ['celery', 'worker', '-A', 'api.celery'] + argv)
        sys.exit(ret)

manager.add_command("celery", CeleryWorker())


def make_shell_context():
    return dict(app=app, db=db, Task=Task, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
