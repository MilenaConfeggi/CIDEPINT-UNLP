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
            @click.prevent="changeTab(tab.name)"
          >
            {{ tab.label }}
          </a>
        </li>
      </ul>
  
      <!-- Documentos -->
      <div v-if="documentos.length">
        <div
          v-for="(document, index) in documentos"
          :key="document.id"
          class="card mb-3 shadow-sm"
        >
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <h5 class="card-title mb-1">{{ document.tipo_documento.nombre }}</h5>
              <p class="card-text">Legajo: {{ document.legajo.nro_legajo }}</p>
              <p class="card-text">Cliente: {{ document.legajo.cliente.nombre }}</p>
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
      <p v-else class="text-center text-muted">No hay documentos disponibles.</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        tabs: [
          { name: "todos", label: "Todos los Documentos" },
        ],
        activeTab: "todos",
        documentos: [], // Almacena todos los documentos obtenidos de la API
      };
    },
    methods: {
      changeTab(tabName) {
        this.activeTab = tabName;
      },
      async fetchDocumentos() {
        try {
          const response = await axios.get(
            `${import.meta.env.VITE_API_URL}/api/documentos/list/2`
          );
          console.log("Documentos recibidos:", response.data); // <-- Inspecciona los datos aquí
          this.documentos = response.data;
        } catch (error) {
          console.error("Error al obtener los documentos:", error);
        }
      },
      firmarDocumento(index) {
        const doc = this.documentos[index];
        alert(`Documento firmado: ${doc.cliente}`);
      },
      async eliminarDocumento(id) {
        try {
          await axios.delete(`${import.meta.env.VITE_API_URL}/api/documentos/${id}`);
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
  