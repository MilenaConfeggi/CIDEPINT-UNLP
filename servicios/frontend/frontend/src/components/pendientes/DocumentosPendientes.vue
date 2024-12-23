<template>
    <div class="container my-5">
        <div v-if="informes.length > 0">
            <h1 class="text-center">Informes pendientes</h1>
            <div v-for="informe in informes" :key="informe.id" class="card mb-3 shadow-sm informe-card">
                <div class="card-body d-flex align-items-center">
                    <div class="left-content me-auto">
                        <h5 class="card-title mb-1">Informe: {{ informe.nombre_documento }}</h5>
                        <p class="card-text">Fecha: {{ formatFecha(informe.fecha_creacion) }}</p>
                        <p class="card-text">Legajo: {{ informe.legajo_id }}</p>
                        <p class="card-text">Cliente: {{ informe.legajo.cliente.contacto }}</p>
                    </div>
                    <div class="button-group">
                        <RouterLink :to="`/legajos/${informe.legajo_id}`" class="btn btn-success">Ver</RouterLink>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <h1 class="text-center">No hay informes pendientes</h1>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            informes: [],
            userRole: JSON.parse(localStorage.getItem('permisos')) || [],
            area: JSON.parse(localStorage.getItem('area')) || 0,
        };
    },
    methods: {
        async fetchInformes() {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/list/4`);
                if (this.userRole.includes('cargar_informe_firmado')) {
                    this.informes = response.data.filter(informe => informe.estado.id === 5);
                }
            } catch (error) {
                console.error("Error al obtener los informes:", error);
            }
        },
        formatFecha(fecha) {
            const date = new Date(fecha);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
    },
    mounted() {
        this.fetchInformes();
    },
};
</script>

<style scoped>
.informe-card{
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
</style>
