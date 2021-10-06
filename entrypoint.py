# entry point of app
import os
# import unittest

from flask_migrate import Migrate # sqlalchemy migrations using alembic
# from flask_script import Manager

from app.main import create_app, db
from app import blueprint

# for migrations when running "flask db migrate"
from app.main.model import user, blacklist

app = create_app(os.environ.get('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()

# manager = Manager(app)

migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)
