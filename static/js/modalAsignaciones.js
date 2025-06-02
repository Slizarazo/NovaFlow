document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM cargado, inicializando eventos...');
    
    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Inicializar filtros dinámicos
    initializeAssignmentFilters();
    
    // Configurar eventos del modal - buscar todos los posibles botones
    setTimeout(function() {
        // Buscar por múltiples selectores
        const addAssignmentBtn = document.querySelector('[data-bs-target="#addAssignmentModal"]') || 
                                document.querySelector('button[title="Nueva Asignación"]') ||
                                document.querySelector('.action-button[title="Nueva Asignación"]');
        
        console.log('Botón encontrado:', addAssignmentBtn);
        
        if (addAssignmentBtn) {
            // Remover listeners existentes
            const newBtn = addAssignmentBtn.cloneNode(true);
            addAssignmentBtn.parentNode.replaceChild(newBtn, addAssignmentBtn);
            
            newBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Click en botón nueva asignación');
                showModal('addAssignmentModal');
            });
            console.log('Event listener añadido al botón');
        } else {
            console.error('Botón de nueva asignación no encontrado');
            // Buscar todos los botones disponibles para debug
            const allButtons = document.querySelectorAll('button');
            console.log('Botones disponibles:', allButtons);
        }
        
        // Configurar eventos para los elementos del dropdown
        const dropdownItems = document.querySelectorAll('.dropdown-item');
        dropdownItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const target = this.getAttribute('data-bs-target');
                if (target) {
                    showModal(target.replace('#', ''));
                }
            });
        });
    }, 200);
    
    // Configurar botones de cerrar
    document.addEventListener('click', function(e) {
        if (e.target.hasAttribute('data-bs-dismiss') && e.target.getAttribute('data-bs-dismiss') === 'modal') {
            e.preventDefault();
            const modal = e.target.closest('.modal');
            if (modal) {
                hideModal(modal.id);
            }
        }
    });
    
    // Cerrar modales al hacer click en el backdrop
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            hideModal(e.target.id);
        }
    });
});

function showModal(modalId) {
    console.log('Mostrando modal:', modalId);
    const modal = document.getElementById(modalId);
    
    if (!modal) {
        console.error('Modal no encontrado:', modalId);
        return;
    }
    
    // Resetear modal al estado inicial
    resetModal();
    
    // Mostrar modal con estilo específico
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.zIndex = '1055';
    modal.classList.add('show');
    modal.setAttribute('aria-hidden', 'false');
    
    // Ocultar scroll de la página pero mantener el ancho
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = scrollbarWidth + 'px';
    
    // Añadir backdrop
    let backdrop = document.querySelector('.modal-backdrop');
    if (!backdrop) {
        backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop fade show';
        backdrop.style.position = 'fixed';
        backdrop.style.top = '0';
        backdrop.style.left = '0';
        backdrop.style.width = '100%';
        backdrop.style.height = '100%';
        backdrop.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        backdrop.style.zIndex = '1050';
        document.body.appendChild(backdrop);
    }
    
    // Reinicializar iconos de Feather
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    console.log('Modal mostrado correctamente:', modalId);
}

function hideModal(modalId) {
    console.log('Ocultando modal:', modalId);
    const modal = document.getElementById(modalId);
    
    if (!modal) {
        console.error('Modal no encontrado:', modalId);
        return;
    }
    
    // Ocultar modal
    modal.style.display = 'none';
    modal.style.position = '';
    modal.style.top = '';
    modal.style.left = '';
    modal.style.width = '';
    modal.style.height = '';
    modal.style.alignItems = '';
    modal.style.justifyContent = '';
    modal.style.zIndex = '';
    modal.classList.remove('show');
    modal.setAttribute('aria-hidden', 'true');
    
    // Restaurar scroll de la página
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    
    // Remover backdrop
    const backdrop = document.querySelector('.modal-backdrop');
    if (backdrop) {
        backdrop.remove();
    }
    
    // Resetear modal
    resetModal();
    
    console.log('Modal ocultado correctamente:', modalId);
}

function resetModal() {
    document.getElementById('assignmentTypeSelection').style.display = 'block';
    document.getElementById('comunidadForm').style.display = 'none';
    document.getElementById('freelanceForm').style.display = 'none';
    document.getElementById('crearComunidadForm').style.display = 'none';
    document.getElementById('submitAssignmentBtn').style.display = 'none';
    
    // Limpiar formularios
    const freelanceForm = document.getElementById('assignmentForm');
    const comunidadForm = document.getElementById('comunidadAssignmentForm');
    if (freelanceForm) {
        freelanceForm.reset();
    }
    if (comunidadForm) {
        comunidadForm.reset();
    }
}

let contadorMiembros = 0;

