<template>
  <div class="container my-5">
    <div v-if="interareas.length === 0" class="no-interareas text-center">
      <h3>No hay interáreas para mostrar</h3>
    </div>
    <div v-else>
      <h1 v-if="userRole.includes('cargar_interarea_firmada')" class="text-center">Interáreas por firmar</h1>
      <h1 v-else class="text-center">Interáreas por cargar</h1>
      <div v-for="interarea in paginatedInterareas" :key="interarea.id" class="card mb-3 shadow-sm interarea-card">
        <div class="card-body d-flex align-items-center">
          <div class="left-content me-auto">
            <h5 class="card-title mb-1">Interarea: {{ interarea.nro_interarea }}</h5>
            <p class="card-text">Fecha: {{ interarea.fecha_creacion }}</p>
            <p class="card-text">Área solicitante: {{ interarea.area_solicitante.nombre }}</p>
          </div>
          <div class="button-group">
            <RouterLink :to="`/interarea-detalle/${interarea.id}`" class="btn btn-success">Ver</RouterLink>
          </div>
        </div>
      </div>
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)" class="btn btn-primary">
          Anterior
        </button>
        <span>Página {{ currentPage }} de {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)" class="btn btn-primary">
          Siguiente
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export default {
  data() {
    return {
      interareas: [],
      userRole: JSON.parse(localStorage.getItem('permisos')) || [],
      area: JSON.parse(localStorage.getItem('area')) || 0,
      currentPage: 1,
      itemsPerPage: 5, 
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.interareas.length / this.itemsPerPage);
    },
    paginatedInterareas() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.interareas.slice(start, end);
    },
  },
  methods: {
    async fetchInterareas() {
      try {
        const authStore = useAuthStore();
        const token = authStore.getToken();
        const status = this.userRole.includes('cargar_interarea_firmada') ? 1 : 2;
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/interareas`,{
          headers: { Authorization : `Bearer ${token}` },
        });
        if (status === 1) {
          this.interareas = response.data.filter((interarea) => interarea.estadoInterarea_id === 1);
        } else {
          this.interareas = response.data.filter((interarea) => interarea.area_receptora.id === this.area && interarea.estadoInterarea_id === 2);
        }
      } catch (error) {
        console.error("Error al obtener las interareas:", error);
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
  mounted() {
    this.fetchInterareas();
  },
};
</script>

<style scoped>
.no-interareas {
  margin-top: 50px;
}

.interarea-card {
  border-radius: 10px;
  max-width: 600px;
  margin: 0 auto;
  height: 160px; 
  display: flex;
  flex-direction: column; 
  justify-content: space-between; 
}

.card-body {
  padding: 15px;
  display: flex;
  justify-content: space-between;
}

.left-content {
  text-align: left;
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
}

.card-text {
  margin-bottom: 10px;
}

.button-group {
  display: flex;
  align-items: center;
}

.btn-success {
  margin-right: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  margin: 0 10px;
}
</style>
