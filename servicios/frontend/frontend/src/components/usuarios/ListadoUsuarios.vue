<template>
    <div>
      <h1>Listado de Usuarios</h1>
      <ul v-if="usuarios.length > 0">
        <li v-for="usuario in usuarios" :key="usuario.id">
          {{ usuario.rol }} - {{ usuario.mail }}
        </li>
      </ul>
      <p v-else>Cargando usuarios...</p>
    </div>
  </template>
  
  <script>
  
  export default {
    data() {
      return {
        usuarios: [],
      };
    },
    async created() {
      try {
        const getUsuarios = async () => {
            const token = localStorage.getItem('jwt'); // Obtén el token del localStorage

            if (!token) {
                throw new Error('No estás autenticado');
            }

            try {
                const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Error al obtener usuarios');
                }

                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Error:', error.message);
                throw error;
            }
        };
        this.usuarios = await getUsuarios();
      } catch (error) {
        console.error('Error al cargar usuarios:', error.message);
        alert('No se pudo cargar el listado de usuarios.');
      }
    },
  };
  </script>