<template>
    <div class="container my-5">
        <div v-if="interareas.length === 0" class="no-interareas text-center">
            <h3>No hay interareas para mostrar</h3>
        </div>
        <div v-else>
            <h1 v-if="userRole.includes('cargar_interarea_firmada')" class="text-center">Interáreas por firmar</h1>
            <h1 v-else class="text-center">Interáreas por cargar</h1>
            <div v-for="interarea in interareas" :key="interarea.id" class="card mb-3 shadow-sm">
                <div class="card-body">
                    <div>
                        <h5 class="card-title mb-1">Interarea: {{ interarea.nro_interarea }}</h5>
                        <p class="card-text">Fecha: {{ interarea.fecha_creacion }}</p>
                        <p class="card-text">Área solicitante: {{ interarea.area_solicitante.nombre }}</p>
                    </div>
                    <div class="button-group">
                        <RouterLink :to="`/interarea-detalle/${interarea.id}`" class="btn btn-success">Ver</RouterLink>
                        <button class="btn btn-danger">b</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        interareas: [],
        userRole: JSON.parse(localStorage.getItem('permisos')) || [],
        area: JSON.parse(localStorage.getItem('area')) || 0,
      };
    },
    methods: {
      async fetchInterareas() {
        try {
          const status = this.userRole.includes('cargar_interarea_firmada') ? 1 : 2;
          const response = await axios.get(`${import.meta.env.VITE_API_URL}/interareas`);
  
          if (status === 1) {
            this.interareas = response.data.filter((interarea) => interarea.estadoInterarea_id === 1);
          } else {
            this.interareas = response.data.filter((interarea) => interarea.area_receptora.id === this.area && interarea.estadoInterarea_id === 2);
          }
        } catch (error) {
          console.error("Error al obtener las interareas:", error);
        }
      },
    },
    mounted() {
      this.fetchInterareas();
    },
  };
  </script>
  
<style scoped>
h1 {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 20px;
    color: #343a40;
}

.no-interareas {
    margin-top: 50px;
}

.card {
    border-radius: 10px;
}

.card-body {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-title {
    font-size: 1.25rem;
    font-weight: bold;
    margin-bottom: 5px;
}

.card-text {
    margin-bottom: 5px;
    align-items: left;
}

.button-group {
    display: flex;
    gap: 10px;
}

.btn-success {
    margin-right: 10px;
}

.btn-danger {
    background-color: #dc3545;
    border-color: #dc3545;
}

.btn-danger:hover {
    background-color: #c82333;
    border-color: #bd2130;
}
</style>
  