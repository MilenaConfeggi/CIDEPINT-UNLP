<template>
    <div class="container mt-4">
      <h3 class="text-center mb-4">Subir Fotos</h3>
      <form @submit.prevent="submitForm" enctype="multipart/form-data">
        <div class="mb-3">
          <label for="archivo" class="form-label">Selecciona archivo:</label>
          <div class="file-upload-wrapper">
            <input
              type="file"
              id="archivo"
              class="file-upload-input"
              @change="handleFileUpload"
              required
              style="display: none;"
            />
            <button type="button" class="btn btn-file custom-button" @click="triggerFileInput">
              <i class="fas fa-upload"></i> Seleccionar archivo
            </button>
          </div>
          <div v-if="fileNames.length" class="mt-2">
            <p><strong>Archivo seleccionado:</strong></p>
            <ul>
              <li v-for="(fileName, index) in fileNames" :key="fileName">
                {{ fileName }}
                <button type="button" @click="removeFile(index)" class="btn-icon">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </li>
            </ul>
          </div>
        </div>
        <div class="mb-3">
          <label for="muestra" class="form-label">Selecciona número de muestra:</label>
          <select id="muestra" v-model="selectedMuestra" class="form-control" required>
            <option v-for="muestra in muestras" :key="muestra.id" :value="muestra.id">
              {{ muestra.nro_muestra }} - {{ muestra.iden_cliente }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label for="fecha" class="form-label">Fecha:</label>
          <input type="date" id="fecha" v-model="fecha" class="form-control" required />
        </div>
        <div v-if="isUploading" class="mb-3 text-center">
          <div class="spinner-border" role="status">
            <span class="sr-only">Cargando...</span>
          </div>
          <p>Subiendo archivo...</p>
        </div>
        <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>
        <div v-if="successMessage" class="alert alert-success" role="alert">
          {{ successMessage }}
        </div>
        <button type="submit" class="btn btn-success custom-button" :disabled="isUploading">Subir</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      legajoId: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        formData: new FormData(),
        isUploading: false,
        error: null,
        successMessage: null,
        fileNames: [],
        files: [],
        muestras: [],
        selectedMuestra: null,
        fecha: null
      };
    },
    methods: {
      async fetchMuestras() {
        try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/muestras/${this.legajoId}`);
          const data = await response.json();
          if (response.ok) {
            this.muestras = data;
          } else {
            this.error = data.message || 'Error al obtener las muestras';
          }
        } catch (error) {
          this.error = error.message || 'Error al obtener las muestras';
        }
      },
      handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
          this.fileNames = [file.name];
          this.files = [file];
          this.formData.set('archivo', file);
        }
      },
      removeFile(index) {
        this.fileNames.splice(index, 1);
        this.files.splice(index, 1);
        this.formData.delete('archivo');
      },
      triggerFileInput() {
        document.getElementById('archivo').click();
      },
      async submitForm() {
        this.isUploading = true;
        this.error = null;
        this.successMessage = null;
  
        try {
          this.formData.set('muestra_id', this.selectedMuestra);
          this.formData.set('fecha', this.fecha);
          const response = await fetch(
            `${import.meta.env.VITE_API_URL}/muestras/subir_fotos/${this.legajoId}`,
            {
              method: 'POST',
              body: this.formData,
            }
          );
  
          const data = await response.json();
  
          if (!response.ok) {
            throw new Error(data.error || 'Error al enviar los datos');
          }
  
          this.successMessage = data.message || 'Fotos subidas con éxito';
          console.log('Respuesta del servidor:', data);
        } catch (error) {
          this.error = error.message || 'Hubo un problema al subir las fotos, asegúrate de que los archivos sean .png, .jpg o .jpeg';
          console.error('Error:', error);
        } finally {
          this.isUploading = false;
        }
      }
    },
    mounted() {
      this.fetchMuestras();
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
  </style>