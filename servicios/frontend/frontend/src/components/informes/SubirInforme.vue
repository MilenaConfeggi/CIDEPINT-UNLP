<template>
    <div class="container mt-4">
      <h3 class="text-center mb-4">Subir Informe</h3>
      <form @submit.prevent="submitForm" enctype="multipart/form-data">
        <div class="mb-3">
          <label for="archivo" class="form-label">Selecciona archivo:</label>
          <div class="file-upload-wrapper">
            <!-- Input file oculto -->
            <input
              type="file"
              id="archivo"
              class="file-upload-input"
              @change="handleFileUpload"
              required
            />
            <!-- Botón para activar el input file -->
            <button type="button" class="btn btn-file custom-button" @click="triggerFileInput">
              <i class="fas fa-upload"></i> Seleccionar archivo
            </button>
          </div>
          <!-- Mostrar el nombre del archivo seleccionado -->
          <div v-if="fileName" class="mt-2">
            <p><strong>Archivo seleccionado:</strong> {{ fileName }}</p>
          </div>
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
        fileName: null // Nombre del archivo seleccionado
      };
    },
    methods: {
      handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
          this.fileName = file.name;
          this.formData = new FormData();
          this.formData.append('archivo', file);
        }
      },
      triggerFileInput() {
        document.getElementById('archivo').click();
      },
      async submitForm() {
        this.isUploading = true;
        this.error = null;
        this.successMessage = null;
  
        try {
          const response = await fetch(
            `${import.meta.env.VITE_API_URL}/informes/cargar_informe/${this.legajoId}`,
            {
              method: 'POST',
              body: this.formData,
            }
          );
  
          const data = await response.json();
  
          if (!response.ok) {
            throw new Error(data.error || 'Error al enviar los datos');
          }
  
          this.successMessage = data.message || 'Archivo subido con éxito';
          console.log('Respuesta del servidor:', data);
        } catch (error) {
          this.error = error.message || 'Hubo un problema al subir el archivo';
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
    display: flex;
    align-items: center;
  }
  
  .file-upload-input {
    display: none;
  }
  
  .btn-file {
    display: flex;
    align-items: center;
    background-color: #4897ff;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    border: none;
    font-size: 16px;
  }
  
  .btn-file:hover {
    background-color: #0056b3;
  }
  
  .btn-file i {
    margin-right: 8px;
  }
  
  .spinner-border {
    width: 3rem;
    height: 3rem;
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
  
  .alert {
    margin-top: 20px;
  }
  </style>