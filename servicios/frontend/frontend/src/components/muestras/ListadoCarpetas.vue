<template>
  <div class="container mt-4">
    <div class="title-container">
      <hr class="line">
      <h1 class="text-center mb-4">Carpetas de fotos para el legajo {{ legajoId }}</h1>
      <hr class="line">
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="Object.keys(carpetas).length" class="row">
      <div v-for="fecha in fechasOrdenadas" :key="fecha" class="col-md-3 mb-4">
        <div class="card" @click="abrirCarpeta(fecha)">
          <div class="card-body">
            <h5 class="card-title">
              <i class="fas fa-calendar-alt"></i> {{ formatFecha(fecha) }}
            </h5>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center">
      <p class="text-muted">No hay fotos disponibles.</p>
    </div>

    <!-- Modal de ListadoFotosCarpeta -->
    <div v-if="mostrarListadoFotosCarpeta" class="modal-overlay" @click="cerrarListadoFotosCarpeta">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarListadoFotosCarpeta">&times;</button>
        <ListadoFotosCarpeta :fecha-seleccionada="fechaSeleccionada" :legajo-id="legajoId" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import ListadoFotosCarpeta from './ListadoFotosCarpeta.vue';

export default {
  components: {
    ListadoFotosCarpeta
  },
  props: {
    legajoId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const fotos = ref([]);
    const carpetas = ref({});
    const error = ref(null);
    const mostrarListadoFotosCarpeta = ref(false);
    const fechaSeleccionada = ref(null);

    const fetchFotos = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/muestras/fotos_por_legajo/${props.legajoId}`);
        console.log('Response data:', response.data); // Verificar la respuesta del backend
        fotos.value = response.data;
        agruparFotosPorFecha();
      } catch (err) {
        error.value = 'Error al cargar las fotos';
        console.error('Error fetching photos:', err);
      }
    };

    const agruparFotosPorFecha = () => {
      const agrupadas = fotos.value.reduce((acc, foto) => {
        const fecha = foto.fecha; // Usar la fecha directamente como cadena
        if (!acc[fecha]) {
          acc[fecha] = [];
        }
        acc[fecha].push(foto);
        return acc;
      }, {});
      carpetas.value = agrupadas;
    };

    const fechasOrdenadas = computed(() => {
      return Object.keys(carpetas.value).sort((a, b) => new Date(a) - new Date(b));
    });

    const formatFecha = (fecha) => {
      const [year, month, day] = fecha.split('-');
      return `${day}-${month}-${year}`;
    };

    const abrirCarpeta = (fecha) => {
      fechaSeleccionada.value = fecha;
      mostrarListadoFotosCarpeta.value = true;
    };

    const cerrarListadoFotosCarpeta = () => {
      mostrarListadoFotosCarpeta.value = false;
      fechaSeleccionada.value = null;
    };

    onMounted(() => {
      fetchFotos();
    });

    watch(() => props.legajoId, fetchFotos);

    return { carpetas, error, fechasOrdenadas, formatFecha, abrirCarpeta, cerrarListadoFotosCarpeta, mostrarListadoFotosCarpeta, fechaSeleccionada };
  }
};
</script>

<style scoped>
.card {
  background-color: #ffffb6;
  color: #646464;
  border: 1px solid #c1b69b;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
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
  text-align: center;
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
</style>