<template>
  <div class="container mt-4">
    <hr class="line" />
    <h1 class="text-center mb-4">Listado de STAN</h1>
    <hr class="line" />
    <div v-if="loading" class="spinner-border text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <table v-else class="table table-hover table-bordered">
      <thead class="thead-dark">
        <tr>
          <th class="col-numero">Número</th>
          <th class="col-ensayos">Ensayos Asociados</th>
          <th class="col-precio-por">Precio por</th>
          <th class="col-precio-pesos">Precio en Pesos</th>
          <th class="col-precio-dolares">Precio en Dólares</th>
          <th class="col-acciones">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(stan, index) in stans"
          :key="stan.id"
          @click="highlightRow(stan.id)"
          :class="{ 'table-active': selectedStan === stan.id }"
          :style="{ animationDelay: `${index * 0.1}s` }"
          class="fade-in"
        >
          <td class="col-numero">{{ stan.numero }}</td>
          <td class="col-ensayos">
            <ul>
              <li v-for="ensayo in stan.ensayos" :key="ensayo.id">{{ ensayo.nombre }}</li>
            </ul>
          </td>
          <td class="col-precio-por">{{ stan.precio_por_muestra ? 'muestra' : 'hora' }}</td>
          <td class="col-precio-pesos">${{ stan.precio_pesos }}</td>
          <td class="col-precio-dolares">${{ stan.precio_dolares }}</td>
          <td class="col-acciones">
            <button @click.stop="modificarStan(stan.id)" class="btn-modificar">
              <i class="fas fa-pencil-alt"></i>
            </button>
            <button @click.stop="eliminarStan(stan.id)" class="btn-eliminar">
              <i class="fas fa-trash-alt"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <nav aria-label="Paginación" class="mt-3">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button
            class="page-link"
            @click="fetchStans(currentPage - 1)"
            :disabled="currentPage === 1"
          >
            Anterior
          </button>
        </li>
        <li
          v-for="page in totalPages"
          :key="page"
          class="page-item"
          :class="{ active: currentPage === page }"
        >
          <button class="page-link" @click="fetchStans(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button
            class="page-link"
            @click="fetchStans(currentPage + 1)"
            :disabled="currentPage === totalPages"
          >
            Siguiente
          </button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const stans = ref([])
const selectedStan = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const loading = ref(true)
const successMessage = ref(null)
const errorMessage = ref(null)
const emit = defineEmits(['modificar-stan'])
const authStore = useAuthStore()

const fetchStans = async (page = 1) => {
  loading.value = true
  try {
    const token = authStore.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL}/stans?page=${page}&per_page=10`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (response.status !== 200) {
      throw { status: response.status, message: `Error: ${response.status}` }; 
    }

    const data = await response.json()
    stans.value = data.stans
    currentPage.value = data.current_page
    totalPages.value = data.pages
  } catch (error) {
    if (error.status === 401 || error.status === 422) {
      authStore.logout()
      router.push('/log-in')
    }
    console.error('Error al obtener los stans:', error.message || error)
  } finally {
    loading.value = false
  }
}

const highlightRow = (id) => {
  selectedStan.value = id
}

const modificarStan = (id) => {
  emit('modificar-stan', id)
}

const eliminarStan = async (id) => {
  if (!confirm('¿Estás seguro de que deseas eliminar este STAN?')) {
    return
  }

  try {
    const token = authStore.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL}/stans/eliminar_stan/${id}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (response.status !== 200) {
      throw new Error('Error al eliminar el STAN')
    }

    successMessage.value = 'STAN eliminado exitosamente'
    setTimeout(() => {
      window.location.reload()
    }, 1500)
  } catch (error) {
    console.error('Error al eliminar el STAN:', error)
    errorMessage.value = 'Error al eliminar el STAN'
  }
}

onMounted(() => {
  fetchStans()
})
</script>

<style scoped>
.table {
  width: 100%;
  margin: auto;
  border-collapse: collapse;
  background-color: #f9f9f9; /* Fondo claro para la tabla */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Sombra para la tabla */
}

.table th,
.table td {
  text-align: center;
  vertical-align: middle;
  padding: 10px;
  border: 1px solid #ddd; /* Bordes ligeros para las celdas */
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
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition:
    background-color 0.3s ease,
    box-shadow 0.3s ease; /* Transición para el fondo y la sombra */
}

button:hover {
  background-color: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra al pasar el ratón */
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

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  margin-left: 10px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
}

.btn-modificar {
  background-color: #ffc107; /* Color amarillo */
  color: #000; /* Color negro */
  transition:
    background-color 0.3s ease,
    box-shadow 0.3s ease; /* Transición para el fondo y la sombra */
}

.btn-modificar:hover {
  background-color: #e0a800; /* Color amarillo oscuro */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra al pasar el ratón */
}

.btn-eliminar {
  background-color: #dc3545; /* Color rojo */
  color: #fff; /* Color blanco */
  transition:
    background-color 0.3s ease,
    box-shadow 0.3s ease; /* Transición para el fondo y la sombra */
}

.btn-eliminar:hover {
  background-color: #a71d2a; /* Color rojo oscuro */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra al pasar el ratón */
}

.btn-modificar,
.btn-eliminar {
  font-size: 0.8rem; /* Tamaño de fuente más pequeño */
  padding: 5px 10px; /* Menor padding */
  width: 30px; /* Ancho más pequeño */
  height: 30px; /* Alto más pequeño */
  border-radius: 50%; /* Botones redondos */
}

/* Definir anchos fijos para las columnas */
.col-numero {
  width: 10%;
}

.col-ensayos {
  width: 50%;
}

.col-precio-por {
  width: 10%;
}

.col-precio-pesos {
  width: 10%;
}

.col-precio-dolares {
  width: 10%;
}

.col-acciones {
  width: 10%;
}

.fade-in {
  opacity: 0;
  animation: fadeIn 0.5s forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}
</style>