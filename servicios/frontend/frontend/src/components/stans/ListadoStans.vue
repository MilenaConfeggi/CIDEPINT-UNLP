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
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';

const stans = ref([]);
const selectedStan = ref(null);
const emit = defineEmits(['modificar-stan']);

const fetchStans = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/stans`);
    if (!response.ok) {
      throw new Error('Error al obtener los stans');
    }
    stans.value = await response.json();
  } catch (error) {
    console.error('Error al obtener los stans:', error);
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
</style>