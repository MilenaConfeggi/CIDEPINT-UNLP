<template>
    <div class="container my-5">
        <!-- Títulos -->
        <div class="row">
            <div class="col-md-6">
                <h2 class="text-center">Informes Pendientes por Firmar</h2>
            </div>
            <div class="col-md-6" v-if="userRole.includes('informes_pendientes_cargar')">
                <h2 class="text-center">Informes Pendientes por Cargar</h2>
            </div>
        </div>
        <!-- Listados -->
        <div class="row">
            <!-- Informes por Firmar -->
            <div class="col-md-6">
                <div class="listado">
                    <div v-for="informe in paginatedFirmar" :key="informe.id" class="card mb-3 shadow-sm informe-card">
                        <div class="card-body">
                            <h5 class="card-title">Informe: {{ informe.nombre_documento }}</h5>
                            <p class="card-text">Fecha: {{ formatFecha(informe.fecha_creacion) }}</p>
                            <p class="card-text">Legajo: {{ informe.legajo_id }}</p>
                            <p class="card-text">Cliente: {{ informe.legajo.cliente.contacto }}</p>
                            <RouterLink :to="`/legajos/${informe.legajo_id}`" class="btn btn-success">Ver</RouterLink>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Informes por Cargar (condicional) -->
            <div class="col-md-6" v-if="userRole.includes('informes_pendientes_cargar')">
                <div class="listado">
                    <div v-for="informe in paginatedCargar" :key="informe.id" class="card mb-3 shadow-sm informe-card">
                        <div class="card-body">
                            <h5 class="card-title">Informe: {{ informe.nombre_documento }}</h5>
                            <p class="card-text">Fecha: {{ formatFecha(informe.fecha_creacion) }}</p>
                            <p class="card-text">Legajo: {{ informe.legajo_id }}</p>
                            <p class="card-text">Cliente: {{ informe.legajo.cliente.contacto }}</p>
                            <RouterLink :to="`/legajos/${informe.legajo_id}`" class="btn btn-success">Ver</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Paginación -->
        <div class="row mt-3">
            <!-- Paginación por Firmar -->
            <div class="col-md-6 text-center">
                <div class="pagination">
                    <button :disabled="currentFirmarPage === 1" @click="changeFirmarPage(currentFirmarPage - 1)" class="btn btn-primary">
                        Anterior
                    </button>
                    <span>Página {{ currentFirmarPage }} de {{ totalFirmarPages }}</span>
                    <button :disabled="currentFirmarPage === totalFirmarPages" @click="changeFirmarPage(currentFirmarPage + 1)" class="btn btn-primary">
                        Siguiente
                    </button>
                </div>
            </div>
            <!-- Paginación por Cargar (condicional) -->
            <div class="col-md-6 text-center" v-if="userRole.includes('informes_pendientes_cargar')">
                <div class="pagination">
                    <button :disabled="currentCargarPage === 1" @click="changeCargarPage(currentCargarPage - 1)" class="btn btn-primary">
                        Anterior
                    </button>
                    <span>Página {{ currentCargarPage }} de {{ totalCargarPages }}</span>
                    <button :disabled="currentCargarPage === totalCargarPages" @click="changeCargarPage(currentCargarPage + 1)" class="btn btn-primary">
                        Siguiente
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            informes: [],
            informes_pendientes_cargar: [],
            userRole: JSON.parse(localStorage.getItem("permisos")) || [],
            area: JSON.parse(localStorage.getItem("area")) || 0,

            // Paginación por Firmar
            currentFirmarPage: 1,
            itemsPerPageFirmar: 1,

            // Paginación por Cargar
            currentCargarPage: 1,
            itemsPerPageCargar: 1,

            loading: false,
            error: null,
        };
    },
    computed: {
        totalFirmarPages() {
            return Math.ceil(this.informes.length / this.itemsPerPageFirmar);
        },
        paginatedFirmar() {
            const start = (this.currentFirmarPage - 1) * this.itemsPerPageFirmar;
            return this.informes.slice(start, start + this.itemsPerPageFirmar);
        },
        totalCargarPages() {
            return Math.ceil(this.informes_pendientes_cargar.length / this.itemsPerPageCargar);
        },
        paginatedCargar() {
            const start = (this.currentCargarPage - 1) * this.itemsPerPageCargar;
            return this.informes_pendientes_cargar.slice(start, start + this.itemsPerPageCargar);
        },
    },
    methods: {
        async fetchInformes() {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/list/4`);
                this.processInformes(response.data);
            } catch (error) {
                console.error("Error al obtener los informes:", error);
                this.error = "No se pudieron cargar los informes. Intente nuevamente.";
            } finally {
                this.loading = false;
            }
        },
        processInformes(data) {
            if (this.area === 0 || this.userRole.includes("informes_pendientes_cargar")) {
                this.informes = data.filter((informe) => informe.estado.id === 7);
                this.informes_pendientes_cargar = data.filter((informe) => informe.estado.id === 8);
            } else {
                this.informes = data.filter((informe) => informe.estado.id === 5 && informe.area_id === this.area);
            }
        },
        formatFecha(fecha) {
            const date = new Date(fecha);
            return date.toISOString().split("T")[0];
        },
        changeFirmarPage(page) {
            if (page >= 1 && page <= this.totalFirmarPages) {
                this.currentFirmarPage = page;
            }
        },
        changeCargarPage(page) {
            if (page >= 1 && page <= this.totalCargarPages) {
                this.currentCargarPage = page;
            }
        },
    },
    mounted() {
        this.fetchInformes();
    },
};
</script>

<style scoped>
.informe-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.informe-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.card-title {
    font-size: 1.2rem;
    font-weight: bold;
}

.card-text {
    font-size: 0.9rem;
    color: #555;
}

.btn-success {
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
}

.pagination span {
    margin: 0 1rem;
    font-weight: bold;
}

.pagination .btn {
    margin: 0 0.5rem;
}

.text-center h2 {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
    border-bottom: 2px solid #007bff;
    padding-bottom: 0.5rem;
}

.listado {
    padding: 1rem;
    background: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

</style>