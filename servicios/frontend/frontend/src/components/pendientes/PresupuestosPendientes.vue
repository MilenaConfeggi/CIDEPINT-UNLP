<template>
    <div class="container my-5">
        <div v-if="presupuestos.length === 0" class="text-center">
            <h3>No hay presupuestos para firmar</h3>
        </div>
        <div v-else>
            <h2 class="text-center mb-4">Presupuestos por firmar</h2>
            <div v-for="presupuesto in paginatedPresupuestos" :key="presupuesto.id" class="card mb-3 shadow-sm presupuesto-card">
                <div class="card-body d-flex align-items-center">
                    <div class="left-content me-auto">
                        <h5 class="card-title mb-1">{{ presupuesto.tipo_documento.nombre }} {{ presupuesto.nombre_documento }}</h5>
                        <p class="card-text">Fecha: {{ formatFecha(presupuesto.fecha_creacion) }}</p>
                        <p class="card-text">Legajo: {{ presupuesto.legajo_id }}</p>
                    </div>
                    <div class="button-group">
                        <RouterLink :to="`/legajos/${presupuesto.legajo_id}`" class="btn btn-success">Ver</RouterLink>
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
import { useAuthStore } from '../../stores/auth';
  
export default {
    data() {
        return {
            presupuestos: [],
            currentPage: 1,
            itemsPerPage: 5,
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.presupuestos.length / this.itemsPerPage);
        },
        paginatedPresupuestos() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.presupuestos.slice(start, end);
        },
    },
    methods: {
        async fetchPresupuestos() {

        const authStore = useAuthStore();
        const token = authStore.getToken();
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/list/2`,{
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            this.presupuestos = response.data.filter(presupuesto => presupuesto.estado.id === 5);
        },
        formatFecha(fecha) {
            const date = new Date(fecha);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },
    },
    mounted() {
        this.fetchPresupuestos();
    },
  };
</script>
  
<style scoped>
.presupuesto-card {
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
  