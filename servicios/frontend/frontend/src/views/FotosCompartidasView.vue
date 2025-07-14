<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Fotos compartidas</h1>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="fotos.length" class="row scrollable-container">
      <div v-for="foto in fotos" :key="foto.id" class="col-md-3 mb-4">
        <div class="card">
          <div class="card-img-container" @click="mostrarVerFoto(foto)">
            <template v-if="isPdf(foto.nombre_archivo)">
              <div class="pdf-icon">
                <i class="fas fa-file-pdf"></i>
                <p>{{ foto.nombre_archivo }}</p>
              </div>
            </template>
            <template v-else>
              <img
                :src="getImageUrl(foto.legajo_id, foto.nombre_archivo)"
                alt="Imagen de foto"
                class="card-img"
              />
            </template>
          </div>
          <div class="card-body">
            <h5 class="card-title">{{ foto.nombre_archivo }}</h5>
            <p class="card-text" v-if="foto.descripcion && foto.descripcion.trim() !== ''">
              <strong>horas:</strong> {{ foto.descripcion }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center">
      <p class="text-muted">No hay fotos disponibles.</p>
    </div>

    <!-- Modal de VerFoto -->
    <div v-if="mostrarVerFotoModal" class="modal-overlay" @click="cerrarVerFoto">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarVerFoto">&times;</button>
        <div v-if="fotoSeleccionada">
          <div class="text-center">
            <img
              v-if="!isPdf(fotoSeleccionada.nombre_archivo)"
              :src="getImageUrl(fotoSeleccionada.legajo_id, fotoSeleccionada.nombre_archivo)"
              alt="Imagen de foto"
              class="img-fluid large-image"
            />
            <iframe
              v-else
              :src="getImageUrl(fotoSeleccionada.legajo_id, fotoSeleccionada.nombre_archivo)"
              class="pdf-viewer"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const fotos = ref([])
const error = ref(null)
const mostrarVerFotoModal = ref(false)
const fotoSeleccionada = ref(null)

function getImageUrl(legajoId, filename) {
  return `${import.meta.env.VITE_API_URL}/muestras/imagenes/${legajoId}/${filename}`;
}

function isPdf(filename) {
  return filename && filename.toLowerCase().endsWith('.pdf')
}

function mostrarVerFoto(foto) {
  fotoSeleccionada.value = foto
  mostrarVerFotoModal.value = true
}

function cerrarVerFoto() {
  mostrarVerFotoModal.value = false
  fotoSeleccionada.value = null
}

onMounted(async () => {
  try {
    const { data } = await axios.get(
      `${import.meta.env.VITE_API_URL}/muestras/compartido/fotos/${route.params.token}`
    )
    fotos.value = Array.isArray(data) ? data : (data.fotos || [])
    console.log('Fotos recibidas:', fotos.value)
    fotos.value.forEach(f => console.log('Nombre archivo:', f.nombre_archivo, 'Legajo:', f.legajo_id));
  } catch (e) {
    error.value = 'El enlace es inválido o ha expirado.'
  }
})
</script>

<style scoped>
.scrollable-container {
  max-height: 60vh;
  overflow-y: auto;
}
.card-img-container {
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  cursor: pointer;
}
.card-img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}
.pdf-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #dc3545;
  font-size: 3rem;
}
.pdf-icon p {
  margin-top: 10px;
  font-size: 1rem;
  text-align: center;
}
.card-body {
  position: relative;
  color: #000000;
  background-color: #ffffff;
  padding-right: 40px;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 80%;
  width: 100%;
  position: relative;
}
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
.img-fluid.large-image {
  max-width: 100%;
  height: auto;
  max-height: 80vh;
}
.pdf-viewer {
  width: 100%;
  height: 80vh;
  border: none;
}
</style>