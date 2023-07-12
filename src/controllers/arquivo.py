import os

from flask import Flask, request, send_file
from flask_restx import Api, Resource

from src.server.instance import server

app, api = server.app, server.api

@api.route('/arquivos')
class Arquivos(Resource):
    def get(self, ):
        file_path = os.path.join(files_dir(),'somaBasica.txt')

        return send_file(file_path, as_attachment=True)
    
    def post(self, ):
        if 'file' not in request.files:
            return "Arquivo nao encontrado", 500
        
        file = request.files['file']

        if file and file.filename == '':
            return "Arquivo nao identificado", 500
        
        if allowed_file(file.filename):
            save_file(file)
            return "Sucesso", 200

        return "Erro", 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def unique_filename(filename, directory):
    base_name, extension = os.path.splitext(filename)
    counter = 0
    unique_filename = filename
    
    while os.path.exists(os.path.join(directory, unique_filename)):
        counter += 1
        unique_filename = f"{base_name}{counter}{extension}"

    return unique_filename

def save_file(file):
    target_dir = files_dir()

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    filename = unique_filename(file.filename, target_dir)

    file_path = os.path.join(target_dir, filename)

    file.save(file_path)

def files_dir():
    controllers_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(controllers_dir)
    files_dir = os.path.join(src_dir, app.config['UPLOAD_FOLDER'])

    return files_dir