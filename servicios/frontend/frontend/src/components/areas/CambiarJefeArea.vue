<template>
    <div class="container mt-4">
      <div class="title-container">
        <hr class="line">
        <h3 class="text-center mb-4">Cambiar Jefe De Area</h3>
        <hr class="line">
      </div>
      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="mb-4">
            
            <label for="area" class="form-label">Seleccione un area:</label>
            <select id="area" v-model="area" class="form-control" required>
              <option v-for="area in areasExistentes" :key="area.id" :value="area.id">
                {{ area.nombre }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label for="usuario" class="form-label">Seleccione un usuario de ese área para hacerlo jefe de área</label>
            <select id="usuario" v-model="usuario" class="form-control" required>
              <option v-for="usuario in usuariosExistentes" :key="usuario.id" :value="usuario.id">
                {{ usuario.mail }}
              </option>
            </select>
          </div>
          <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
          <div v-if="successMessage" class="alert alert-success" role="alert">{{ successMessage }}</div>
          <button type="submit" class="btn btn-success custom-button" :disabled="isSubmitting">Hacer Jefe de área</button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const authStore = useAuthStore();
  
  const area = ref(null); // Cambiado a valor simple
  const usuario = ref(null);
  
  const areasExistentes = ref([]);
  const usuariosExistentes = ref([]);
  const error = ref(null);
  const successMessage = ref(null);
  const isSubmitting = ref(false);

  const token = authStore.getToken();
  
  const fetchAreas = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/areas`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`, // Token JWT en el header
        "Content-Type": "application/json", // Header opcional para el tipo de contenido
      },
      });
      if (!response.ok) {
        throw new Error('Error al obtener las áreas');
      }
      areasExistentes.value = await response.json();
    } catch (error) {
      console.error('Error al obtener las áreas:', error);
    }
  };
  
  const fetchUsuarios = async () => {
    try {
      if (!area.value) return; // Verifica que haya un área seleccionada
      const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/${area.value}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`, // Token JWT en el header
        "Content-Type": "application/json", // Header opcional para el tipo de contenido
      },
      });
      if (!response.ok) {
        throw new Error('Error al obtener los usuarios de un área');
      }
      usuariosExistentes.value = await response.json();
    } catch (error) {
      console.error('Error al obtener los usuarios de un área:', error);
    }
  };
  
  // Observa los cambios en el área seleccionada
  watch(area, (newValue) => {
    if (newValue) {
      fetchUsuarios();
    }
  });
  
  const submitForm = async () => {
    error.value = null;
    successMessage.value = null;
    isSubmitting.value = true;
  
    const data = { usuario_id: usuario.value, area_id: area.value };
  
    try {
      const token = authStore.getToken();
      const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/cambiar_jefe_area`, {
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
      
    } catch (err) {
      error.value = err.message;
    } finally {
      isSubmitting.value = false;
    }
  };
  
  onMounted(() => {
    fetchAreas();
  });
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  
  .form-control {
    border-radius: 8px;
  }
  
  .btn-success {
    width: 100%;
    border-radius: 8px;
  }
  
  .custom-button {
    background-color: #28a745;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    transition-duration: 0.4s;
  }
  
  .custom-button:hover {
    background-color: white;
    color: black;
    border: 2px solid #28a745;
  }
  
  .line {
    border: 0;
    height: 1px;
    background: #333;
    background-image: linear-gradient(to right, #ccc, #333, #ccc);
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
  
  .form-container {
    max-height: 400px; 
    overflow-y: auto;
    overflow-x: hidden; 
  }
  </style>