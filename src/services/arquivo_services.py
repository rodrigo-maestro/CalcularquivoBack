import os
import re
import io
import zipfile

from src.server.instance import server

app = server.app

def obter_zip_arquivos(id_usuario):
    diretorio_arquivos = obter_diretorio_arquivos()
    regra_arquivo_usuario = obter_regra_arquivo_usuario(id_usuario)

    nomes_arquivos = [nome_arquivo for nome_arquivo in os.listdir(diretorio_arquivos) if nome_arquivo.endswith(regra_arquivo_usuario)]

    if nomes_arquivos.count == 0:
        return
        
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for nome_arquivo in nomes_arquivos:
            file_path = os.path.join(diretorio_arquivos, nome_arquivo)
            zipf.write(file_path, arcname=nome_arquivo)

    zip_buffer.seek(0)

    return zip_buffer, f"arquivos_usuario_{id_usuario}.zip"

def salvar_arquivo(file, id_usuario):
    if not arquivo_permitido(file.filename):
        return False

    diretorio_arquivos = obter_diretorio_arquivos()

    if not os.path.exists(diretorio_arquivos):
        os.makedirs(diretorio_arquivos)

    nome_arquivo = obter_nome_unico_arquivo_usuario(file.filename, diretorio_arquivos, id_usuario)

    diretorio_arquivo = os.path.join(diretorio_arquivos, nome_arquivo)

    file.save(diretorio_arquivo)

    return True

def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def obter_nome_unico_arquivo_usuario(nome_arquivo, diretorio_arquivos, id_usuario):
    nome_base, extensao = os.path.splitext(nome_arquivo)

    nome_unico = f"{nome_base}_{id_usuario}{extensao}"
    
    i = 0
    while os.path.exists(os.path.join(diretorio_arquivos, nome_unico)):
        i += 1
        nome_unico = f"{nome_base}{i}_{id_usuario}{extensao}"

    return nome_unico

def obter_dados_arquivo(id_usuario):
    diretorio_arquivos = obter_diretorio_arquivos()
    regra_arquivo_usuario = obter_regra_arquivo_usuario(id_usuario)

    nomes_arquivos = [nome_arquivo for nome_arquivo in os.listdir(diretorio_arquivos) if nome_arquivo.endswith(regra_arquivo_usuario)]
    
    arquivos = []

    for nome_arquivo in nomes_arquivos:
        arquivos.append({ "nome":nome_arquivo, "linhas": calcular_arquivo(os.path.join(diretorio_arquivos, nome_arquivo))})

    return arquivos

def obter_diretorio_arquivos():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_src = os.path.dirname(diretorio_atual)
    diretorio_arquivos = os.path.join(diretorio_src, app.config['UPLOAD_FOLDER'])

    return diretorio_arquivos

def obter_regra_arquivo_usuario(id_usuario):
    return f"_{id_usuario}.txt"

def calcular_arquivo(diretorio_arquivo):
    linhas_com_resultados = []
    with open (diretorio_arquivo) as arquivo:
        while True:
            linha = arquivo.readline()
            if not linha:
                break
            linhas_com_resultados.append(calcular_linha(linha))

    return linhas_com_resultados

def calcular_linha(linha):
    resultado = 0
    i = 0
    digito_atual = 0
    digitos = re.findall(r'(\d+|\+|-|\*|\/|=)', linha)
    for digito in digitos:
        if digito == '=':
            return f"{linha.strip()} {resultado}"

        if i == 0:
            resultado += int(digito)        
        
        if digito == '+' or digito == '-':
            digito_atual = digito
        elif digito.isnumeric():
            if digito_atual == '+':
                resultado += int(digito)
            elif digito_atual == '-':
                resultado -=int(digito)
                
        i += 1

    return resultado
        