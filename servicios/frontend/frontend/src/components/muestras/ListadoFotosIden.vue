<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Fotos para la muestra {{ muestraId }}</h1>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="fotos.length" class="row scrollable-container">
      <div v-for="foto in fotos" :key="foto.id" class="col-md-3 mb-4">
        <div class="card">
          <div class="card-img-container" @click="mostrarVerFoto(foto)">
            <img
              :src="getImageUrl(foto.muestra_id, foto.nombre_archivo)"
              alt="Imagen de foto"
              class="card-img"
            />
          </div>
          <div class="card-body">
            <h5 class="card-title">{{ foto.nombre_archivo }}</h5>
            <p class="card-text">Fecha de carga: {{ foto.fecha }}</p>
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
            <img :src="getImageUrl(fotoSeleccionada.muestra_id, fotoSeleccionada.nombre_archivo)" alt="Imagen de foto" class="img-fluid large-image" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth'

export default {
  props: {
    muestraId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const fotos = ref([]);
    const error = ref(null);
    const mostrarVerFotoModal = ref(false);
    const fotoSeleccionada = ref(null);

    const fetchFotos = async () => {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/muestras/fotos/${props.muestraId}`, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "multipart/form-data"
          }
        });
        fotos.value = response.data;
      } catch (err) {
        error.value = 'Error al cargar las fotos';
        console.error(err);
      }
    };

    const getImageUrl = (muestraId, filename) => {
      return `${import.meta.env.VITE_API_URL}/muestras/imagenes/${muestraId}/${filename.replace(/ /g, "_")}`;
    };

    const mostrarVerFoto = (foto) => {
      fotoSeleccionada.value = foto;
      mostrarVerFotoModal.value = true;
    };

    const cerrarVerFoto = () => {
      mostrarVerFotoModal.value = false;
      fotoSeleccionada.value = null;
    };

    onMounted(() => {
      fetchFotos();
    });

    watch(() => props.muestraId, fetchFotos);

    return { fotos, error, getImageUrl, mostrarVerFoto, cerrarVerFoto, mostrarVerFotoModal, fotoSeleccionada };
  }
};
</script>

<style scoped>
.scrollable-container {
  max-height: 60vh; /* Limitar la altura máxima del contenedor de fotos */
  overflow-y: auto; /* Habilitar el desplazamiento vertical */
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

.card-body {
  position: relative;
  color: #000000;
  background-color: #ffffff; 
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
</style>