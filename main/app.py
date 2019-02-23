from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Project import Project, ProjectList

api_bp = Blueprint('api', __name__)

api = Api(api_bp)


# Route
api.add_resource(Hello, '/Hello', endpoint = 'hello')
api.add_resource(ProjectList, '/projects', endpoint = 'projects')
api.add_resource(Project, '/project/<int:id>', endpoint = 'project')