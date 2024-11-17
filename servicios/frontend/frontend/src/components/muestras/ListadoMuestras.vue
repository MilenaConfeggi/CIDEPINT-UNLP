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
            <button @click="mostrarFotos(muestra.id)" class="btn btn-primary">Ver fotos</button>
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
import { ref, onMounted, watch } from 'vue';
import { useMuestrasStore } from '@/stores/muestras';
import { storeToRefs } from 'pinia';
import ListadoFotosIden from './ListadoFotosIden.vue';

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

    onMounted(() => {
      fetchMuestras();
    });

    watch(() => props.legajoId, fetchMuestras);

    return { muestras, error, mostrarFotos, cerrarListadoFotos, mostrarListadoFotos, muestraSeleccionada };
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
</style>