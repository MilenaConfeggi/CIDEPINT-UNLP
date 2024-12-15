<template>
  <div class="container mt-4">
    <div class="title-container">
      <hr class="line">
      <h3 class="text-center mb-4">Identificar Muestras</h3>
      <hr class="line">
    </div>
    <div class="form-container">
      <form @submit.prevent="submitForm">
        <div v-for="(muestra, index) in muestras" :key="index" class="mb-3">
          <label :for="'fechaIngreso' + index" class="form-label">Fecha de Ingreso:</label>
          <input
            type="date"
            :id="'fechaIngreso' + index"
            v-model="muestra.fechaIngreso"
            class="form-control"
            required
          />
          <label :for="'idenCliente' + index" class="form-label">Identificación del Cliente:</label>
          <input
            type="text"
            :id="'idenCliente' + index"
            v-model="muestra.idenCliente"
            class="form-control"
            required
          />
          <button type="button" @click="removeMuestra(index)" class="btn-icon">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
        <button type="button" @click="addMuestra" class="btn btn-secondary mb-3">Agregar Muestra</button>
        <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
        <div v-if="successMessage" class="alert alert-success" role="alert">{{ successMessage }}</div>
        <button type="submit" class="btn btn-success custom-button" :disabled="isSubmitting">Identificar</button>
      </form>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { ref, onMounted, computed } from 'vue';
export default {
  props: {
    legajoId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      muestras: [
        { fechaIngreso: '', idenCliente: '' }
      ],
      isSubmitting: false,
      error: null,
      successMessage: null
    };
  },
  methods: {
    addMuestra() {
      this.muestras.push({ fechaIngreso: '', idenCliente: '' });
    },
    removeMuestra(index) {
      this.muestras.splice(index, 1);
    },
    async submitForm() {
      this.isSubmitting = true;
      this.error = null;
      this.successMessage = null;
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/muestras/subir_muestras/${this.legajoId}`,
          {
            method: 'POST',
            headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          },
            body: JSON.stringify(this.muestras)
          }
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Error al enviar los datos');
        }

        this.successMessage = data.message || 'Muestras identificadas con éxito';
        console.log('Respuesta del servidor:', data);
      } catch (error) {
        this.error = error.message || 'Hubo un problema al identificar las muestras';
        console.error('Error:', error);
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
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

.btn-icon {
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-size: 1.2rem;
  margin-left: 10px;
}

.btn-icon:hover {
  color: #a71d2a;
}
.form-container {
  max-height: 400px; 
  overflow-y: auto;
  overflow-x: hidden; 
}
</style>