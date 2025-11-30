
#Importaciones
import time
from flask import Flask, request, jsonify, render_template, request_tearing_down, session
from flask_socketio import SocketIO, emit, send
from pathlib import Path
import json
import random
import secrets
import os


lista_de_usuarios = {}
puntuacion = {}


#define la app Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='gevent')

#Ruta del index
@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = secrets.token_urlsafe(16)
        
    return render_template('index.html')


""""
RONDA ACTUAL
"""

ronda_actual = {
    'pais': {},
    'opciones':[],
    'betado': []
}

#Generar Ronda
def generar_ronda():
    ronda_actual['pais'] = sortear_pais()
    ronda_actual['opciones'] = sortear_opciones(ronda_actual['pais'])
    ronda_actual['betado'] = []

#Actualizar puntos
def puntos_totales():
    indice = 1
    global puntuacion
    for jugador in lista_de_usuarios:
        puntuacion[f'jugador_{indice}']['punto'] = 0
        puntuacion[f'jugador_{indice}']['id'] = jugador





puntos_totales()

# CARGAR PAISES
ruta = Path('static/json/paises.json')
contenido = ruta.read_text()
paises = json.loads(contenido)

#Sortea un pais a adivinar
def sortear_pais():
    return random.choice(paises)


pais_a_adivinar = sortear_pais()


#Verifica ususario nuevo conectado
def verificar_id(id):
    """Funcion para verificar si una id ya esta previamente conectado y devuelve su numero"""
    for user in puntuacion:
        if puntuacion[user]['id'] == id:
            return puntuacion[user]['mi_numero']
    return len(puntuacion)+1



#Sortear opciones
def sortear_opciones(correcto):
    """Funcion para sortear 4 opciones aleatorias donde la correcta se pasa como argumento"""
    
    lista_de_opciones = []
    lista_de_opciones.append(correcto['nombre'])
    for i in range(3):
        selecionado = sortear_pais()['nombre']
        
        while selecionado == correcto:
            selecionado = sortear_pais()['nombre']
            if selecionado != correcto:
                break
        
        lista_de_opciones.append(selecionado)
    random.shuffle(lista_de_opciones)
    return lista_de_opciones



#Socket que resive señal para cambiar de pais
@socketio.on('cambiar_pais')
def cambiar_pais():
    generar_ronda()
    emit('set_opciones',{'correcto': ronda_actual['pais'], 'opciones': ronda_actual['opciones'],'betado':ronda_actual['betado'],'puntuacion':puntuacion},broadcast=True)
    

#Socket que envia el resultado a todos los usuarios    
@socketio.on('resultado')
def resultado(data):
    
    
    if str(data['entrada']) == ronda_actual['pais']['nombre'] and str(data['id']) not in ronda_actual['betado']:
        

        puntuacion[f'jugador {data["jugador"]}']['punto'] += 1
        
        emit('decir_resultado', puntuacion, broadcast=True)
        emit('mi_id',{'id':data['id'],'betado': (data['id'] in ronda_actual['betado']),'mi_numero':data['jugador']})    
    else:
        
        if data['id'] not in ronda_actual['betado']:
            ronda_actual['betado'].append(data['id'])
        if len(lista_de_usuarios) == len(ronda_actual['betado']):
            time.sleep(3)

            print(puntuacion)
            emit('decir_resultado',puntuacion, broadcast=True)
        
        emit('mi_id',{'id':data['id'],'betado': (data['id'] in ronda_actual['betado']),'mi_numero':data['jugador']})
    




@socketio.on('get_contry')
def get_contry(data):
    global lista_de_opciones
    lista_de_opciones.clear()
    sortear_opciones(pais_a_adivinar['nombre'])
    emit('set_opciones',{'correcto': ronda_actual['pais'], 'opciones': ronda_actual['opciones'],'betado':ronda_actual['betado'],'puntuacion':puntuacion}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    user_id = session.get('user_id')
    lista_de_usuarios[user_id] = request.sid
    
    mi_numero = verificar_id(user_id)
    puntos = 0
    if f'jugador {mi_numero}' in puntuacion:
        if 'punto' in puntuacion[f'jugador {mi_numero}']:
            puntos = puntuacion[f'jugador {mi_numero}']['punto']
    
    
    puntuacion[f'jugador {mi_numero}'] = {'id': user_id , 'punto': puntos, 'mi_numero': mi_numero}
    


    


    if ronda_actual['pais']:
        emit('set_opciones', {'correcto': ronda_actual['pais'], 'opciones': ronda_actual['opciones'],'betado':ronda_actual['betado'],'puntuacion':puntuacion},broadcast=True)
    else:
        generar_ronda()
        emit('set_opciones', {'correcto': ronda_actual['pais'], 'opciones': ronda_actual['opciones'],'betado':ronda_actual['betado'],'puntuacion':puntuacion },broadcast=True)
        emit('decir_pais', ronda_actual['pais'],broadcast=True)
    emit('mi_id',{'id':user_id,'betado': (user_id in ronda_actual['betado']), 'mi_numero': mi_numero})

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
    port = int(os.environ.get('PORT',5000))
    socketio.run(app, host='0.0.0.0', port=port)
