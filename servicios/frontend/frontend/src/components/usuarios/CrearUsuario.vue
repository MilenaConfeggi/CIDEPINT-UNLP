<template>
    <div class="container mt-4">
      <hr class="line">
      <h1 class="text-center mb-4">Crear Usuario</h1>
      <hr class="line">
      <form @submit.prevent="submitForm" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 form-container">
        <div class="mb-4">
          <label for="mail" class="block text-gray-700 text-sm font-bold mb-2">Mail:</label>
          <input type="email" id="mail" v-model="usuario.mail" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" required>
        </div>
        <div class="mb-4">
          <label for="mail" class="block text-gray-700 text-sm font-bold mb-2">Contraseña:</label>
          <input type="password" id="contra" v-model="usuario.contra" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" required>
        </div>
        <div class="mb-4">
            <label for="rol" class="block text-gray-700 text-sm font-bold mb-2">Rol:</label>
            <select
                id="rol"
                v-model="usuario.rol"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                required
            >
                <option v-for="rol in rolesExistentes" :key="rol.id" :value="rol.id">
                {{ rol.nombre }}
                </option>
            </select>
            </div>
        <div v-if="error" class="alert alert-danger mb-4" role="alert">
          {{ error }}
        </div>
        <div v-if="successMessage" class="alert alert-success mb-4" role="alert">
          {{ successMessage }}
        </div>
        <div class="flex items-center justify-between">
          <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Crear Usuario</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  const authStore = useAuthStore();
  
  const usuario = ref({
    mail: '',
    contra: null,
    rol: null,
  });
  
  const rolesExistentes = ref([]);
  const error = ref(null);
  const successMessage = ref(null);
  
  const fetchRoles = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/roles`);
      if (!response.ok) {
        throw new Error('Error al obtener los roles');
      }
      rolesExistentes.value = await response.json();
    } catch (error) {
      console.error('Error al obtener los roles:', error);
    }
  };
  
  const submitForm = async () => {
    error.value = null;
    successMessage.value = null;
  
    const data = {
      ...usuario.value
    };
  
    try {
      const token = authStore.getToken();
      const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/crear`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });
  
      const result = await response.json();
  
      if (!response.ok) {
        throw new Error(result.message || 'Error al crear el usuario');
      }
  
      successMessage.value = result.message;
      setTimeout(() => {
        router.push({ name: 'usuarios' });
      }, 1500); // 1500 milisegundos = 1,5 segundos
    } catch (err) {
      error.value = err.message;
    }
  };
  
  onMounted(() => {
    fetchRoles();
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