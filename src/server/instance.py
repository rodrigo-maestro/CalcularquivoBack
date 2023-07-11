from flask import Flask
from flask_restx import Api

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'txt'}

class Server():
    def __init__(self, ):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.app.config['MAX_CONTEXT_LENGTH'] = 16 * 1000 * 1000
        self.app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
        self.api = Api(self.app,
            version='1.0',
            title='Calcularquivo',
            description='API para calcular',
            doc='/docs'
        )

    def run(self, ):
        self.app.run(
            debug=True
        )

server = Server()