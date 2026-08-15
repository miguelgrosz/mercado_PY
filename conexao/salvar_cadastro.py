from fastapi import FastAPI, Form, Path #Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import pymysql


app = FastAPI()


# Libera o HTML acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Conexão MySQL
conexao = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="cadastro"
)


# CADASTRO
@app.post("/cadastro")
def cadastrar(
    nome: str = Form(...),
    senha: str = Form(...),
    email: str = Form(...)
):

    cursor = conexao.cursor()

    sql = """
    INSERT INTO usuarios (nome, senha, email)
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (nome, senha, email))

    conexao.commit()

    cursor.close()

    return RedirectResponse(
        url="http://127.0.0.1:5500/mercado_PY/frontend/pagina_login.html",
        status_code=303
    )



# LOGIN
@app.post("/login")
def login(
    nome: str = Form(...),
    senha: str = Form(...)
):

    cursor = conexao.cursor()

    sql = """
    SELECT * FROM usuarios
    WHERE nome=%s AND senha=%s
    """

    cursor.execute(sql, (nome, senha))

    usuario = cursor.fetchone()

    cursor.close()


    if usuario:
        return RedirectResponse(
            url="http://127.0.0.1:5500/mercado_PY/frontend/pagina_log.html",
            status_code=303
        )

    else:
        return {
            "mensagem": "Nome ou senha incorretos"
        }



# MOSTRAR USUÁRIOS
@app.get("/usuarios")
def listar_usuarios():

    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, nome, senha, email FROM usuarios"
    )

    usuarios = cursor.fetchall()

    cursor.close()

    return usuarios

@app.delete("/usuarios/{id}")
def excluir_usuario(id: int):

    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM usuarios WHERE id = %s",
        (id,)
    )

    conexao.commit()

    cursor.close()

    return {"mensagem": "Usuário excluído com sucesso"}


# @app.get("/paginadinamica/{caminho}")
# def paginaDinamica(response: Response):
#     txt = "<html><body><h1>Hellow</h1></body></html>"        
#     return Response(
#         content=txt, 
#         status_code=200, 
#         headers={"Content-Type": "text/html; charset=utf-8"}
#     )
