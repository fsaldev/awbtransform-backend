import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app, db, path1

app.config['MONGOALCHEMY_DATABASE'] = 'awbtransport'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = path1

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()