function agregarMiembroComunidad() {
    const container = document.getElementById('miembrosComunidadContainer');
    const plantilla = document.getElementById('miembroPlantilla');

    if (!plantilla) {
        console.error('No se encontró la plantilla de miembro.');
        return;
    }

    const nuevoMiembro = plantilla.cloneNode(true);
    nuevoMiembro.style.display = 'flex';
    nuevoMiembro.removeAttribute('id');

    // Limpia valores por si acaso
    const selects = nuevoMiembro.querySelectorAll('select');
    selects.forEach(sel => sel.selectedIndex = 0);

    const inputs = nuevoMiembro.querySelectorAll('input');
    inputs.forEach(inp => inp.value = '');

    container.appendChild(nuevoMiembro);
}

function selectAssignmentType(type) {
    document.getElementById('assignmentTypeSelection').style.display = 'none';
    
    if (type === 'comunidad') {
        document.getElementById('comunidadForm').style.display = 'block';
        document.getElementById('submitAssignmentBtn').style.display = 'inline-block';
        document.getElementById('submitAssignmentBtn').textContent = 'Crear Asignación de Comunidad';
    } else if (type === 'freelance') {
        document.getElementById('freelanceForm').style.display = 'block';
        document.getElementById('submitAssignmentBtn').style.display = 'inline-block';
        document.getElementById('submitAssignmentBtn').textContent = 'Crear Asignación de Freelance';
    } else if (type === 'crear_comunidad') {
        document.getElementById('crearComunidadForm').style.display = 'block';
        document.getElementById('submitAssignmentBtn').style.display = 'inline-block';
        document.getElementById('submitAssignmentBtn').textContent = 'Crear Comunidad';
    }
    
    // Reinicializar iconos de Feather
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function backToTypeSelection() {
    document.getElementById('assignmentTypeSelection').style.display = 'block';
    document.getElementById('comunidadForm').style.display = 'none';
    document.getElementById('freelanceForm').style.display = 'none';
    document.getElementById('crearComunidadForm').style.display = 'none';
    document.getElementById('submitAssignmentBtn').style.display = 'none';
    
    // Reinicializar iconos de Feather
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function showDataManagementModal() {
    console.log('Mostrando modal de gestión de datos');
    showModal('dataManagementModal');
}

function openImportModal() {
    hideModal('dataManagementModal');
    setTimeout(() => {
        showModal('importAssignmentModal');
    }, 100);
}

function openExportModal() {
    hideModal('dataManagementModal');
    setTimeout(() => {
        showModal('exportAssignmentModal');
    }, 100);
}

function submitAssignment() {
    const freelanceForm = document.getElementById('freelanceForm');
    const comunidadForm = document.getElementById('comunidadForm');
    const crearComunidadDiv = document.getElementById('crearComunidadForm');
    const crearComunidadForm = document.getElementById('crearComunidadFormContent'); // Este es el <form>

    let formData = {};
    let tipoAsignacion = '';

    if (freelanceForm && freelanceForm.style.display !== 'none') {
        const form = document.getElementById('assignmentForm');
        if (!form || !form.checkValidity()) {
            if (form) form.reportValidity();
            return;
        }

        const casoUso = document.getElementById('casoUsoSelect');
        const usuario = document.getElementById('usuarioSelect');
        const rol = document.getElementById('rolProyecto');

        formData = {
            tipo: 'freelance',
            id_sede: casoUso.value,
            id_usuario: usuario.value,
            rol_en_cliente: rol.value
        };
        tipoAsignacion = 'freelance';

    } else if (comunidadForm && comunidadForm.style.display !== 'none') {
        const form = document.getElementById('comunidadAssignmentForm');
        if (!form || !form.checkValidity()) {
            if (form) form.reportValidity();
            return;
        }

        const casoUso = document.getElementById('casoUsoComunidadSelect');
        const comunidad = document.getElementById('comunidadSelect');

        formData = {
            tipo: 'comunidad',
            id_sede: casoUso.value,
            id_comunidad: comunidad.value
        };
        tipoAsignacion = 'comunidad';

    } else if (crearComunidadDiv && crearComunidadDiv.style.display !== 'none') {
        const form = document.getElementById('crearComunidadFormContent'); // <form>
        if (!form || !(form instanceof HTMLFormElement)) {
            alert('No se encontró el formulario de creación de comunidad');
            return;
        }
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const nombre = document.getElementById('nombreComunidad').value;
        const tipo = document.getElementById('tipoComunidad').value;
        const descripcion = document.getElementById('descripcionComunidad').value;

        // Captura los usuarios y roles
        const usuarios = Array.from(document.querySelectorAll('select[name="usuario[]"]')).map(s => s.value);
        const roles = Array.from(document.querySelectorAll('input[name="rol[]"]')).map(i => i.value);

        formData = {
            tipo: 'crear_comunidad',
            nombre: nombre,
            tipo_comunidad: tipo,
            descripcion: descripcion,
            miembros: usuarios.map((u, i) => ({
                usuario: u,
                rol: roles[i]
            }))
        };
        tipoAsignacion = 'crear_comunidad';
    } else {
        alert('Error: No se pudo determinar el tipo de formulario activo');
        return;
    }

    console.log('Enviando datos:', formData);

    fetch('/api/asignaciones', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            alert(`✅ ${tipoAsignacion} creado correctamente`);
            hideModal('addAssignmentModal');
            location.reload();
        } else {
            alert('⚠️ Error: ' + (data.message || 'Ocurrió un problema'));
        }
    })
    .catch(err => {
        console.error('❌ Error en el envío:', err);
        alert('Error de conexión con el servidor');
    });
}

