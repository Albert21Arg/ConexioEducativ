const listaUsuarios2 = async () => {
    try {
        const response = await fetch('/usuariosListar2/');
        const data = await response.json();

        const tbody = document.querySelector('.bodyListaUsuarios'); // Asegúrate de declarar esto aquí
        tbody.innerHTML = ''; // Limpiar contenido previo si lo hay

        data.usuarios.forEach((usuario, index) => {
            const row = `
                <tr>
                <td>${index + 1}</td>
                    <td>${usuario.nombre} ${usuario.apellido}</td>                    
                    <td>${usuario.correo}</td>
                    <td>
                        <a href="#" class="btn btn-sm btn-info">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
                        <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                        <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                        </svg>                        
                        </a>
                    </td>
                </tr>`;
            tbody.innerHTML += row;
        });

        
        if (!$.fn.DataTable.isDataTable('#datatableEstudiantes')) {
            new DataTable('#datatableEstudiantes', {
                pageLength: 5,
                lengthMenu: [
                    [5, 10, 25, -1],
                    [5, 10, 25, "Todos"]
                ],
                language: {
                    url: "https://cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json",
                    lengthMenu: "Mostrar _MENU_  ",
                    zeroRecords: "No se encontraron resultados",
                    info: "Estudiantes del _START_ a _END_ de _TOTAL_ ",
                    infoEmpty: "Mostrando 0 a 0 de 0 Usuarios",
                    infoFiltered: "(filtrado de _MAX_ Estudiantes totales)",
                    search: "Buscar:",
                    paginate: {
                        first: "<<",
                        last: ">>",
                        next: ">",
                        previous: "<"
                    }
                }
            });
        }

    } catch (ex) {
        alert('Error al obtener usuarios: ' + ex);
    }
};

window.addEventListener("load", listaUsuarios2);