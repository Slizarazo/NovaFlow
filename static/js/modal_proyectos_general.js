document.addEventListener("DOMContentLoaded", function () {
        feather.replace();
        
        // Inicializar tooltips
        const tooltips = document.querySelectorAll('.tooltip-icon');
        tooltips.forEach(tooltip => {
            tooltip.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.2)';
            });
            tooltip.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });
    });

    function openOportunidadModal() {
        const modal = document.getElementById('nuevaOportunidadModal');
        if (modal) {
            // Limpiar formulario
            const form = document.getElementById('nuevaOportunidadForm');
            if (form) {
                form.reset();
            }
            
            // Mostrar modal
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.6)';
            modal.style.zIndex = '1055';
            
            // Reemplazar iconos de Feather
            setTimeout(() => {
                feather.replace();
            }, 100);
        }
    }

    function closeOportunidadModal() {
        const modal = document.getElementById('nuevaOportunidadModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    function submitOportunidad() {
        const form = document.getElementById('nuevaOportunidadForm');
        
        if (!form || !form.checkValidity()) {
            if (form) form.reportValidity();
            return;
        }

        const cuentaElement = document.getElementById('cuenta');
        const casoUsoElement = document.getElementById('casoUso');
        const descripcionElement = document.getElementById('descripcion');
        const impactoElement = document.getElementById('impacto');

        if (!cuentaElement || !casoUsoElement || !descripcionElement || !impactoElement) {
            alert('Error: No se pudieron encontrar todos los campos del formulario');
            return;
        }

        const formData = {
            cuenta: cuentaElement.value,
            casoUso: casoUsoElement.value,
            descripcion: descripcionElement.value,
            impacto: impactoElement.value
        };

        // Enviar datos al servidor
        fetch('/api/oportunidades', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Oportunidad creada exitosamente');
                closeOportunidadModal();
                // Recargar página para mostrar la nueva oportunidad
                window.location.reload();
            } else {
                alert('Error al crear oportunidad: ' + (data.message || 'Error desconocido'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al conectar con el servidor');
        });
    }

    // Cerrar modal al hacer click en el fondo
    document.addEventListener('click', function(e) {
        const modal = document.getElementById('nuevaOportunidadModal');
        if (e.target === modal) {
            closeOportunidadModal();
        }
    });