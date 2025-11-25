
#Importaciones
import time
from flask import Flask, request, jsonify, render_template, request_tearing_down
from flask_socketio import SocketIO, emit, send
from pathlib import Path
import json
import random


lista_de_usuarios = []
lista_de_opciones = []

#define la app Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta'
socketio = SocketIO(app, cors_allowed_origins='*')

#Ruta del index
@app.route('/')
def index():
    return render_template('index.html')




# CARGAR PAISES
ruta = Path('static/json/paises.json')
contenido = ruta.read_text()
paises = json.loads(contenido)

#Sortea un pais a adivinar
def sortear_pais():
    return random.choice(paises)


pais_a_adivinar = sortear_pais()

#Sortear opciones
def sortear_opciones(correcto):
    global lista_de_opciones
    lista_de_opciones.append(correcto)
    for i in range(3):
        selecionado = sortear_pais()['nombre']
        
        while selecionado == correcto:
            selecionado = sortear_pais()['nombre']
            if selecionado != correcto:
                break
        
        lista_de_opciones.append(selecionado)
        random.shuffle(lista_de_opciones)



#Socket que resive señal para cambiar de pais
@socketio.on('cambiar_pais')
def cambiar_pais():
    global lista_de_opciones
    lista_de_opciones.clear()
    global pais_a_adivinar
    pais_a_adivinar = sortear_pais()
    sortear_opciones(pais_a_adivinar['nombre'])
    emit('set_opciones',{'correcto': pais_a_adivinar, 'opciones': lista_de_opciones},broadcast=True)
    

#Socket que envia el resultado a todos los usuarios    
@socketio.on('resultado')
def resultado(data):
    if data == pais_a_adivinar['nombre']:
        emit('decir_resultado', request.sid, broadcast=True)    
    else:
        emit('nada','nada')
    



@socketio.on('get_contry')
def get_contry(data):
    global lista_de_opciones
    lista_de_opciones.clear()
    sortear_opciones(pais_a_adivinar['nombre'])
    emit('set_opciones',{'correcto': pais_a_adivinar, 'opciones': lista_de_opciones}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    global lista_de_opciones
    lista_de_opciones.clear()
    sortear_opciones(pais_a_adivinar['nombre'])
    
    if pais_a_adivinar:
        emit('set_opciones', {'correcto': pais_a_adivinar, 'opciones': lista_de_opciones},broadcast=True)
    else:
        emit('set_opciones', {'correcto': pais_a_adivinar, 'opciones': lista_de_opciones},broadcast=True)
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
