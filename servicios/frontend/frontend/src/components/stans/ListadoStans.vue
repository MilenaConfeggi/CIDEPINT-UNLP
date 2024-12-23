<template>
  <div class="container mt-4">
    <hr class="line">
    <h1 class="text-center mb-4">Listado de STAN</h1>
    <hr class="line">
    <table class="table table-hover table-bordered">
      <thead class="thead-dark">
        <tr>
          <th>Número</th>
          <th>Precio en Pesos</th>
          <th>Precio en Dólares</th>
          <th>Precio por</th>
          <th>Ensayos Asociados</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stan in stans" :key="stan.id" @click="highlightRow(stan.id)" :class="{ 'table-active': selectedStan === stan.id }">
          <td>{{ stan.numero }}</td>
          <td>${{ stan.precio_pesos }}</td>
          <td>${{ stan.precio_dolares }}</td>
          <td>{{ stan.precio_por_muestra ? 'muestra' : 'hora' }}</td>
          <td>
            <ul>
              <li v-for="ensayo in stan.ensayos" :key="ensayo.id">{{ ensayo.nombre }}</li>
            </ul>
          </td>
          <td>
            <button @click.stop="modificarStan(stan.id)" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Modificar</button>
          </td>
        </tr>
      </tbody>
    </table>
    <nav aria-label="Paginación" class="mt-3">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="fetchStans(currentPage - 1)" :disabled="currentPage === 1">Anterior</button>
        </li>
        <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
          <button class="page-link" @click="fetchStans(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="fetchStans(currentPage + 1)" :disabled="currentPage === totalPages">Siguiente</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';
import { useAuthStore } from '@/stores/auth';

const stans = ref([]);
const selectedStan = ref(null);
const currentPage = ref(1);
const totalPages = ref(1);
const emit = defineEmits(['modificar-stan']);
const authStore = useAuthStore();

const fetchStans = async (page = 1) => {
  try {
    const token = authStore.getToken();
    console.log('Token:', token);
    const response = await fetch(`${import.meta.env.VITE_API_URL}/stans?page=${page}&per_page=10`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
    });

    if (!response.ok) {
      throw new Error("Error al obtener los stans");
    }

    const data = await response.json();
    stans.value = data.stans;
    currentPage.value = data.current_page;
    totalPages.value = data.pages;
  } catch (error) {
    console.error("Error al obtener los stans:", error);
  }
};

const highlightRow = (id) => {
  selectedStan.value = id;
};

const modificarStan = (id) => {
  emit('modificar-stan', id);
};

onMounted(() => {
  fetchStans();
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
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
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