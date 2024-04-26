import os
from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from celery.schedules import crontab

from application.models import db, User, Role, UserRole
from application.worker import cache

def create_app():
  app = Flask(__name__)
  current_dir=os.path.abspath(os.path.dirname(__file__))
  app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(current_dir,'db/lms_database.db')

  app.config["SECRET_KEY"] = "ufgaeihiogjarbjvjear"
  app.config["CELERY"] = {"broker_url": "redis://localhost:6379", 
                          "result_backend": "redis://localhost:6379"}


  db.init_app(app)
  datastore = SQLAlchemyUserDatastore(db, User, Role)
  app.security = Security(app, datastore)

  cache.init_app(app, {"CACHE_TYPE": "RedisCache",
                       "CACHE_DEFAULT_TIMEOUT": 10,
                       "CACHE_REDIS_URL": "redis://localhost:6379/0"})

  app.app_context().push()

  with app.app_context():
      db.create_all()

      if not Role.query.all():
        admin_role = app.security.datastore.create_role(name="admin")
        user_role = app.security.datastore.create_role(name="user")
        db.session.flush()

        admin = app.security.datastore.create_user(username="Harry", 
                                                   email="harry.potter@hogwarts.edu", 
                                                   password="tom")
        app.security.datastore.add_role_to_user(admin, admin_role)
        db.session.commit()

  return app

app = create_app()

from application.controllers import *
from application.worker import celery_init_app
from application.tasks import daily_reminder, report, autorevoke_issue

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
celery_app = celery_init_app(app)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(crontab(hour=20,minute=0), daily_reminder.s(), name='Daily Reminder')
  sender.add_periodic_task(crontab(hour=17,minute=0), autorevoke_issue.s(), name='Autorevoke Issue')
  sender.add_periodic_task(crontab(day_of_month='28',hour=12,minute=0), report.s(), name='Monthly Report')

if __name__=='__main__':
  app.run(host='127.0.0.1',port=5000,debug=True)