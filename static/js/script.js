
const socket = io();


const div_bandera = document.getElementById('bandera');

const resultado_txt = document.getElementById('resultadoo');

var en_juego = true


var pais_a_adivinar = {};
var opciones = [];

var puntuaciones = {};

var registrado = false;
var mi_id_web = '';
var mi_numero = 0;
var mi_nombre = '';
var betado = false;


socket.on('set_opciones',function(data){
    pais_a_adivinar = data.correcto;
    opciones = data.opciones;
    puntuaciones = data.puntuacion;
    cargar_puntuacion()
    cambiar_bandera(pais_a_adivinar['imagen']);
    cargar_opciones()
});

socket.on('decir_resultado',function(data){
    cambiarBandera();
    en_juego = true;
    puntuaciones = data;
    cargar_puntuacion();
});
socket.on('mi_id',function(data){
    mi_id_web = data.id;
    betado = data.betado;
    mi_nombre = data.nombre;
    if (data.mi_numero){mi_numero = data.mi_numero;};
    
})
;

//Recibe el pais a adivinar//
socket.on('decir_pais',function(data){
    pais_a_adivinar = data
    cambiar_bandera(pais_a_adivinar['imagen'])
});

socket.on('usuario_registrado', function(data){

})

;

function get_contry(){
    socket.emit('get_contry','hello')
};


function cambiar_bandera(pais){
    div_bandera.style.backgroundImage = `url('/static/images/banderas/${pais}')`
};

function cambiarBandera(){
    socket.emit('cambiar_pais');
};

function resultado_decir(entrada){
    socket.emit('resultado', {'entrada':entrada,'id':mi_id_web, 'jugador':mi_numero}  );
};




// CARGAR OPCIONES//

const contenedor_de_opciones = document.getElementById('opciones');

function cargar_opciones(){
    contenedor_de_opciones.replaceChildren();
    for (let pais in opciones){
        const opcion = document.createElement("div");
        opcion.className =  'opcion';
        opcion.id = `opcion_${pais}`;
        opcion.innerHTML = `${opciones[pais]}`;
        contenedor_de_opciones.appendChild(opcion);
        opcion.addEventListener('click',function(){
            if (opcion.innerHTML == pais_a_adivinar.nombre && !betado)  {
                resultado_txt.innerHTML = "CORRECTO";
                opcion.style.backgroundColor = 'rgba(10,100,20,0.6)';
                resultado_decir(opcion.innerHTML)
                ;
    }
        else{resultado_txt.innerHTML = "INCORRECTO";
            opcion.style.backgroundColor = 'rgba(100,10,20,0.6)';
            resultado_decir(opcion.innerHTML);
            en_juego = false;
            

        }
        });
    }
    opciones = []
        ;
    
};

cargar_opciones();


const cuadro_de_puntos = document.getElementById('puntos');
function cargar_puntuacion(){
    cuadro_de_puntos.replaceChildren();
    for (let puntos in puntuaciones){

        var txt_puntos = document.createElement('p');
        txt_puntos.style.display = 'inline';
        txt_puntos.className= 'punto';
        txt_puntos.innerText = `${puntuaciones[puntos].nombre}: ${puntuaciones[puntos].punto}`
        if (puntuaciones[puntos].nombre == mi_nombre){
            txt_puntos.style.color = 'rgba(5, 248, 127, 1)';
        };
        cuadro_de_puntos.appendChild(txt_puntos)

        
    }
}

cargar_puntuacion();




