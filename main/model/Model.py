import datetime
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


ma = Marshmallow()
db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    display_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    tasks = relationship('Tasks')
    timetracking relationship('TimeTracking')
    userid = db.Column(UUID(as_uuid=True))

class Tasks(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    sub_tasks = relationship('SubTask')
    timetracking relationship('TimeTracking')
##sub task can be specified or just an instance of when the timer is started on a task
class SubTask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    timetracking relationship('TimeTracking')

class TimeTracking(db.Model):
    __tablename__ = 'time_tracking'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    tracking_type = db.Column(db.Integer) ##specifies what type of tracking is being stored (project = 1, task = 2, sub_task = 3)
    start_time = dbColumn(DateTime, default=datetime.datetime.utcnow) 
    stop_time = dbColumn(DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.String, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    subtask_id = db.Column(db.Integer, db.ForeignKey('subtask.id'))
    trackingid = db.Column(db.Integer) ##based on the tracking type this ties the start and 

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    auth = relationship("LocalAuth", uselist=False, back_populates="users")

class LocalAuth(db.Model):
    __tablename__ = 'local_auth'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    parent_id = Column(Integer, ForeignKey('user.id'))
    parent = relationship("Users", back_populates="local_auth")

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    note_type = db.Column(db.Integer) ##specifies what type of note is stored (project = 1, task = 2, sub_task = 3)



