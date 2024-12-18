<template>
    <div class="container mt-4">
        <h1 class="text-center mb-4">Documentos por firmar</h1>

        <!-- Tabs -->
        <ul class="nav nav-pills mb-4 justify-content-center">
        <li class="nav-item" v-for="tab in tabs" :key="tab.name">
            <a
            class="nav-link"
            :class="{ active: activeTab === tab.name }"
            href="#"
            @click="changeTab(tab.name)"
            >
            {{ tab.label }}
            </a>
        </li>
        </ul>

        <!-- Documentos -->
        <div v-if="filteredDocuments.length">
        <div
            v-for="(document, index) in filteredDocuments"
            :key="document.id"
            class="card mb-3 shadow-sm"
        >
            <div class="card-body d-flex justify-content-between align-items-center">
            <div>
                <h5 class="card-title mb-1">{{ tabTitles[activeTab] }}</h5>
                <p class="card-text">Cliente: {{ document.cliente }}</p>
            </div>
            <div>
                <button class="btn btn-success me-2" @click="firmarDocumento(index)">
                Firmar
                </button>
                <button class="btn btn-danger" @click="eliminarDocumento(document.id)">
                Eliminar
                </button>
            </div>
            </div>
        </div>
        </div>
        <p v-else class="text-center text-muted">No hay documentos en esta sección.</p>
    </div>
</template>
  
<script>
import axios from "axios";

export default {
data() {
    return {
    tabs: [
        { name: "presupuestos", label: "Presupuestos" },
        { name: "informes", label: "Informes" },
        { name: "interareas", label: "Interareas" },
    ],
    activeTab: "presupuestos",
    documentos: [], // Array general que guarda todos los documentos

    tabTitles: {
        presupuestos: "Presupuesto CIDEPINT",
        informes: "Informe CIDEPINT",
        interareas: "Documento Interáreas",
    },
    };
},
computed: {
    filteredDocuments() {
    // Filtrar documentos según la pestaña activa
    return this.documentos.filter(
        (doc) => doc.tipo === this.activeTab
    );
    },
},
methods: {
    changeTab(tabName) {
    this.activeTab = tabName;
    },
    async fetchDocumentos() {
    try {
        const response = await axios.get("api/documentos/");
        this.documentos = response.data; // Almacenar los documentos obtenidos
    } catch (error) {
        console.error("Error al obtener los documentos:", error);
    }
    },
    firmarDocumento(index) {
    const doc = this.filteredDocuments[index];
    alert(`Documento firmado: ${doc.cliente}`);
    // Aquí puedes agregar lógica para actualizar el documento como "firmado"
    },
    async eliminarDocumento(id) {
    try {
        // Simulamos un DELETE a la API
        await axios.delete(`api/documentos/${id}/`);
        this.documentos = this.documentos.filter((doc) => doc.id !== id);
    } catch (error) {
        console.error("Error al eliminar el documento:", error);
    }
    },
},
mounted() {
    this.fetchDocumentos();
},
};
</script>

<style scoped>
.container {
max-width: 900px;
}
.nav-pills .nav-link {
cursor: pointer;
}
.card {
border: 1px solid #ddd;
}
</style>
  