// Sistema de filtros dinámicos para asignaciones
function initializeAssignmentFilters() {
    console.log('🔧 Inicializando filtros de asignaciones...');
    
    try {
        // Poblar filtros desde datos de la tabla
        populateAssignmentFiltersFromTable();
        
        // Configurar event listeners para filtros automáticos
        setupAssignmentFilterListeners();
        
        console.log('✅ Sistema de filtros de asignaciones inicializado correctamente');
    } catch (error) {
        console.error('❌ Error al inicializar filtros de asignaciones:', error);
    }
}

function populateAssignmentFiltersFromTable() {
    console.log('📊 Poblando filtros desde datos de la tabla de asignaciones...');
    
    const table = document.querySelector('.table tbody');
    if (!table) {
        console.error('❌ Tabla de consultores no encontrada');
        return;
    }
    
    const rows = table.querySelectorAll('tr');
    const especialidades = new Set();
    const ciudades = new Set();
    
    rows.forEach(row => {
        try {
            const especialidad = row.getAttribute('data-especialidad');
            const ciudad = row.getAttribute('data-ciudad');
            
            if (especialidad && especialidad.trim()) especialidades.add(especialidad.trim());
            if (ciudad && ciudad.trim()) ciudades.add(ciudad.trim());
        } catch (error) {
            console.warn('⚠️ Error procesando fila:', error);
        }
    });
    
    // Poblar selectores
    populateAssignmentSelect('filterEspecialidad', especialidades);
    populateAssignmentSelect('filterCiudad', ciudades);
    
    console.log('✅ Filtros poblados:', {
        especialidades: especialidades.size,
        ciudades: ciudades.size
    });
}

function populateAssignmentSelect(selectId, options) {
    const select = document.getElementById(selectId);
    if (!select) {
        console.error('❌ Selector no encontrado:', selectId);
        return;
    }
    
    // Limpiar opciones existentes excepto la primera
    const firstOption = select.querySelector('option[value=""]');
    select.innerHTML = '';
    if (firstOption) {
        select.appendChild(firstOption);
    }
    
    // Agregar nuevas opciones ordenadas
    Array.from(options).sort().forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
    });
}

function setupAssignmentFilterListeners() {
    const filterIds = ['filterEspecialidad', 'filterDisponibilidad', 'filterCiudad'];
    
    filterIds.forEach(filterId => {
        const filter = document.getElementById(filterId);
        if (filter) {
            filter.addEventListener('change', applyAssignmentFilters);
            console.log('✅ Event listener agregado a', filterId);
        } else {
            console.error('❌ Filtro no encontrado:', filterId);
        }
    });
}

function applyAssignmentFilters() {
    console.log('🎯 Aplicando filtros de asignaciones...');
    
    try {
        // Obtener valores de filtros
        const especialidadValue = document.getElementById('filterEspecialidad').value.toLowerCase();
        const disponibilidadValue = parseInt(document.getElementById('filterDisponibilidad').value) || 0;
        const ciudadValue = document.getElementById('filterCiudad').value.toLowerCase();
        
        console.log('📊 Filtros aplicados:', {
            especialidad: especialidadValue,
            disponibilidad: disponibilidadValue,
            ciudad: ciudadValue
        });
        
        // Obtener filas de la tabla
        const table = document.querySelector('.table tbody');
        if (!table) {
            console.error('❌ Tabla no encontrada');
            return;
        }
        
        const rows = table.querySelectorAll('tr');
        let visibleCount = 0;
        
        rows.forEach(row => {
            try {
                // Extraer datos de la fila
                const especialidad = row.getAttribute('data-especialidad').toLowerCase();
                const disponibilidad = parseInt(row.getAttribute('data-disponibilidad'));
                const ciudad = row.getAttribute('data-ciudad').toLowerCase();
                
                // Aplicar filtros
                const matchEspecialidad = especialidadValue === '' || especialidad.includes(especialidadValue);
                const matchDisponibilidad = disponibilidadValue === 0 || disponibilidad >= disponibilidadValue;
                const matchCiudad = ciudadValue === '' || ciudad.includes(ciudadValue);
                
                // Mostrar/ocultar fila
                if (matchEspecialidad && matchDisponibilidad && matchCiudad) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            } catch (error) {
                console.warn('⚠️ Error procesando fila:', error);
                // En caso de error, mostrar la fila
                row.style.display = '';
                visibleCount++;
            }
        });
        
        console.log(`✅ Filtrado completado: ${visibleCount}/${rows.length} consultores visibles`);
        
    } catch (error) {
        console.error('❌ Error al aplicar filtros:', error);
    }
}