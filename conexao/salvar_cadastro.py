
# Instala as bibliotecas necessárias:
# fastapi  -> cria a API
# uvicorn  -> servidor que executa a API
# pymysql  -> permite o Python conversar com o MySQL
# python-multipart -> permite receber dados enviados por formulário HTML

# Esse comando é executado no terminal, não dentro do código:
# pip install fastapi uvicorn pymysql python-multipart


# Importa o FastAPI para criar a API
# Importa Form para receber dados vindos de um formulário HTML
from fastapi import FastAPI, Form


# Importa a biblioteca que conecta o Python ao MySQL
import pymysql


# Cria a aplicação FastAPI
# O objeto "app" é o servidor da API
app = FastAPI()


# Cria uma conexão com o banco de dados MySQL
conexao = pymysql.connect(

    # Endereço do banco
    # localhost significa que o MySQL está no próprio computador
    host="localhost",

    # Usuário do MySQL
    user="root",

    # Senha do usuário MySQL
    password="root",

    # Banco que será utilizado
    database="cadastro"
)


# Cria uma rota da API
# Quando alguém enviar um POST para /cadastro,
# essa função será executada
@app.post("/cadastro")


# Função que recebe os dados enviados pelo HTML
def cadastrar(

    # Pega o campo "nome" do formulário
    # str significa que esperamos um texto
    # Form(...) significa que vem de um formulário
    # ... significa que é obrigatório
    nome: str = Form(...),


    # Pega o campo "senha" do formulário
    senha: str = Form(...),


    # Pega o campo "email" do formulário
    email: str = Form(...)

):


    # Cria um cursor.
    # O cursor é usado para mandar comandos SQL para o banco
    cursor = conexao.cursor()


    # Comando SQL que será executado
    #
    # O %s é um espaço reservado.
    # Depois ele será substituído pelos valores reais.
    sql = """
    INSERT INTO usuarios (nome, senha, email)
    VALUES (%s, %s, %s)
    """


    # Executa o comando SQL
    #
    # Aqui o Python troca:
    #
    # primeiro %s -> nome
    # segundo %s -> senha
    # terceiro %s -> email
    #
    cursor.execute(sql, (nome, senha, email))


    # Confirma a alteração no banco.
    # Sem o commit, o INSERT pode não ser salvo.
    conexao.commit()


    # Retorna uma resposta para quem chamou a API
    return {"mensagem": "Usuário cadastrado!"}