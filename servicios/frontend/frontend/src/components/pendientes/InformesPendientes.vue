<template>
    <div class="container my-5">
        <div class="row justify-content-center mb-4">
            <div class="col-md-4 text-center" v-if="userRole.includes('informes_pendientes_cargar')">
                <h2 class="pending-title">Pendientes por Subir</h2>
            </div>
            <div class="col-md-4 text-center" v-if="userRole.includes('crear_intearea')">
                <h2 class="pending-title">Pendientes por Firmar JA</h2>
            </div>
            <div class="col-md-4 text-center" v-if="userRole.includes('cambiar_jefe_area')">
                <h2 class="pending-title">Pendientes Firma Director</h2>
            </div>
        </div>
        <div class="row justify-content-center">
            <!-- Pendientes por subir (Secretaría) -->
            <div class="col-lg-4 col-md-6 mb-4" v-if="userRole.includes('informes_pendientes_cargar')">
                <div class="listado d-flex flex-column align-items-center">
                    <div v-if="paginatedFirmar.length === 0" class="text-muted text-center py-4">
                        <i class="bi bi-check-circle" style="font-size:2rem;"></i><br>
                        ¡No hay informes pendientes!
                    </div>
                    <div v-for="item in paginatedFirmar" :key="item.legajo_id" class="card mb-3 shadow-sm informe-card w-100">
                        <div class="card-body text-center">
                            <h5 class="card-title mb-2">Legajo: <span class="fw-bold">{{ item.legajo_id }}</span></h5>
                            <p class="card-text mb-1"><b>Cliente:</b> {{ item.legajo?.cliente?.contacto }}</p>
                            <p class="card-text mb-1"><b>Documentaciones:</b> {{ item.documentaciones }}</p>
                            <p class="card-text mb-1"><b>Informes:</b> {{ item.informes }}</p>
                            <p class="card-text text-danger mb-2">
                                <b>Faltan cargar {{ item.pendientes }} informe(s)</b>
                            </p>
                            <RouterLink :to="`/legajos/${item.legajo_id}`" class="btn btn-success btn-sm">Ver</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Pendientes por firmar JA -->
            <div class="col-lg-4 col-md-6 mb-4" v-if="userRole.includes('crear_intearea')">
                <div class="listado d-flex flex-column align-items-center">
                    <div v-if="paginatedCargar.length === 0" class="text-muted text-center py-4">
                        <i class="bi bi-check-circle" style="font-size:2rem;"></i><br>
                        ¡No hay informes pendientes!
                    </div>
                    <div v-for="item in paginatedCargar" :key="item.legajo_id" class="card mb-3 shadow-sm informe-card w-100">
                        <div class="card-body text-center">
                            <h5 class="card-title mb-2">Legajo: <span class="fw-bold">{{ item.legajo_id }}</span></h5>
                            <p class="card-text mb-1"><b>Cliente:</b> {{ item.legajo?.cliente?.contacto }}</p>
                            <p class="card-text mb-1"><b>Informes:</b> {{ item.informes }}</p>
                            <p class="card-text mb-1"><b>Firmados JA:</b> {{ item.informesFirmadosJA }}</p>
                            <p class="card-text text-danger mb-2">
                                <b>Faltan firmar {{ item.pendientes }} informe(s)</b>
                            </p>
                            <RouterLink :to="`/legajos/${item.legajo_id}`" class="btn btn-success btn-sm">Ver</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Pendientes por firmar Director -->
            <div class="col-lg-4 col-md-6 mb-4" v-if="userRole.includes('cambiar_jefe_area')">
                <div class="listado d-flex flex-column align-items-center">
                    <div v-if="paginatedDirector.length === 0" class="text-muted text-center py-4">
                        <i class="bi bi-check-circle" style="font-size:2rem;"></i><br>
                        ¡No hay informes pendientes!
                    </div>
                    <div v-for="item in paginatedDirector" :key="item.legajo_id" class="card mb-3 shadow-sm informe-card w-100">
                        <div class="card-body text-center">
                            <h5 class="card-title mb-2">Legajo: <span class="fw-bold">{{ item.legajo_id }}</span></h5>
                            <p class="card-text mb-1"><b>Cliente:</b> {{ item.legajo?.cliente?.contacto }}</p>
                            <p class="card-text mb-1"><b>Firmados JA:</b> {{ item.informesFirmadosJA }}</p>
                            <p class="card-text mb-1"><b>Firmados Director:</b> {{ item.informesFirmadosDirector }}</p>
                            <p class="card-text text-danger mb-2">
                                <b>Faltan firmar {{ item.pendientes }} informe(s)</b>
                            </p>
                            <RouterLink :to="`/legajos/${item.legajo_id}`" class="btn btn-success btn-sm">Ver</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Paginación -->
        <div class="row mt-3 justify-content-center">
            <div class="col-lg-4 col-md-6 text-center" v-if="userRole.includes('informes_pendientes_cargar')">
                <div class="pagination">
                    <button :disabled="currentFirmarPage === 1" @click="changeFirmarPage(currentFirmarPage - 1)" class="btn btn-primary btn-sm">
                        Anterior
                    </button>
                    <span>Página {{ currentFirmarPage }} de {{ totalFirmarPages }}</span>
                    <button :disabled="currentFirmarPage === totalFirmarPages" @click="changeFirmarPage(currentFirmarPage + 1)" class="btn btn-primary btn-sm">
                        Siguiente
                    </button>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 text-center" v-if="userRole.includes('crear_intearea')">
                <div class="pagination">
                    <button :disabled="currentCargarPage === 1" @click="changeCargarPage(currentCargarPage - 1)" class="btn btn-primary btn-sm">
                        Anterior
                    </button>
                    <span>Página {{ currentCargarPage }} de {{ totalCargarPages }}</span>
                    <button :disabled="currentCargarPage === totalCargarPages" @click="changeCargarPage(currentCargarPage + 1)" class="btn btn-primary btn-sm">
                        Siguiente
                    </button>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 text-center" v-if="userRole.includes('cambiar_jefe_area')">
                <div class="pagination">
                    <button :disabled="currentDirectorPage === 1" @click="changeDirectorPage(currentDirectorPage - 1)" class="btn btn-primary btn-sm">
                        Anterior
                    </button>
                    <span>Página {{ currentDirectorPage }} de {{ totalDirectorPages }}</span>
                    <button :disabled="currentDirectorPage === totalDirectorPages" @click="changeDirectorPage(currentDirectorPage + 1)" class="btn btn-primary btn-sm">
                        Siguiente
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { useAuthStore } from '../../stores/auth';
import { useRouter } from 'vue-router';

