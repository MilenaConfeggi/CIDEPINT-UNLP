<template>
    <div class="container mt-4">
      <hr class="line">
      <h1 class="text-center mb-4">Listado de Usuarios</h1>
      <hr class="line">
      <table class="table table-hover table-bordered">
        <thead class="thead-dark">
          <tr>
            <th>Mail</th>
            <th>Rol</th>
            <th>Eliminar</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="usuario in usuarios" :key="usuario.id" @click="highlightRow(usuario.id)" :class="{ 'table-active': selectedUsuario === usuario.id }">
            <td>{{ usuario.mail }}</td>
            <td>{{ usuario.rol }}</td>
            <td>
            <button
              @click.stop="confirmarEliminacion(usuario.id)"
              class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Eliminar
            </button>
          </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, defineEmits } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  
  const usuarios = ref([]);
  const selectedUsuario = ref(null);
  //const emit = defineEmits(['modificar-stan']);
  const authStore = useAuthStore();
  
  const fetchUsuarios = async () => {
    try {
      const token = authStore.getToken();
      const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
      });
  
      if (!response.ok) {
        throw new Error("Error al obtener los usuarios");
      }
  
      usuarios.value = await response.json();
      console.log(usuarios.value);
      
      
    } catch (error) {
      console.error("Error al obtener los usuarios:", error);
    }
  };
  const highlightRow = (id) => {
    selectedUsuario.value = id;
  };

  const confirmarEliminacion = (id) => {
    if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
      eliminarUsuario(id);
    }
  };
  
  const eliminarUsuario = async (id) => {
    try {
      const token = authStore.getToken();
      const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/borrar`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ "id": id })
      });
  
      if (!response.ok) {
        throw new Error("Error al eliminar el usuario");
      }
  
      usuarios.value = await response.json();
    } catch (error) {
      console.error("Error al eliminar el usuario:", error);
    }
  };
  
  onMounted(() => {
    fetchUsuarios();
  });
  </script>
  
  <style scoped>
  .table {
    width: 100%;
    margin: auto;
    border-collapse: collapse;
  }
  
  .table th, .table td {
    text-align: center;
    vertical-align: middle;
    padding: 10px;
  }
  
  .table-hover tbody tr:hover {
    background-color: #f1f1f1;
    cursor: pointer;
  }
  
  .table-active {
    background-color: #d1ecf1;
  }
  
  .thead-dark th {
    background-color: #343a40;
    color: white;
  }
  
  .line {
    border: 0;
    height: 1px;
    background: #333;
    background-image: linear-gradient(to right, #ccc, #333, #ccc);
  }
  
  button {
    background-color: #dF2b00;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #A01b00;
  }
  </style>