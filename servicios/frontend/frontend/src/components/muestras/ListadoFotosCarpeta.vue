<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Fotos para la fecha {{ formatFecha(fechaSeleccionada) }}</h1>
    <div class="d-flex justify-content-end mb-3">
      <button v-if="tienePermisoDescargar" class="btn btn-primary" @click="descargarSeleccionadas">
        <i class="fas fa-download"></i> Descargar
      </button>
      <button v-if="tienePermisoEnviarMail" class="btn btn-secondary ml-2" @click="enviarMail">
        <i class="fas fa-envelope"></i> Enviar Correo
      </button>
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="fotos.length" class="row scrollable-container">
      <div v-for="foto in fotos" :key="foto.id" class="col-md-3 mb-4">
        <div class="card" :class="{ 'selected': seleccionadas.includes(foto.id) }" @click="toggleSeleccionar(foto.id)">
          <div class="card-img-container" @click.stop="mostrarVerFoto(foto)">
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
            <!-- Botón de eliminar -->
            <button class="btn-icon btn-delete" @click.stop="confirmarEliminarFoto(foto.id)">
              <i class="fas fa-trash-alt"></i>
            </button>
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

<script>
import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const permisos = JSON.parse(localStorage.getItem('permisos')) || [];

const tienePermisoDescargar = computed(() => {
  return permisos.includes('descargar_fotos');
});

const tienePermisoEnviarMail = computed(() => {
  return permisos.includes('enviar_fotos');
});

export default {
  props: {
    fechaSeleccionada: {
      type: String,
      required: true
    },
    legajoId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const fotos = ref([]);
    const error = ref(null);
    const mostrarVerFotoModal = ref(false);
    const fotoSeleccionada = ref(null);
    const seleccionadas = ref([]);
    const router = useRouter();

    const fetchFotos = async () => {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/muestras/fotos_por_fecha/${props.legajoId}/${props.fechaSeleccionada}`, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        if (response.status < 200 || response.status >= 300) {
          throw ({ message: 'Error en la petición', status: response.status });
        }
        fotos.value = response.data;
      } catch (err) {
        if (err.status === 401 || err.status === 422) {
          authStore.logout();
          router.push('/log-in');
        } else {
          error.value = 'Error al cargar las fotos';
          console.error(err);
        }
      }
    };

    const getImageUrl = (legajoId, filename) => {
      return `${import.meta.env.VITE_API_URL}/muestras/imagenes/${props.legajoId}/${filename.replace(/ /g, "_")}`;
    };

    const mostrarVerFoto = (foto) => {
      fotoSeleccionada.value = foto;
      mostrarVerFotoModal.value = true;
    };

    const cerrarVerFoto = () => {
      mostrarVerFotoModal.value = false;
      fotoSeleccionada.value = null;
    };

    const formatFecha = (fecha) => {
      const [year, month, day] = fecha.split('-');
      return `${day}-${month}-${year}`;
    };

    const toggleSeleccionar = (id) => {
      const index = seleccionadas.value.indexOf(id);
      if (index > -1) {
        seleccionadas.value.splice(index, 1);
      } else {
        seleccionadas.value.push(id);
      }
    };

    const descargarSeleccionadas = async () => {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      for (const id of seleccionadas.value) {
        try {
          const response = await fetch(`/muestras/descargar_fotos/${id}`, {
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json"
            }
          });
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = url;
          a.download = `foto_${id}.jpg`; // Cambia la extensión según sea necesario
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
        } catch (error) {
          console.error('Error al descargar la foto:', error);
        }
      }
    };

    const enviarMail = async () => {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/muestras/enviar_mail/${props.legajoId}/${props.fechaSeleccionada}`, {}, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        console.log(response.data);
        this.toast.success('Correo enviado correctamente');
      } catch (error) {
        console.error('Error al enviar el correo:', error);
        this.toast.error('Error al enviar el correo');
      }
    };

    const confirmarEliminarFoto = (idFoto) => {
      if (confirm("¿Estás seguro de que quieres eliminar esta foto?")) {
        eliminarFoto(idFoto);
      }
    };

    const eliminarFoto = async (idFoto) => {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await axios.delete(`${import.meta.env.VITE_API_URL}/muestras/eliminar_foto/${idFoto}`, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        if (response.status === 200) {
          fotos.value = fotos.value.filter(foto => foto.id !== idFoto); // Eliminar la foto del listado
        }
      } catch (error) {
        console.error('Error al eliminar la foto:', error);
        error.value = 'Error al eliminar la foto';
      }
    };

    // Detecta si el archivo es PDF
    const isPdf = (filename) => {
      return filename && filename.toLowerCase().endsWith('.pdf');
    };

    onMounted(() => {
      fetchFotos();
    });

    watch(() => props.fechaSeleccionada, fetchFotos);

    return {
      fotos,
      error,
      getImageUrl,
      mostrarVerFoto,
      cerrarVerFoto,
      mostrarVerFotoModal,
      fotoSeleccionada,
      formatFecha,
      seleccionadas,
      toggleSeleccionar,
      descargarSeleccionadas,
      enviarMail,
      confirmarEliminarFoto,
      eliminarFoto,
      tienePermisoDescargar,
      tienePermisoEnviarMail,
      isPdf
    };
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

.foto-card {
  position: relative;
  display: inline-block;
  margin: 10px;
}

.card.selected {
  border: 2px solid #007bff;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary i {
  margin-right: 5px;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary i {
  margin-right: 5px;
}

.ml-2 {
  margin-left: 0.5rem;
}

.btn-icon {
  background: none;
  border: none;
  color: #dc3545; /* Rojo */
  cursor: pointer;
  font-size: 1.2rem;
  position: absolute;
  top: 10px;
  right: 10px;
}

.btn-icon:hover {
  color: #a71d2a; /* Rojo más oscuro */
}
</style>