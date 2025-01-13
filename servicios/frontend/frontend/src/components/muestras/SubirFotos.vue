<template>
  <div class="container mt-4">
    <h3 class="text-center mb-4">Subir Fotos</h3>
    <div class="form-scroll-container">
      <form @submit.prevent="submitForm" enctype="multipart/form-data">
        <div v-for="(foto, index) in fotos" :key="index" class="mb-4">
          <div class="mb-3">
            <label :for="'archivo' + index" class="form-label">Selecciona archivo:</label>
            <div class="file-upload-wrapper">
              <input
                :id="'archivo' + index"
                type="file"
                class="file-upload-input"
                @change="handleFileUpload($event, index)"
                required
                style="display: none;"
              />
              <button type="button" class="btn btn-file custom-button" @click="triggerFileInput(index)">
                <i class="fas fa-upload"></i> Seleccionar archivo
              </button>
            </div>
            <div v-if="foto.fileName" class="mt-2">
              <p><strong>Archivo seleccionado:</strong> {{ foto.fileName }}</p>
            </div>
          </div>
          <div class="mb-3">
            <label :for="'muestra' + index" class="form-label">Selecciona número de muestra:</label>
            <select :id="'muestra' + index" v-model="foto.selectedMuestra" class="form-control" required>
              <option v-for="muestra in muestras" :key="muestra.id" :value="muestra.id">
                {{ muestra.nro_muestra }} - {{ muestra.iden_cliente }}
              </option>
            </select>
          </div>
          <div class="mb-3">
            <label :for="'fecha' + index" class="form-label">Fecha:</label>
            <input :id="'fecha' + index" type="date" v-model="foto.fecha" class="form-control" required />
          </div>
          <button type="button" class="btn btn-icon" @click="removeFoto(index)">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
        <div class="mb-3">
          <button type="button" class="btn btn-secondary" @click="addFoto">Subir otra foto</button>
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
      muestras: [],
      fotos: [
        {
          file: null,
          fileName: '',
          selectedMuestra: null,
          fecha: null
        }
      ]
    };
  },
  methods: {
    async fetchMuestras() {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      const router = useRouter();
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/muestras/${this.legajoId}`, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          },
        });

        if (!response.ok) {
          throw ({message: 'Error al obtener las muestras', status: response.status})
        }
        if (response.status === 200) {
          this.muestras = response.data.filter(muestra => !muestra.terminada); // Filtrar muestras terminadas
        } else {
          this.error = response.data.message || 'Error al obtener las muestras';
        }
      } catch (error) {
        if (error.status === 401 || error.status === 422) {
          authStore.logout()
          router.push('/log-in')
        }
        if (error.response && error.response.status === 404) {
          this.error = 'No se encontraron muestras';
        } else {
          this.error = error.response?.data?.message || error.message || 'Error al obtener las muestras';
        }
      }
    },
    handleFileUpload(event, index) {
      const file = event.target.files[0];
      if (file) {
        this.fotos[index].file = file;
        this.fotos[index].fileName = file.name;
      }
    },
    triggerFileInput(index) {
      document.getElementById('archivo' + index).click();
    },
    addFoto() {
      this.fotos.push({
        file: null,
        fileName: '',
        selectedMuestra: null,
        fecha: null
      });
    },
    removeFoto(index) {
      this.fotos.splice(index, 1);
    },
    async submitForm() {
      this.isUploading = true;
      this.error = null;
      this.successMessage = null;

      const authStore = useAuthStore();
      const token = authStore.getToken();

      try {
        for (const foto of this.fotos) {
          const formData = new FormData();
          formData.append('archivo', foto.file);
          formData.append('muestra_id', foto.selectedMuestra);
          formData.append('fecha', foto.fecha);

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

          this.successMessage = response.data.message || 'Fotos subidas con éxito';
          console.log('Respuesta del servidor:', response.data);
        }
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

.form-scroll-container {
  max-height: 400px;
  overflow-y: auto;
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