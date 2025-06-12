document.querySelectorAll('.estado-columna').forEach((columna) => {
    Sortable.create(columna, {
        group: 'kanban',
        animation: 150,

        // ⚠️ Aquí validamos el movimiento antes de que ocurra
        onMove: function (evt) {
            const tarjeta = evt.dragged;
            const estadoActual = tarjeta.dataset.estado;
            const nuevoEstado = evt.to.id.replace('col-', '');

            // Solo permitir mover de oportunidad (1) a propuesta
            if (!((estadoActual === '2' && nuevoEstado === 'aprobado') || (estadoActual === '3' && nuevoEstado === 'propuesta'))) {
                return false; // impide el movimiento
            }

            return true;
        },

        // ✅ Esta función se ejecuta después del drop
        onEnd: function (evt) {
            const tarjeta = evt.item;
            const nuevoEstado = evt.to.id.replace('col-', '');
            const idProyecto = tarjeta.dataset.id;

            console.log(`Proyecto ${idProyecto} movido a estado ${nuevoEstado}`);

            fetch('/api/cambio_estado_caso_uso', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include', // necesario si usas sesiones
                body: JSON.stringify({ id: idProyecto, estado: nuevoEstado })
            }).then (() => {
                // Actualiza contadores y recarga la pagina
                actualizarContadoresEstados();
                location.reload();
            });
        }
    });
});
