from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean())
    authenticated = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_role', 
                            backref=db.backref('users', lazy=True))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Section(db.Model):
  __tablename__ = 'section'
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(200), unique=True, nullable=False)
  desc = db.Column(db.String(200), nullable=False)

class Book(db.Model):
  __tablename__ = 'book'
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(200), unique=True, nullable=False)
  desc = db.Column(db.String(200))
  author = db.Column(db.String(200), nullable=False)
  section_id=db.Column(db.Integer,db.ForeignKey('section.id',ondelete='CASCADE'))
  rating=db.Column(db.Integer(),nullable=False)
  image = db.Column(db.Text)

class Issue(db.Model):
  __tablename__ = 'issue'
  id=db.Column(db.Integer(),primary_key=True)
  book_id=db.Column(db.Integer(),db.ForeignKey('book.id',ondelete='CASCADE'))
  user_id=db.Column(db.Integer(),db.ForeignKey('user.id',ondelete='CASCADE'))
  issue_date=db.Column(db.Date(),nullable=False)
  return_date=db.Column(db.Date(),nullable=False)
  returned=db.Column(db.Boolean(),nullable=False)

class Request(db.Model):
  __tablename__ = 'request'
  id=db.Column(db.Integer(),primary_key=True)
  book_id=db.Column(db.Integer(),db.ForeignKey('book.id',ondelete='CASCADE'))
  user_id=db.Column(db.Integer(),db.ForeignKey('user.id',ondelete='CASCADE'))

class Review(db.Model):
  __tablename__= 'review'
  id=db.Column(db.Integer(),primary_key=True)
  book_id=db.Column(db.Integer(),db.ForeignKey('book.id',ondelete='CASCADE'))
  user_id=db.Column(db.Integer(),db.ForeignKey('user.id',ondelete='CASCADE'))
  rating=db.Column(db.Integer(),nullable=False)
  review=db.Column(db.Text())