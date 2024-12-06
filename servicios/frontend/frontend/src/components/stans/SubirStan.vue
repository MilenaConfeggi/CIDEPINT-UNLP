<template>
    <div class="container mt-4">
      <hr class="line">
      <h1 class="text-center mb-4">Subir STAN</h1>
      <hr class="line">
      <form @submit.prevent="submitForm" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 form-container">
        <div class="mb-4">
          <label for="numero" class="block text-gray-700 text-sm font-bold mb-2">Número:</label>
          <input type="text" id="numero" v-model="stan.numero" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" required>
        </div>
        <div class="mb-4">
          <label for="precio_pesos" class="block text-gray-700 text-sm font-bold mb-2">Precio en Pesos:</label>
          <input type="number" id="precio_pesos" v-model="stan.precio_pesos" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
        </div>
        <div class="mb-4">
          <label for="precio_dolares" class="block text-gray-700 text-sm font-bold mb-2">Precio en Dólares:</label>
          <input type="number" id="precio_dolares" v-model="stan.precio_dolares" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
        </div>
        <div class="mb-4">
          <label for="precio_por" class="block text-gray-700 text-sm font-bold mb-2">Precio por:</label>
          <select id="precio_por" v-model="stan.precio_por_muestra" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
            <option :value="true">Muestra</option>
            <option :value="false">Hora</option>
          </select>
        </div>
        <div class="mb-4">
          <label for="ensayos" class="block text-gray-700 text-sm font-bold mb-2">Ensayos Asociados:</label>
          <input type="text" id="ensayos" v-model="ensayos" placeholder="Ingrese nombres de ensayo separados por comas" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ensayos-input">
        </div>
        <div class="mb-4">
          <input type="checkbox" id="mostrar_ensayos" v-model="mostrarEnsayos" class="mr-2">
          <label for="mostrar_ensayos">Mostrar Ensayos Existentes</label>
          <div v-if="mostrarEnsayos" class="ensayos-list">
            <label for="mostrar_ensayos" class="block text-gray-700 text-sm font-bold mb-2">Seleccionar Ensayos Existentes:</label>
            <div v-for="ensayo in ensayosExistentes" :key="ensayo.id" class="ensayo-item">
              <input type="checkbox" :id="`ensayo-${ensayo.id}`" :value="ensayo.nombre" v-model="selectedEnsayos" class="mr-2">
              <label :for="`ensayo-${ensayo.id}`">{{ ensayo.nombre }}</label>
            </div>
          </div>
        </div>
        <div v-if="error" class="alert alert-danger mb-4" role="alert">
          {{ error }}
        </div>
        <div v-if="successMessage" class="alert alert-success mb-4" role="alert">
          {{ successMessage }}
        </div>
        <div class="flex items-center justify-between">
          <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Subir Stan</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const stan = ref({
    numero: '',
    precio_pesos: null,
    precio_dolares: null,
    precio_por_muestra: true,
  });
  
  const ensayos = ref('');
  const ensayosExistentes = ref([]);
  const selectedEnsayos = ref([]);
  const mostrarEnsayos = ref(false);
  const error = ref(null);
  const successMessage = ref(null);
  
  const fetchEnsayos = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/stans/ensayos`);
      if (!response.ok) {
        throw new Error('Error al obtener los ensayos');
      }
      ensayosExistentes.value = await response.json();
    } catch (error) {
      console.error('Error al obtener los ensayos:', error);
    }
  };
  
  const submitForm = async () => {
    error.value = null;
    successMessage.value = null;
  
    const ensayosArray = ensayos.value.split(',').map(ensayo => ensayo.trim()).filter(ensayo => ensayo);
    const data = {
      ...stan.value,
      ensayos: [...ensayosArray, ...selectedEnsayos.value],
    };
  
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/stans/subir_stan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      const result = await response.json();
  
      if (!response.ok) {
        throw new Error(result.message || 'Error al subir el stan');
      }
  
      successMessage.value = result.message;
    } catch (err) {
      error.value = err.message;
    }
  };
  
  onMounted(() => {
    fetchEnsayos();
  });
  </script>
  
  <style scoped>
  .line {
    border: 0;
    height: 1px;
    background: #333;
    background-image: linear-gradient(to right, #ccc, #333, #ccc);
  }
  
  .form-container {
    max-height: 400px; 
    overflow-y: auto;
  }
  
  .ensayos-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    background-color: #f9f9f9;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  
  .ensayo-item {
    display: flex;
    align-items: center;
    background-color: #fff;
    padding: 5px 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .ensayos-input {
    height: 50px; 
    padding: 10px; 
    width: 100%; 
    box-sizing: border-box; 
  }
  
  button {
    background-color: #28a745; 
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #218838; 
  }
  
  .alert {
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 20px;
  }
  
  .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }
  
  .alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }
  </style>