from flask import Flask, request
from flask_restx import Api, Resource

from src.server.instance import server

app, api = server.app, server.api

arquivos_teste = [
    {'id':1, 'nome':'id1'},
    {'id':2, 'nome':'id2'}
]

@api.route('/arquivos')
class Arquivos(Resource):
    def get (self, ):
        return arquivos_teste
    
    def post (self, ):
        if 'file' not in request.files:
            return "Arquivo nao encontrado", 500
        
        file = request.files['file']
        print(file)
        return arquivos_teste, 200