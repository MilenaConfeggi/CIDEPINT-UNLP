<template>
  <div class="container mt-4">
    <div class="title-container">
      <hr class="line">
      <h3 class="text-center mb-4">Crear Usuario</h3>
      <hr class="line">
    </div>
    <div class="form-container">
      <form @submit.prevent="submitForm">
        <div class="mb-4">
          <label for="mail" class="form-label">Mail:</label>
          <input type="email" id="mail" v-model="usuario.mail" class="form-control" required>
        </div>
        <div class="mb-4">
          <label for="rol" class="form-label">Rol:</label>
          <select id="rol" v-model="usuario.rol" class="form-control" required>
            <option v-for="rol in rolesExistentes" :key="rol.id" :value="rol.id">
              {{ rol.nombre }}
            </option>
          </select>
        </div>
        <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
        <div v-if="successMessage" class="alert alert-success" role="alert">{{ successMessage }}</div>
        <button type="submit" class="btn btn-success custom-button" :disabled="isSubmitting">Crear Usuario</button>
      </form>
    </div>
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
  rol: null,
  empleado: null,
});

const rolesExistentes = ref([]);
const error = ref(null);
const successMessage = ref(null);
const isSubmitting = ref(false);

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
  isSubmitting.value = true;

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
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(() => {
  fetchRoles();
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