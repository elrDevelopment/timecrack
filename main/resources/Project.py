from flask import Flask, request, current_app, jsonify
from flask_restful import Resource, Api, reqparse
from Model import Project as proj, ProjectSchema as proj_scma


projects = {}
project_schemas = proj_scma(many=True, strict=True)
project_schema = ()

parser = reqparse.RequestParser()

class Project(Resource):
    def get(self, proj_id):
        project = proj.get_one(proj_id)
        return {'status': 'success', 'data': project}, 201


class ProjectList(Resource):
    def get(self):
        projects = proj.get_all()
      
        response = project_schemas.dump(projects).data
        return response


