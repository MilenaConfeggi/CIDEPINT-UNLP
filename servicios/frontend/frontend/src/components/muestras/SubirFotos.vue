<template>
  <div class="container mt-4">
    <h3 class="text-center mb-4">Subir Fotos</h3>
    <div class="form-scroll-container">
      <form @submit.prevent="submitForm" enctype="multipart/form-data">
        <div class="mb-4">
          <label for="archivo" class="form-label">Selecciona archivos:</label>
          <div class="file-upload-wrapper">
            <input
              id="archivo"
              type="file"
              class="file-upload-input"
              @change="handleFileUpload"
              multiple
              required
              style="display: none;"
            />
            <button type="button" class="btn btn-file custom-button" @click="triggerFileInput">
              <i class="fas fa-upload"></i> Seleccionar archivos
            </button>
          </div>
          <div v-if="fileNames.length" class="mt-2">
            <p><strong>Archivos seleccionados:</strong></p>
            <ul>
              <li v-for="(fileName, index) in fileNames" :key="index">{{ fileName }}</li>
            </ul>
          </div>
        </div>
        <div class="mb-4">
          <label for="fecha" class="form-label">Fecha:</label>
          <input id="fecha" type="date" v-model="fecha" class="form-control" required />
        </div>
        <div class="mb-4">
          <label for="descripcion" class="form-label">Horas:</label>
          <input id="descripcion" type="text" v-model="descripcion" class="form-control" maxlength="255" placeholder="horas" />
        </div>
        <div class="mb-3">
          <button type="submit" class="btn btn-success custom-button" :disabled="isUploading">Subir</button>
        </div>
        <div v-if="isUploading" class="mb-3 text-center">
          <div class="spinner-border" role="status">
            <span class="sr-only">Cargando...</span>
          </div>
          <p>Subiendo archivos...</p>
        </div>
        <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>
        <div v-if="successMessage" class="alert alert-success" role="alert">
          {{ successMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

export default {
  props: {
    legajoId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      isUploading: false,
      error: null,
      successMessage: null,
      fecha: null,
      descripcion: "", // Nuevo campo
      files: [],
      fileNames: []
    };
  },
  methods: {
    handleFileUpload(event) {
      const maxFileSize =  4 * 1024 * 1024 * 1024; // 4gb
      const newFiles = Array.from(event.target.files);

      this.files = [];
      this.fileNames = [];

      newFiles.forEach(file => {
        if (file.size > maxFileSize) {
          this.error = `El archivo ${file.name} excede el tamaño máximo permitido de 4gb.`;
        } else {
          this.files.push(file);
          this.fileNames.push(file.name);
        }
      });
    },
    triggerFileInput() {
      document.getElementById('archivo').click();
    },
    async submitForm() {
      this.isUploading = true;
      this.error = null;
      this.successMessage = null;

      const authStore = useAuthStore();
      const token = authStore.getToken();

      try {
        const formData = new FormData();
        this.files.forEach(file => {
          formData.append('archivos', file);
        });
        formData.append('fecha', this.fecha);
        formData.append('descripcion', this.descripcion); // Enviar descripción

        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/muestras/subir_fotos/${this.legajoId}`,
          formData,
          {
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "multipart/form-data"
            },
          }
        );

        if (response.status !== 200) {
          throw new Error(response.data.message || 'Error al enviar los datos');
        }

        this.successMessage = response.data.message || 'Fotos subidas con éxito, recargue la página para ver los cambios';
        console.log('Respuesta del servidor:', response.data);
      } catch (error) {
        this.error = error.response?.data?.message || 'Hubo un problema al subir las fotos, asegúrate de que los archivos sean .png, .jpg o .jpeg';
        console.error('Error:', error);
      } finally {
        this.isUploading = false;
      }
    }
  }
};
</script>

<style scoped>
.file-upload-wrapper {
  position: relative;
  display: inline-block;
}

.btn-file {
  display: inline-block;
  cursor: pointer;
}

.form-scroll-container {
  max-height: 400px;
  overflow-y: auto;
}

.custom-button {
  margin-top: 10px;
}

.alert {
  margin-top: 10px;
}
</style>