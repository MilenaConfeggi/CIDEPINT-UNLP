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
            <!-- Mostrar nro_muestra-nro_grupo -->
            <h5 class="card-title">
              Número de muestra: {{ formatNumeroMuestra(muestra.nro_muestra, muestra.nro_grupo) }}
            </h5>
            <p class="card-text">Iden cliente: {{ muestra.iden_cliente }}</p>
            <p class="card-text">Fecha de ingreso: {{ muestra.fecha_ingreso }}</p>
            <p v-if="muestra.terminada" class="text-danger mb-0">Terminada</p>
            <div class="d-flex justify-content-end align-items-center">
              <button
                v-if="tienePermisoTerminar && !muestra.terminada"
                @click="confirmarTerminarMuestra(muestra.id)"
                class="btn btn-warning btn-sm btn-terminar"
              >
                Terminar
              </button>
              <button 
                v-if="tienePermisoTerminar"
                @click="confirmarEliminarMuestra(muestra.id)" class="btn btn-icon">
                <i class="fas fa-trash-alt text-danger"></i>
              </button>
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
  components: {},
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
      muestras.value = []; // Limpiar el estado de las muestras antes de la nueva solicitud
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

    const confirmarEliminarMuestra = (muestraId) => {
      if (confirm("¿Estás seguro de que deseas eliminar esta muestra?")) {
        eliminarMuestra(muestraId);
      }
    };

    const eliminarMuestra = async (muestraId) => {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await axios.delete(`${import.meta.env.VITE_API_URL}/muestras/eliminar_muestra/${muestraId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        if (response.status === 200) {
          fetchMuestras(); // Refrescar la lista de muestras después de eliminar una muestra
          alert(response.data.message); // Mostrar mensaje de éxito
        }
      } catch (err) {
        alert(err.response?.data?.error || 'Error al eliminar la muestra');
      }
    };

    // Formatear el número de muestra como "nro_muestra-nro_grupo"
    const formatNumeroMuestra = (nroMuestra, nroGrupo) => {
      return nroGrupo ? `${nroMuestra}-${nroGrupo}` : `${nroMuestra}`;
    };

    onMounted(() => {
      fetchMuestras();
    });

    watch(() => props.legajoId, fetchMuestras);

    return { muestras, error, muestraSeleccionada, confirmarTerminarMuestra, tienePermisoTerminar, noMuestras, formatNumeroMuestra, confirmarEliminarMuestra };
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
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-title {
  font-size: 1.25rem;
  margin-bottom: 10px;
}

.card-text {
  font-size: 1rem;
  margin-bottom: 5px;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
}

.btn-icon i {
  font-size: 1.2rem;
}

.btn-icon:hover i {
  color: #a71d2a;
}

.btn-warning {
  background-color: #ffc107; /* Color amarillo */
  color: #000; /* Texto negro */
  border: none;
}

.btn-warning:hover {
  background-color: #e0a800; /* Amarillo más oscuro al pasar el mouse */
  color: #000;
}

.btn-terminar {
  margin-right: 2px; /* Espaciado entre el botón de terminar y el tachito */
}
</style>