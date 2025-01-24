<template>
  <div class="container mt-4">
    <hr class="line">
    <h1 class="text-center mb-4">Listado de Usuarios</h1>
    <hr class="line">
    <div v-if="loading" class="spinner-border text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div>
    <table v-else class="table table-hover table-bordered">
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
    <nav aria-label="Paginación" class="mt-3">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="fetchUsuarios(currentPage - 1)" :disabled="currentPage === 1">Anterior</button>
        </li>
        <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
          <button class="page-link" @click="fetchUsuarios(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="fetchUsuarios(currentPage + 1)" :disabled="currentPage === totalPages">Siguiente</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const usuarios = ref([]);
const selectedUsuario = ref(null);
const currentPage = ref(1);
const totalPages = ref(1);
const loading = ref(true);
const authStore = useAuthStore();

const fetchUsuarios = async (page = 1) => {
  loading.value = true;
  try {
    const token = authStore.getToken();
    const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios?page=${page}&per_page=10`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
    });

    if (response.status !== 200) {
      throw new Error("Error al obtener los usuarios");
    }

    const data = await response.json();
    usuarios.value = data.usuarios;
    currentPage.value = data.current_page;
    totalPages.value = data.pages;
  } catch (error) {
    console.error("Error al obtener los usuarios:", error);
  } finally {
    loading.value = false;
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

    if (response.status !== 200) {
      throw new Error("Error al eliminar el usuario");
    }

    await fetchUsuarios(currentPage.value);
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

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.page-item {
  list-style: none;
}

.page-link {
  display: inline-block;
  padding: 8px 12px;
  margin: 0 5px;
  border: 1px solid #007bff;
  border-radius: 4px;
  color: #007bff;
  background-color: white; 
  text-decoration: none;
  transition: all 0.3s ease;
}

.page-link:hover {
  background-color: #007bff;
  color: white;
}

.page-item.active .page-link {
  background-color: #0056b3;
  color: white;
  border-color: #0056b3;
}

.page-item.disabled .page-link {
  color: #ccc;
  cursor: not-allowed;
  background-color: #f8f9fa;
  border-color: #ddd;
}

.page-item.previous .page-link,
.page-item.next .page-link {
  padding: 8px 16px;
  font-weight: bold;
}
</style>