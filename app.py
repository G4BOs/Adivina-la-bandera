import time
from flask import Flask, request, jsonify, render_template, request_tearing_down
from flask_socketio import SocketIO, emit, send
from pathlib import Path
import json
import random


lista_de_usuarios = []


app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')

# CARGAR PAISES
ruta = Path('static/json/paises.json')
contenido = ruta.read_text()
paises = json.loads(contenido)

def sortear_pais():
    return random.choice(paises)


pais_a_adivinar = sortear_pais()

@socketio.on('cambiar_pais')
def cambiar_pais():
    global pais_a_adivinar
    pais_a_adivinar = sortear_pais()
    emit('set_contry',pais_a_adivinar,broadcast=True)
    
    
@socketio.on('resultado')
def resultado(data):
    if data == pais_a_adivinar['nombre'].lower():
        emit('decir_resultado', request.sid, broadcast=True)    
    else:
        emit('nada','nada')
    



@socketio.on('get_contry')
def get_contry(data):
    emit('set_contry',pais_a_adivinar, broadcast=True)

@socketio.on('connect')
def handle_connect():
    if pais_a_adivinar:
        emit('decir_pais', pais_a_adivinar,broadcast=True)
    else:
        emit('set_contry', pais_a_adivinar,broadcast=True)
        emit('decir_pais', pais_a_adivinar,broadcast=True)


'''@socketio.on('unirse_como')
def add_usser(data):
    if lista_de_usuarios:
        for user in lista_de_usuarios:
            if user['nombre'] == data['nombre']:
                emit('usuario_registrado', user['nombre'])
            else:
                datos = {'nombre': data['nombre'], 'uid': request.sid}
                emit('usuario_registrado', user['nombre'])
    else:
                datos = {'nombre': data['nombre'], 'uid': request.sid}
                emit('usuario_registrado', user['nombre'])
'''


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
