
const socket = io();

const div_bandera = document.getElementById('bandera');

const resultado_txt = document.getElementById('resultadoo');

var en_juego = true


var pais_a_adivinar = {};
var opciones = [];
var registrado = false;



socket.on('set_opciones',function(data){
    pais_a_adivinar = data.correcto;
    opciones = data.opciones;
    cambiar_bandera(pais_a_adivinar['imagen']);
    cargar_opciones()
});

socket.on('decir_resultado',function(data){
    cambiarBandera();
    en_juego = true
});

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
    socket.emit('resultado', entrada);
};



// CARGAR OPCIONES//

const contenedor_de_opciones = document.getElementById('opciones');

function cargar_opciones(){
    contenedor_de_opciones.replaceChildren();
    for (let pais in opciones){
        console.log(opciones[pais]);
        const opcion = document.createElement("div");
        opcion.className =  'opcion';
        opcion.id = `opcion_${pais}`;
        opcion.innerHTML = `${opciones[pais]}`;
        contenedor_de_opciones.appendChild(opcion);
        opcion.addEventListener('click',function(){
            if (opcion.innerHTML == pais_a_adivinar.nombre && en_juego)  {
                resultado_txt.innerHTML = "CORRECTO";
                opcion.style.backgroundColor = 'rgba(10,100,20,0.6)';
                resultado_decir(opcion.innerHTML)
                ;
    }
        else{resultado_txt.innerHTML = "INCORRECTO";
            opcion.style.backgroundColor = 'rgba(100,10,20,0.6)';
            en_juego = false

        }
        });
    }
    opciones = []
        ;
    
};

cargar_opciones();





