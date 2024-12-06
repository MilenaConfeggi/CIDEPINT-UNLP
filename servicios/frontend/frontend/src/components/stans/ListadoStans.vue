<template>
    <div class="container mt-4">
      <hr class="line">
      <h1 class="text-center mb-4">Listado de Stans</h1>
      <hr class="line">
      <table class="table table-hover table-bordered">
        <thead class="thead-dark">
          <tr>
            <th>Número</th>
            <th>Precio en Pesos</th>
            <th>Precio en Dólares</th>
            <th>Precio por</th>
            <th>Ensayos Asociados</th>
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
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const stans = ref([]);
  const selectedStan = ref(null);
  
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
  

  </style>