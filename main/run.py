from flask import Flask
from flask_cors import CORS

def create_app(config_filename):
    app = Flask(__name__)
    
    app.config.from_object(config_filename)
    app.secret_key = '0CAE90CC-3930-4523-9EEC-F3E5178F734A'
    app.config['SESSION_TYPE'] = 'filesystem'

    cors = CORS(app, resources={r"/tc/api/v1.0/*": {"origins": "*"}})

    from app import api_bp
    
    app.register_blueprint(api_bp, url_prefix='/tc/api/v1.0')

    from Model import db
    
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)