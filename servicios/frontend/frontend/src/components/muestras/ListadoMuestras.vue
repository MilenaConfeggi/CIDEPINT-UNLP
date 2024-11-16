<template>
    <div class="container mt-4">
      <h1 class="text-center mb-4">Muestras para el legajo {{ legajoId }}</h1>
      <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
      <div v-if="muestras.length" class="row">
        <div v-for="muestra in muestras" :key="muestra.id" class="col-md-3 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Número de muestra: {{ muestra.nro_muestra }}</h5>
              <p class="card-text">Cliente: {{ muestra.iden_cliente }}</p>
              <p class="card-text">Fecha de ingreso: {{ muestra.fecha_ingreso }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center">
        <p class="text-muted">No hay muestras disponibles.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { useMuestrasStore } from '@/stores/muestras';
  import { storeToRefs } from 'pinia';
  import { onMounted, watch } from 'vue';
  
  export default {
    props: {
      legajoId: {
        type: Number,
        required: true
      }
    },
    setup(props) {
      const store = useMuestrasStore();
      const { muestras, error } = storeToRefs(store);
  
      const fetchMuestras = async () => {
        await store.fetchMuestras(props.legajoId);
      };
  
      onMounted(() => {
        fetchMuestras();
      });
  
      watch(() => props.legajoId, fetchMuestras);
  
      return { muestras, error };
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
  </style>