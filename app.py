from flask import Flask, jsonify, request
from config import app, db
from config import User

professores = []
turmas = []
alunos = []

# Rota para adicionar um professor
@app.route('/professores', methods=['POST'])
def add_professor():
    data = request.json
    novo_professor = {
        'id': len(professores) + 1,
        'nome': data['nome'],
        'idade': data['idade'],
        'materia': data['materia'],
        'observacoes': data.get('observacoes')
    }
    professores.append(novo_professor)
    return jsonify({'id': novo_professor['id']}), 201

# Rota para adicionar uma turma
@app.route('/turmas', methods=['POST'])
def add_turma():
    data = request.json
    nova_turma = {
        'id': len(turmas) + 1,
        'descricao': data['descricao'],
        'professor_id': data['professor_id'],
        'ativo': data.get('ativo', True)
    }
    turmas.append(nova_turma)
    return jsonify({'id': nova_turma['id']}), 201

# Rota para adicionar um aluno
@app.route('/alunos', methods=['POST'])
def add_aluno():
    data = request.json
    media_final = (data['nota_primeiro_semestre'] + data['nota_segundo_semestre']) / 2
    novo_aluno = {
        'id': len(alunos) + 1,
        'nome': data['nome'],
        'idade': data['idade'],
        'turma_id': data['turma_id'],
        'data_nascimento': data['data_nascimento'],
        'nota_primeiro_semestre': data['nota_primeiro_semestre'],
        'nota_segundo_semestre': data['nota_segundo_semestre'],
        'media_final': media_final
    }
    alunos.append(novo_aluno)
    return jsonify({'id': novo_aluno['id']}), 201

# Rota para listar professores
@app.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(professores)

# Rota para listar turmas
@app.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(turmas)

# Rota para listar alunos
@app.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(alunos)

# Rota para adicionar um usuário
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    password = data['password']
    new_user = User(username=username, password=password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

# Rota para listar todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(user_list)

# Suas rotas aqui...
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas definidas nos modelos
    app.run(debug=True, port=8000)  # Adicione o parâmetro port=8000
