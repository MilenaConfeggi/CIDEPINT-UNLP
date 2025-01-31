<template>
  <div class="container mt-4">
    <div class="title-container">
      <hr class="line">
      <h1 class="text-center mb-4 title">Muestras para el legajo {{ legajoId }}</h1>
      <hr class="line">
    </div>
    <div v-if="error && !noMuestras" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="noMuestras" class="text-center">
      <p class="text-muted">No hay muestras disponibles para este legajo.</p>
    </div>
    <div v-if="muestras.length && !noMuestras" class="row">
      <div v-for="muestra in muestras" :key="muestra.id" class="col-md-3 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Número de muestra: {{ muestra.nro_muestra }}</h5>
            <p class="card-text">Iden cliente: {{ muestra.iden_cliente }}</p>
            <p class="card-text">Fecha de ingreso: {{ muestra.fecha_ingreso }}</p>
            <div class="d-flex align-items-center">
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
    <div v-else-if="!error && !noMuestras" class="text-center">
      <p class="text-muted">No hay muestras disponibles.</p>
    </div>

  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useMuestrasStore } from '@/stores/muestras';
import { storeToRefs } from 'pinia';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export default {
  components: {
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
    const noMuestras = ref(false);

    const permisos = JSON.parse(localStorage.getItem('permisos')) || [];

    const tienePermisoTerminar = computed(() => {
      return permisos.includes('terminar_muestra');
    });

    const fetchMuestras = async () => {
      noMuestras.value = false;
      error.value = null;
      try {
        await store.fetchMuestras(props.legajoId);
        if (muestras.value.length === 0) {
          noMuestras.value = true;
        }
      } catch (err) {
        if (err.response && err.response.status === 404) {
          noMuestras.value = true;
          error.value = 'No hay muestras disponibles para este legajo.';
        } else {
          error.value = err.response?.data?.message || 'Error al obtener las muestras';
        }
      }
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
      } catch (err) {
        error.value = err.response?.data?.message || 'Error al terminar la muestra';
      }
    };

    onMounted(() => {
      fetchMuestras();
    });

    watch(() => props.legajoId, fetchMuestras);

    return { muestras, error, muestraSeleccionada, confirmarTerminarMuestra, tienePermisoTerminar, noMuestras };
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