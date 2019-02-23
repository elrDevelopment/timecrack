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
    display_name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tasks = relationship('Tasks')
    timetracking =relationship('TimeTracking')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    User = relationship("User", foreign_keys=user_id)
    
    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.display_name = data.get('display_name')
        self.description = data.get('description')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Project.query.all()

    @staticmethod
    def get_one(id):
        return Project.query.get(id)


    def __repr(self):
        return '<id {}>'.format(self.id)


class Tasks(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    display_name = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    sub_tasks = relationship('SubTask')
    timetracking =relationship('TimeTracking')

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.display_name = data.get('display_name')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
       
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Tasks.query.all()

    @staticmethod
    def get_one(id):
        return Tasks.query.get(id)


    def __repr(self):
        return '<id {}>'.format(self.id)

class SubTask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    display_name = db.Column(db.String(256))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    timetracking = relationship('TimeTracking')


    def __init__(self, data):
        """
        Class constructor
        """
        self.display_name = data.get('display_name')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
       
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return SubTask.query.all()

    @staticmethod
    def get_one(id):
        return SubTask.query.get(id)


    def __repr(self):
        return '<id {}>'.format(self.id)


class TimeTracking(db.Model):
    __tablename__ = 'time_tracking'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    tracking = db.Column(JSON)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    subtask_id = db.Column(db.Integer, db.ForeignKey('subtask.id'))
    trackingid = db.Column(db.Integer) ##based on the tracking type this ties the start and 

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    auth = relationship("LocalAuth", uselist=False)
    username = db.Column(db.String(80), nullable=False)

    def __init__(self, data):
        """
        Class constructor
        """
        self.username = data.get('username')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
       
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_one(id):
        return User.query.get(id)


    def __repr(self):
        return '<id {}>'.format(self.id)


class LocalAuth(db.Model):
    __tablename__ = 'local_auth'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    password_hash = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    User = relationship("User", foreign_keys=user_id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    pubid  = db.Column(UUID(as_uuid=True), server_default= db.text("uuid_generate_v4()"), )
    note_type = db.Column(db.Integer) ##specifies what type of note is stored (project = 1, task = 2, sub_task = 3)
    note_text = db.Column(db.Text)

    def __init__(self, data):
        """
        Class constructor
        """
        self.note_text = data.get('note_test')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
       
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Tasks.query.all()

    @staticmethod
    def get_one(id):
        return Tasks.query.get(id)


    def __repr(self):
        return '<id {}>'.format(self.id)



class ProjectSchema(ma.ModelSchema):
    class Meta:
       model = Project

class TasksSchema(ma.Schema):
    class Meta:
        model = Tasks

class SubTaskSchema(ma.Schema):
    class Meta:
        model = SubTask

class TimeTrackingSchema(ma.Schema):
    class Meta:
        model = TimeTracking

class UserSchema(ma.Schema):
    class Meta:
        model = User

class LocalAuthSchema(ma.Schema):
    class Meta:
        model = LocalAuth

class NotesSchema(ma.Schema):
    class Meta:
        model = Notes