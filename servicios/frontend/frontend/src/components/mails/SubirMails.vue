<template>
  <div class="container mt-4">
    <h3 class="text-center mb-4">Subir Archivos</h3>
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="archivo" class="form-label">Selecciona archivos:</label>
        <div class="file-upload-wrapper">
          <!-- Input file oculto -->
          <input
            type="file"
            id="archivo"
            class="file-upload-input"
            @change="handleFileUpload"
            multiple
            required
          />
          <!-- Botón para activar el input file -->
          <button type="button" class="btn btn-file custom-button" @click="triggerFileInput">
            <i class="fas fa-upload"></i> Seleccionar archivos
          </button>
        </div>
        <!-- Mostrar el nombre de los archivos seleccionados -->
        <div v-if="fileNames.length" class="mt-2">
          <p><strong>Archivos seleccionados:</strong></p>
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
      fileNames: [], // Lista de nombres de archivos seleccionados
      files: [] // Lista de archivos seleccionados
    };
  },
  methods: {
    handleFileUpload(event) {
      const maxFileSize = 4096 * 1024 * 1024; 
      const newFiles = event.target.files;

      for (let i = 0; i < newFiles.length; i++) {
        const file = newFiles[i];
        if (file.size > maxFileSize) {
          this.error = `El archivo ${file.name} excede el tamaño máximo.`;
          continue;
        }
        this.fileNames.push(file.name);
        this.files.push(file);
        this.formData.append('archivo', file);
      }
    },
    removeFile(index) {
      this.fileNames.splice(index, 1);
      this.files.splice(index, 1);
      this.formData = new FormData();
      this.files.forEach(file => {
        this.formData.append('archivo', file);
      });
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
          `${import.meta.env.VITE_API_URL}/mails/subir_mail/${this.legajoId}`,
          {
            method: 'POST',
            body: this.formData,
          }
        );

        const data = await response.json();

        if (response.status !== 200) {
          throw new Error(data.error || 'Error al enviar los datos');
        }

        this.successMessage = data.message || 'Archivos subidos con éxito';
        console.log('Respuesta del servidor:', data);
      } catch (error) {
        this.error = error.message || 'Hubo un problema al subir los archivos, asegúrate de que los archivos sean .png, .jpg, .jpeg o .pdf';
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