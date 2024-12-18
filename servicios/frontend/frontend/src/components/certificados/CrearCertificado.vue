<template>
    <div class="container mt-4">
      <hr class="line">
      <h1 class="text-center mb-4">Generar Certificado</h1>
      <hr class="line">
      <form @submit.prevent="submitForm" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 form-container">
        <div v-for="(empleado, index) in empleados" :key="index" class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">{{ empleado.nombre }}</label>
          <div class="mb-2">
            <label class="block text-gray-700 text-sm font-bold mb-2">Función:</label>
            <select v-model="empleado.funcion" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
              <option value="Responsable del equipo">Responsable del equipo</option>
              <option value="Integrante del equipo">Integrante del equipo</option>
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-700 text-sm font-bold mb-2">Porcentaje de Participación:</label>
            <input type="number" v-model="empleado.participacion" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" required>
          </div>
        </div>
        <div v-if="error" class="alert alert-danger mb-4" role="alert">
          {{ error }}
        </div>
        <div v-if="successMessage" class="alert alert-success mb-4" role="alert">
          {{ successMessage }}
        </div>
        <div class="flex items-center justify-between">
          <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Generar Certificado</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const idLegajo = route.params.id_legajo;

const empleados = ref([]);
const error = ref(null);
const successMessage = ref(null);

const fetchEmpleados = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/certificado/obtener_empleados/${idLegajo}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    if (!response.ok) {
      throw new Error('Error al obtener los empleados');
    }
    empleados.value = await response.json();
    empleados.value = empleados.value.map(empleado => ({
      nombre: empleado,
      funcion: 'Integrante del equipo',
      participacion: 0,
    }));
  } catch (err) {
    error.value = err.message;
  }
};

const submitForm = async () => {
  error.value = null;
  successMessage.value = null;

  const data = {
    empleados: empleados.value,
  };

  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/certificado/crear/${idLegajo}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || 'Error al generar el certificado');
    }

    successMessage.value = result.message;
  } catch (err) {
    error.value = err.message;
  }
};

onMounted(() => {
  fetchEmpleados();
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
    max-height: 600px; 
    overflow-y: auto;
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