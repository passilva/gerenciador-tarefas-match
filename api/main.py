from flask import Flask, render_template, request, redirect
import sqlite3
from typing import List

app = Flask(__name__)


class Tarefa:
  def __init__(self, id=None, descricao="", data="", prioridade="", concluida=False) -> None:
    self.id = id
    self.descricao = descricao
    self.data = data
    self.prioridade = prioridade
    self.concluida = concluida

conn = sqlite3.connect('tarefas.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE IF NOT EXISTS tarefas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  descricao TEXT NOT NULL,
  data TEXT NOT NULL,
  prioridade TEXT NOT NULL,
  concluida BOOLEAN NOT NULL
);
""")

#tarefas = []


def insert_tarefa(tarefa: Tarefa):
  cursor.execute(f"""
  INSERT INTO tarefas (descricao, data, prioridade, concluida)
  VALUES ('{tarefa.descricao}', '{tarefa.data}', '{tarefa.prioridade}', {tarefa.concluida});
  """)
  conn.commit()

def select_all_tarefas():
  cursor.execute("""
  SELECT * FROM tarefas;
  """)
  tarefas = cursor.fetchall()
  return [Tarefa(tarefa[0], tarefa[1], tarefa[2], tarefa[3], tarefa[4]) for tarefa in tarefas]

def delete_tarefa(id: int):
  cursor.execute(f"""
  DELETE FROM tarefas WHERE id = {id};
  """)
  conn.commit()

def update_tarefa(id:int):
  cursor.execute(f"""
  UPDATE tarefas SET concluida = 1 WHERE id = {id};
  """)
  conn.commit()




prioridade_para_valor = {"Alta": 1, "Media": 2, "Baixa": 3}


@app.route("/")
def index():
  tarefas = select_all_tarefas()
  tarefas_ordenadas = sorted(tarefas, key=lambda x: (prioridade_para_valor[x.prioridade], x.descricao))
  return render_template("index.html", tarefas=tarefas_ordenadas)


@app.route("/adicionar", methods=['POST'])
def adicionar_tarefa():
  tarefa = Tarefa(descricao=request.form['descricao'],  data=request.form['data'],  prioridade=request.form['prioridade'], concluida=False)
  insert_tarefa(tarefa)
  return redirect("/")


@app.route('/excluir/<int:tarefa_id>', methods=['DELETE'])
def excluir_tarefa(tarefa_id):
  delete_tarefa(tarefa_id)
  return '', 200


@app.route('/concluir/<int:tarefa_id>', methods=['PUT'])
def concluir_tarefa(tarefa_id):
  update_tarefa(tarefa_id)
  return redirect("/")


if __name__ == "__main__":
  app.run()

