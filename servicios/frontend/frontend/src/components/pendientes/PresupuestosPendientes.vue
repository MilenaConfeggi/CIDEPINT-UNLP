<template>
    <div class="container my-5">
        <div class="row justify-content-center mb-4">
            <div class="col-md-6 text-center">
                <h2 class="pending-title">Presupuestos pendientes de firma</h2>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-lg-6 col-md-8">
                <div class="listado d-flex flex-column align-items-center">
                    <div v-if="paginatedPendientes.length === 0" class="text-muted text-center py-4">
                        <i class="bi bi-check-circle" style="font-size:2rem;"></i><br>
                        ¡No hay presupuestos pendientes de firma!
                    </div>
                    <div v-for="item in paginatedPendientes" :key="item.legajo_id" class="card mb-3 shadow-sm presupuesto-card w-100">
                        <div class="card-body text-center">
                            <h5 class="card-title mb-2">Legajo: <span class="fw-bold">{{ item.legajo_id }}</span></h5>
                            <p class="card-text mb-1"><b>Presupuestos subidos:</b> {{ item.presupuestos }}</p>
                            <p class="card-text mb-1"><b>Presupuestos firmados:</b> {{ item.presupuestosFirmados }}</p>
                            <p class="card-text text-danger mb-2">
                                <b>Faltan firmar {{ item.pendientes }} presupuesto(s)</b>
                            </p>
                            <RouterLink :to="`/legajos/${item.legajo_id}`" class="btn btn-success btn-sm">Ver</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Paginación -->
        <div class="row mt-3 justify-content-center">
            <div class="col-lg-6 col-md-8 text-center">
                <div class="pagination">
                    <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)" class="btn btn-primary btn-sm">
                        Anterior
                    </button>
                    <span>Página {{ currentPage }} de {{ totalPages }}</span>
                    <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)" class="btn btn-primary btn-sm">
                        Siguiente
                    </button>
                </div>
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
            pendientes: [],
            currentPage: 1,
            itemsPerPage: 5,
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.pendientes.length / this.itemsPerPage);
        },
        paginatedPendientes() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.pendientes.slice(start, end);
        },
    },
    methods: {
        async fetchPresupuestos() {
            const authStore = useAuthStore();
            const token = authStore.getToken();
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/list/2`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            // Agrupar por legajo y contar presupuestos y firmados
            const legajosMap = {};
            response.data.forEach((presupuesto) => {
                const legajoId = presupuesto.legajo_id;
                if (!legajosMap[legajoId]) {
                    legajosMap[legajoId] = {
                        legajo_id: legajoId,
                        presupuestos: 0,
                        presupuestosFirmados: 0,
                    };
                }
                // Estado 5: presupuesto subido, Estado 6: presupuesto firmado
                if (presupuesto.estado.id === 5) legajosMap[legajoId].presupuestos++;
                if (presupuesto.estado.id === 6) legajosMap[legajoId].presupuestosFirmados++;
            });

            // Solo mostrar legajos con pendientes de firma
            this.pendientes = Object.values(legajosMap)
                .map(l => ({
                    ...l,
                    pendientes: l.presupuestos - l.presupuestosFirmados
                }))
                .filter(l => l.pendientes > 0);
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
.pending-title {
    font-size: 1.3rem;
    font-weight: bold;
    color: #007bff;
    border-bottom: 2px solid #007bff;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    display: inline-block;
}
.presupuesto-card {
    border-radius: 10px;
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.card-body {
    padding: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.card-title {
    font-size: 1.15rem;
    font-weight: bold;
    color: #007bff;
}
.card-text {
    margin-bottom: 8px;
    color: #495057;
}
.btn-success {
    margin-top: 8px;
}
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    gap: 0.5rem;
}
.pagination button {
    min-width: 90px;
}
.text-danger {
    color: #dc3545 !important;
}
.text-muted {
    color: #6c757d !important;
}
</style>