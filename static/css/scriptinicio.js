function mostrarFormulario(tipo) {
    const registro = document.getElementById("formularioRegistro");
    const trabajo = document.getElementById("formularioTrabajaConNosotros");


    // Ocultar ambos formularios
    registro.style.display = "none";
    trabajo.style.display = "none";

    // Mostrar el formulario seleccionado
    if (tipo === 'registro') {
        registro.style.display = "flex";
    } else if (tipo === 'trabajo') {
        trabajo.style.display = "flex";
    }
}


window.onclick = function(event) {
    const registro = document.getElementById("formularioRegistro");
    const trabajo = document.getElementById("formularioTrabajaConNosotros");

    if (event.target == registro) {
        registro.style.display = "none";
    }
    if (event.target == trabajo) {
        trabajo.style.display = "none";
    }
}

