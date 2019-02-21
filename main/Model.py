import datetime
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import sessionmaker, relationship
from passlib.apps import custom_app_context as pwd_context


ma = Marshmallow()
db = SQLAlchemy()



class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    display_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    tasks = relationship('Tasks')
    timetracking =relationship('TimeTracking')
    userid = db.Column(UUID(as_uuid=True))

class Tasks(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    sub_tasks = relationship('SubTask')
    timetracking =relationship('TimeTracking')
##sub task can be specified or just an instance of when the timer is started on a task
class SubTask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    timetracking = relationship('TimeTracking')

class TimeTracking(db.Model):
    __tablename__ = 'time_tracking'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    tracking = db.Column(JSON)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    subtask_id = db.Column(db.Integer, db.ForeignKey('subtask.id'))
    trackingid = db.Column(db.Integer) ##based on the tracking type this ties the start and 

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    auth = relationship("LocalAuth", uselist=False, back_populates="user")
    username = db.Column(db.String(80), nullable=False)

class LocalAuth(db.Model):
    __tablename__ = 'local_auth'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    password_hash = db.Column(db.String(128))
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent = relationship("User", back_populates="local_auth")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    note_type = db.Column(db.Integer) ##specifies what type of note is stored (project = 1, task = 2, sub_task = 3)
