import os
import zipfile
import io
import re

from flask import Flask, request, send_file
from flask_restx import Api, Resource

from src.server.instance import server

app, api = server.app, server.api

idUser = 1

@api.route('/arquivos')
class Arquivos(Resource):
    def get(self, ):
        files_dir = get_files_dir()
        pattern = f"_{idUser}.txt"

        filenames = [filename for filename in os.listdir(files_dir) if filename.endswith(pattern)]

        if filenames.count == 0:
            return
        
        zip_buffer = io.BytesIO()

        zipfile_name = f"arquivos_user_{idUser}.zip"

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in filenames:
                file_path = os.path.join(files_dir, filename)
                zipf.write(file_path, arcname=filename)

        zip_buffer.seek(0)

        return send_file(zip_buffer, download_name=zipfile_name, as_attachment=True)        
    
    def post(self, ):
        if 'file' not in request.files:
            return "Arquivo nao encontrado", 500
        
        file = request.files['file']

        if file and file.filename == '':
            return "Arquivo nao identificado", 500
        
        if allowed_file(file.filename):            
            file_path = save_file(file)
            calculate_file(file_path)
            return "Sucesso", 200

        return "Erro", 500

@api.route('/obterDadosArquivos')
class ObterDadosArquivos(Resource):
    def get (self, ):
        files_dir = get_files_dir()
        pattern = f"_{idUser}.txt"

        filenames = [filename for filename in os.listdir(files_dir) if filename.endswith(pattern)]

        return {"arquivos":filenames}, 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_unique_user_filename(filename, directory):
    base_name, extension = os.path.splitext(filename)

    unique_filename = f"{base_name}_{idUser}{extension}"
    
    counter = 0
    while os.path.exists(os.path.join(directory, unique_filename)):
        counter += 1
        unique_filename = f"{base_name}{counter}_{idUser}{extension}"

    return unique_filename

def save_file(file):
    file_dir = get_files_dir()

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    filename = get_unique_user_filename(file.filename, file_dir)

    file_path = os.path.join(file_dir, filename)

    file.save(file_path)

    return file_path

def get_files_dir():
    controllers_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(controllers_dir)
    files_dir = os.path.join(src_dir, app.config['UPLOAD_FOLDER'])

    return files_dir

def calculate_file(file_path):
    with open (file_path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            print(calculate_line(line))

def calculate_line(line):
    result = 0
    counter = 0
    current_operation = 0
    digits = re.findall(r'(\d+|\+|-|\*|\/|=)', line)
    for digit in digits:
        if digit == '=':
            return result

        if counter == 0:
            result += int(digit)        
        
        if digit == '+' or digit == '-':
            current_operation = digit
        elif digit.isnumeric():
            if current_operation == '+':
                result += int(digit)
            elif current_operation == '-':
                result -=int(digit)
                
        counter += 1

    return result
        