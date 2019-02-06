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
    userid = db.Column(UUID(as_uuid=True))

class Tasks(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    sub_tasks = relationship('SubTask')

class SubTask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

class TimeTracking(db.Model):
    __tablename__ = 'time_tracking'
    id = db.Column(db.Integer, autoincrement=True, primarykey=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )

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



