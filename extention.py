import os

from app.main import create_app, db, jwt
from flask_migrate import Migrate

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
migrate = Migrate(app, db)