from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Produto(db.Model):
    __tablename__  = "produto"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column("nome", db.String(100))
    descricao = db.Column("descricao", db.String(100))
    preco = db.Column("preco", db.String(100))
    imagem = db.Column("imagem", db.String(100))
    def toJson(self):
      return {"id": self.id, "nome": self.nome, "descricao": self.descricao, "preco": self.preco, "imagem": self.imagem}

@app.route("/produto", methods=["GET"])
def selecionarProduto():
  try:
    produtos = Produto.query.all()
    produtoJson = [produto.toJson() for produto in produtos]
    return Response(json.dumps(produtoJson))
  except:
    return Response(json.dumps("Nao tem nenhum produto"))
  

@app.route("/produto/<id>", methods=["GET"])
def selecionarProdutoPorId(id):
  try:
    produto = Produto.query.filter_by(id=id).first()
    produtoJson = produto.toJson()
    return Response(json.dumps(produtoJson))
  except:
    return Response(json.dumps("Nao tem nenhum produto com esse id"))

@app.route("/produto", methods=["POST"])
def submitProduto():
  body = request.get_json()
  produto = Produto(nome=body["nome"], descricao=body["descricao"], preco=body["preco"], imagem=body["imagem"])
  db.session.add(produto)
  db.session.commit()
  return Response(json.dumps(produto.toJson()))

@app.route("/produto/<id>", methods=["PATCH"])
def atualizarPreco(id):
  produto = Produto.query.filter_by(id=id).first()
  body = request.get_json()
  produto.preco = body["preco"]
  db.session.add(produto)
  db.session.commit()
  return Response(json.dumps(produto.toJson()))

@app.route("/produto/<id>", methods=["DELETE"])
def deleteProduto(id):
  try:
    produto = Produto.query.filter_by(id=id).first()
    db.session.delete(produto)
    db.session.commit()
    return Response(json.dumps(produto.toJson()))
  except:
    return Response(json.dumps("Nao tem nenhum produto com esse id"))

with app.app_context():
  db.create_all()

app.run()