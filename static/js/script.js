const socket = io();


const div_bandera = document.getElementById('bandera');
const btnCambiar = document.getElementById('btnCambiar');
btnCambiar.addEventListener('click',cambiarBandera);

const input_usr = document.getElementById('userinput');
const submit = document.getElementById('submit');
const resultado_txt = document.getElementById('resultado');

submit.addEventListener('click',()=>{
    if (input_usr.value.toLowerCase() == pais_a_adivinar['nombre'].toLowerCase()){
        resultado_txt.style.color = 'green';
        resultado_txt.innerHTML = 'CORRECTO BOBO';
        resultado_decir(input_usr.value.toLowerCase())
    }

    else{
        resultado_txt.style.color = 'red';
        resultado_txt.innerHTML = 'INCORRECTO BOBO'
    }
});



var pais_a_adivinar = {};
var registrado = false;



socket.on('set_contry',function(data){
    console.log(data.nombre);
    pais_a_adivinar = data;
    cambiar_bandera(pais_a_adivinar['imagen'])

});

socket.on('decir_resultado',function(data){
    resultado_txt.innerHTML = data
})

;

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
    socket.emit('cambiar_pais')
};

function resultado_decir(input){
    socket.emit('resultado', input)
}
