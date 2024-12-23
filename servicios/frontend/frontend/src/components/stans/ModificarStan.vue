<template>
  <div class="container mt-4">
    <hr class="line">
    <h1 class="text-center mb-4">Modificar STAN</h1>
    <hr class="line">
    <form @submit.prevent="submitForm" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 form-container">
      <div v-if="error" class="alert alert-danger mb-4" role="alert">
        {{ error }}
      </div>
      <div v-if="successMessage" class="alert alert-success mb-4" role="alert">
        {{ successMessage }}
      </div>
      <div class="mb-4">
        <label for="numero" class="block text-gray-700 text-sm font-bold mb-2">Número:</label>
        <input type="text" id="numero" v-model="stan.numero" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" disabled>
      </div>
      <div class="mb-4">
        <label for="precio_pesos" class="block text-gray-700 text-sm font-bold mb-2">Precio en Pesos:</label>
        <input type="number" id="precio_pesos" v-model="stan.precio_pesos" min="0" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
      </div>
      <div class="mb-4">
        <label for="precio_dolares" class="block text-gray-700 text-sm font-bold mb-2">Precio en Dólares:</label>
        <input type="number" id="precio_dolares" v-model="stan.precio_dolares" min="0" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
      </div>
      <div class="flex items-center justify-between">
        <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Modificar Stan</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  id: {
    type: Number,
    required: true
  }
});

const stan = ref({
  numero: '',
  precio_pesos: null,
  precio_dolares: null,
  precio_por_muestra: true,
});

const error = ref(null);
const successMessage = ref(null);

const fetchStan = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/stans/modificar_stan/${props.id}`);
    if (!response.ok) {
      throw new Error('Error al obtener el stan');
    }
    const data = await response.json();
    stan.value = data;
  } catch (err) {
    error.value = err.message;
  }
};

const submitForm = async () => {
  error.value = null;
  successMessage.value = null;

  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/stans/editar_stan/${props.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(stan.value),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || 'Error al modificar el stan');
    }

    successMessage.value = result.message;
  } catch (err) {
    error.value = err.message;
  }
};

onMounted(() => {
  fetchStan();
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