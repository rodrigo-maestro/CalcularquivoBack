from flask import Flask
from flask_restx import Api, Resource

from src.server.instance import server

app, api = server.app, server.api

arquivos_teste = [
    {'id':0, 'nome':'id1'},
    {'id':1, 'nome':'id2'}
]

@api.route('/arquivos')
class Arquivos(Resource):
    def get (self, ):
        return arquivos_teste
    
    def post (self, ):
        response = api.payload
        arquivos_teste.append(response)
        return response, 200