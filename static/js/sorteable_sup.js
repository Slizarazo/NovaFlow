function actualizarContadoresEstados() {
    const estados = ['oportunidad', 'propuesta'];
    estados.forEach(estado => {
        const columna = document.getElementById(`col-${estado}`);
        const tarjetas = columna.querySelectorAll('.card');
        const th = document.getElementById(`count-${estado}`);
        if (th) {
            const textoBase = th.textContent.split('(')[0].trim();
            th.textContent = `${textoBase} (${tarjetas.length})`;
        }
    });
}

document.querySelectorAll('.estado-columna').forEach((columna) => {
    Sortable.create(columna, {
        group: 'kanban',
        animation: 150,

        onMove: function (evt) {
            const tarjeta = evt.dragged;
            const estadoActual = tarjeta.dataset.estado;             // "propuesta"
            const nuevoEstado = evt.to.id.replace('col-', '');       // "oportunidad"

            console.log(`Intentando mover de ${estadoActual} a ${nuevoEstado}`);

            const movimientoValido =
                (estadoActual === 'oportunidad' && nuevoEstado === 'propuesta') ||
                (estadoActual === 'propuesta' && nuevoEstado === 'oportunidad');

            if (!movimientoValido) {
                console.warn('❌ Movimiento no permitido');
                return false;
            }

            return true;
        },

        onEnd: function (evt) {
            const tarjeta = evt.item;
            const nuevoEstado = evt.to.id.replace('col-', '');
            const idProyecto = tarjeta.dataset.id;

            tarjeta.dataset.estado = nuevoEstado;

            console.log(`✅ Proyecto ${idProyecto} movido a estado ${nuevoEstado}`);

            fetch('/api/cambio_estado_caso_uso', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ id: idProyecto, estado: nuevoEstado })
            }).then(() => {
                actualizarContadoresEstados();
                location.reload();
            });
        }
    });
});