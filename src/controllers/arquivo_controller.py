import io

from flask import Flask, request, send_file
from flask_restx import Api, Resource

from src.server.instance import server
from src.services.arquivo_services import obter_dados_arquivo, obter_zip_arquivos, salvar_arquivo

api = server.api

id_usuario = 1

@api.route('/arquivos')
class Arquivos(Resource):
    def get(self, ):
        zip_buffer, nome_arquivo_zip = obter_zip_arquivos(id_usuario)

        return send_file(zip_buffer, download_name=nome_arquivo_zip, as_attachment=True)        
    
    def post(self, ):
        if 'file' not in request.files:
            return "Arquivo nao encontrado", 500
        
        file = request.files['file']

        if file and file.filename == '':
            return "Arquivo nao identificado", 500
        
        if salvar_arquivo(file, id_usuario):
            return "Sucesso", 200

        return "Erro", 500

@api.route('/obterDadosArquivos')
class ObterDadosArquivos(Resource):
    def get (self, ):
        arquivos = obter_dados_arquivo(id_usuario)

        return {"arquivos":arquivos}, 200