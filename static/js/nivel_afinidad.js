function actualizarNivelAfinidad(valor) {
    document.getElementById('nivelValor').textContent = `${valor}/100`;

    let nivel = '';
    if (valor <= 25) {
        nivel = 'Junior';
    } else if (valor <= 50) {
        nivel = 'Mid';
    } else if (valor <= 75) {
        nivel = 'Senior';
    } else {
        nivel = 'Expert';
    }

    document.getElementById('nivelTexto').textContent = nivel;
}
