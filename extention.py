import os

from app.main import create_app, db, create_catcher_app
from flask_migrate import Migrate

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app_catcher = create_catcher_app()
migrate = Migrate(app, db)