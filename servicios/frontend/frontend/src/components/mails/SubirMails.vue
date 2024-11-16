<template>
  <div class="container mt-4">
    <h3 class="text-center mb-4">Subir Imagen</h3>
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="archivo" class="form-label">Selecciona un archivo:</label>
        <input
          type="file"
          id="archivo"
          class="form-control"
          @change="handleFileUpload"
          required
        />
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
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.formData.append('archivo', file);
      }
    },
    async submitForm() {
      this.isUploading = true;
      this.error = null;
      this.successMessage = null;
      
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/mails/subir_mail/${this.legajoId}`,
          {
            method: 'POST',
            body: this.formData,
          }
        );

        if (!response.ok) {
          throw new Error('Error al enviar los datos');
        }

        const data = await response.json();
        this.successMessage = 'Archivo subido con éxito';
        console.log('Respuesta del servidor:', data);
      } catch (error) {
        this.error = 'Hubo un problema al subir el archivo.';
        console.error('Error:', error);
      } finally {
        this.isUploading = false;
      }
    }
  },
};
</script>

<style scoped>
/* Estilo adicional para el formulario */
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

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>