export default {
    data() {
        return {
            informes: [],
            informes_pendientes_cargar: [],
            informes_pendientes_director: [],
            userRole: JSON.parse(localStorage.getItem("permisos")) || [],
            area: JSON.parse(localStorage.getItem("area")) || 0,

            currentFirmarPage: 1,
            itemsPerPageFirmar: 1,

            currentCargarPage: 1,
            itemsPerPageCargar: 1,

            currentDirectorPage: 1,
            itemsPerPageDirector: 1,

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
        totalDirectorPages() {
            return Math.ceil(this.informes_pendientes_director.length / this.itemsPerPageDirector);
        },
        paginatedDirector() {
            const start = (this.currentDirectorPage - 1) * this.itemsPerPageDirector;
            return this.informes_pendientes_director.slice(start, start + this.itemsPerPageDirector);
        },
    },
    methods: {
        async fetchInformes() {
            const authStore = useAuthStore();
            const router = useRouter();
            this.loading = true;
            this.error = null;
            try {
                const token = authStore.getToken();
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/list/4`,{
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                if (response.status !== 200) {
                    throw ({message: 'Error al obtener los informes', status: response.status})
                }
                this.processInformes(response.data);
            } catch (error) {
                if (error.status === 401 || error.status === 422) {
                    authStore.logout()
                    router.push('/log-in')
                } else {
                    console.error("Error al obtener los informes:", error);
                    this.error = "No se pudieron cargar los informes. Intente nuevamente.";
                }
            } finally {
                this.loading = false;
            }
        },
        processInformes(data) {
            const legajosMap = {};

            data.forEach((doc) => {
                const legajoId = doc.legajo_id;
                if (!legajosMap[legajoId]) {
                    legajosMap[legajoId] = {
                        legajo: doc.legajo,
                        legajo_id: legajoId,
                        area_id: doc.legajo?.area_id, // <-- Asegúrate de tener el área
                        documentaciones: 0,
                        informes: 0,
                        informesFirmadosJA: 0,
                        informesFirmadosDirector: 0,
                    };
                }
                if (doc.estado.id === 8) legajosMap[legajoId].documentaciones++;
                if (doc.estado.id === 5) legajosMap[legajoId].informes++;
                if (doc.estado.id === 7) legajosMap[legajoId].informesFirmadosJA++;
                if (doc.estado.id === 6) legajosMap[legajoId].informesFirmadosDirector++;
            });

            // Secretaría: solo si hay documentaciones > informes
            this.informes = Object.values(legajosMap)
                .map(l => ({
                    ...l,
                    pendientes: l.documentaciones - l.informes
                }))
                .filter(l => l.pendientes > 0);

            // JA: solo si hay informes > firmados JA y el área coincide
            this.informes_pendientes_cargar = Object.values(legajosMap)
                .map(l => ({
                    ...l,
                    pendientes: l.informes - l.informesFirmadosJA
                }))
                .filter(l => l.pendientes > 0 && Number(l.area_id) === Number(this.area));
                console.log("legajosMap", legajosMap, "this.area", this.area);
            // Director: solo si hay firmados JA > firmados Director
            this.informes_pendientes_director = Object.values(legajosMap)
                .map(l => ({
                    ...l,
                    pendientes: l.informesFirmadosJA - l.informesFirmadosDirector
                }))
                .filter(l => l.pendientes > 0);
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
        changeDirectorPage(page) {
            if (page >= 1 && page <= this.totalDirectorPages) {
                this.currentDirectorPage = page;
            }
        },
    },
    mounted() {
        this.fetchInformes();
    },
};
</script>

<style scoped>
.container {
    max-width: 1200px;
}
.pending-title {
    font-size: 1.3rem;
    font-weight: bold;
    color: #007bff;
    border-bottom: 2px solid #007bff;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    display: inline-block;
}
.informe-card {
    border: 1px solid #dee2e6;
    border-radius: 10px;
    transition: all 0.3s ease-in-out;
    background: white;
}
.informe-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}
.btn-success {
    font-size: 0.9rem;
    padding: 0.4rem 1rem;
}
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
}
.pagination span {
    font-weight: bold;
    color: #495057;
}
.pagination .btn {
    padding: 0.3rem 1rem;
    font-size: 0.9rem;
}
.listado {
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.07);
    min-height: 200px;
}
.card-title {
    font-size: 1.1rem;
    font-weight: bold;
    color: #007bff;
}
.card-text {
    font-size: 0.95rem;
    color: #495057;
    margin-bottom: 0.3rem;
}
.text-danger {
    color: #dc3545 !important;
}
.text-muted {
    color: #6c757d !important;
}
</style>