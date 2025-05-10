<template>
  <div class="container mt-4">
    <div class="title-container">
      <hr class="line">
      <h3 class="text-center mb-4">Identificar Muestras</h3>
      <hr class="line">
    </div>
    <div v-if="ultimaMuestra" class="alert alert-info">
      La última muestra fue la {{ ultimaMuestra }}
    </div>
    <div class="form-container">
      <form @submit.prevent="submitForm" class="scrollable-form">
        <div v-for="(muestra, index) in muestras" :key="index" class="mb-3">
          <label :for="'nroMuestra' + index" class="form-label">Número de Muestra:</label>
          <input
            type="number"
            :id="'nroMuestra' + index"
            v-model="muestra.nroMuestra"
            class="form-control"
            required
          />
          <label :for="'nroGrupo' + index" class="form-label">Número de Grupo (Opcional):</label>
          <input
            type="number"
            :id="'nroGrupo' + index"
            v-model="muestra.nroGrupo"
            class="form-control"
          />
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
        <div class="button-container">
          <button type="button" @click="addMuestra" class="btn btn-secondary">Agregar Muestra</button>
          <button type="submit" class="btn btn-success" :disabled="isSubmitting">Identificar</button>
        </div>
        <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
        <div v-if="successMessage" class="alert alert-success" role="alert">{{ successMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { ref, onMounted } from 'vue';
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
        { nroMuestra: '', nroGrupo: '', fechaIngreso: '', idenCliente: '' }
      ],
      ultimaMuestra: null,
      isSubmitting: false,
      error: null,
      successMessage: null
    };
  },
  methods: {
    async fetchUltimaMuestra() {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/muestras/ultima_muestra`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        if (response.ok) {
          const data = await response.json();
          this.ultimaMuestra = data.ultimaMuestra; // Mostrar el formato "nrodemuestra-nrodegrupo"
        }
      } catch (error) {
        console.error('Error al obtener la última muestra:', error);
      }
    },
    addMuestra() {
      this.muestras.push({ nroMuestra: '', nroGrupo: '', fechaIngreso: '', idenCliente: '' });
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
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.muestras)
          }
        );

        const data = await response.json();

        if (response.status !== 200) {
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
  },
  mounted() {
    this.fetchUltimaMuestra();
  }
};
</script>

<style scoped>
.scrollable-form {
  max-height: 400px; /* Ajusta el tamaño máximo del contenedor */
  overflow-y: auto; /* Habilita el scroll vertical */
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.button-container {
  display: flex;
  justify-content: space-between; /* Alinea los botones horizontalmente */
  margin-top: 15px;
}

.btn-icon {
  margin-left: 10px;
  color: #dc3545;
  background: none;
  border: none;
  cursor: pointer;
}

.btn-icon i {
  font-size: 1.2rem;
}

.btn-icon:hover {
  color: #a71d2a;
}
</style>