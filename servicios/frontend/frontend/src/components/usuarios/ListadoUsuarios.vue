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
          <th>Área</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="usuario in usuarios" :key="usuario.id" @click="highlightRow(usuario.id)" :class="{ 'table-active': selectedUsuario === usuario.id }">
          <td>{{ usuario.mail }}</td>
          <td>{{ usuario.rol }}</td>
          <td>
            {{ usuario.empleado && usuario.empleado.area && usuario.empleado.area.nombre ? usuario.empleado.area.nombre : 'Sin área' }}
          </td>
          <td>
            <button
              v-if="usuario.rol !== 'Director' && usuario.rol !== 'Secretaria'"
              @click.stop="abrirModalCambiarRol(usuario)"
              class="btn-cambiar-rol"
            >
              Cambiar Rol
            </button>
            <button
              @click.stop="confirmarEliminacion(usuario.id)"
              class="btn-eliminar"
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

    <!-- Modal Cambiar Rol -->
    <div v-if="mostrarModalCambiarRol" class="modal-overlay" @click="cerrarModalCambiarRol">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarModalCambiarRol">&times;</button>
        <h5 class="mb-3">Cambiar Rol de Usuario</h5>
        <div class="mb-3">
          <label for="nuevoRol" class="form-label">Nuevo Rol:</label>
          <select id="nuevoRol" v-model="nuevoRolSeleccionado" class="form-control">
            <option v-for="rol in rolesDisponibles" :key="rol" :value="rol">{{ rol }}</option>
          </select>
        </div>
        <button class="btn btn-success" @click="cambiarRolUsuario">Guardar</button>
      </div>
    </div>
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

const mostrarModalCambiarRol = ref(false);
const usuarioCambiarRol = ref(null);
const nuevoRolSeleccionado = ref(null);
const rolesDisponibles = ['Jefe de area', 'Trabajador'];

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

// Cambiar Rol
const abrirModalCambiarRol = (usuario) => {
  usuarioCambiarRol.value = usuario;
  // Por defecto, selecciona el otro rol
  nuevoRolSeleccionado.value = usuario.rol === 'Jefe de area' ? 'Trabajador' : 'Jefe de area';
  mostrarModalCambiarRol.value = true;
};

const cerrarModalCambiarRol = () => {
  mostrarModalCambiarRol.value = false;
  usuarioCambiarRol.value = null;
};

const cambiarRolUsuario = async () => {
  if (!usuarioCambiarRol.value || !nuevoRolSeleccionado.value) return;
  try {
    const token = authStore.getToken();
    const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/cambiar-rol`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        id: usuarioCambiarRol.value.id,
        nuevo_rol: nuevoRolSeleccionado.value
      })
    });

    if (response.status !== 200) {
      throw new Error("Error al cambiar el rol del usuario");
    }

    await fetchUsuarios(currentPage.value);
    cerrarModalCambiarRol();
  } catch (error) {
    console.error("Error al cambiar el rol del usuario:", error);
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

.btn-cambiar-rol {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-right: 8px;
  transition: background-color 0.3s ease;
}

.btn-cambiar-rol:hover {
  background-color: #0056b3;
}

.btn-eliminar {
  background-color: #dc3545;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.btn-eliminar:hover {
  background-color: #a71d2a;
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

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; 
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
  width: 100%;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
</style>