<template>
  <div class="container mt-4">
    <div class="title-container">
      <hr class="line">
      <h1 class="text-center mb-4 title">Muestras para el legajo {{ legajoId }}</h1>
      <hr class="line">
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="muestras.length" class="row">
      <div v-for="muestra in muestras" :key="muestra.id" class="col-md-3 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Número de muestra: {{ muestra.nro_muestra }}</h5>
            <p class="card-text">Iden cliente: {{ muestra.iden_cliente }}</p>
            <p class="card-text">Fecha de ingreso: {{ muestra.fecha_ingreso }}</p>
            <div class="d-flex align-items-center">
              <button @click="mostrarFotos(muestra.id)" class="btn btn-primary">Ver fotos</button>
              <template v-if="muestra.terminada">
                <p class="text-danger mb-0 ml-2">Terminada</p>
              </template>
              <template v-else>
                <button v-if="tienePermisoTerminar" @click="confirmarTerminarMuestra(muestra.id)" class="btn btn-danger ml-2">Terminar</button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center">
      <p class="text-muted">No hay muestras disponibles.</p>
    </div>

    <!-- Modal de ListadoFotosIden -->
    <div v-if="mostrarListadoFotos" class="modal-overlay" @click="cerrarListadoFotos">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarListadoFotos">&times;</button>
        <ListadoFotosIden :muestra-id="muestraSeleccionada" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useMuestrasStore } from '@/stores/muestras';
import { storeToRefs } from 'pinia';
import ListadoFotosIden from './ListadoFotosIden.vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export default {
  components: {
    ListadoFotosIden
  },
  props: {
    legajoId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const store = useMuestrasStore();
    const { muestras, error } = storeToRefs(store);

    const mostrarListadoFotos = ref(false);
    const muestraSeleccionada = ref(null);

    const permisos = JSON.parse(localStorage.getItem('permisos')) || [];

    const tienePermisoTerminar = computed(() => {
      return permisos.includes('terminar_muestra');
    });

    const fetchMuestras = async () => {
      await store.fetchMuestras(props.legajoId);
    };

    const mostrarFotos = (muestraId) => {
      muestraSeleccionada.value = muestraId;
      mostrarListadoFotos.value = true;
    };

    const cerrarListadoFotos = () => {
      mostrarListadoFotos.value = false;
      muestraSeleccionada.value = null;
    };

    const confirmarTerminarMuestra = (muestraId) => {
      if (confirm("¿Estás seguro de que deseas terminar esta muestra?")) {
        terminarMuestra(muestraId);
      }
    };

    const terminarMuestra = async (muestraId) => {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/muestras/terminar_muestra/${muestraId}`, {}, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          },
        });

        if (response.status === 200) {
          fetchMuestras(); // Refrescar la lista de muestras después de terminar una muestra
        }
      } catch (error) {
        console.error('Error al terminar la muestra:', error);
      }
    };

    onMounted(() => {
      fetchMuestras();
    });

    watch(() => props.legajoId, fetchMuestras);

    return { muestras, error, mostrarFotos, cerrarListadoFotos, mostrarListadoFotos, muestraSeleccionada, confirmarTerminarMuestra, tienePermisoTerminar };
  }
};
</script>

<style scoped>
.card {
  background-color: #cde3e4;
  color: #000000;
  border: 1px solid #9bc1bc;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 1.25rem;
  margin-bottom: 10px;
}

.card-text {
  font-size: 1rem;
  margin-bottom: 5px;
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

.d-flex {
  display: flex;
}

.align-items-center {
  align-items: center;
}

.ml-2 {
  margin-left: 0.5rem;
}

.mb-0 {
  margin-bottom: 0;
}
</style>