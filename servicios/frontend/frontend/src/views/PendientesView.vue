<template>
  <div class="app">
    <div>
      <DocumentosPendientes v-if="currentSection === 'DocumentosPendientes'" />
      <InterareasPendientes v-if="currentSection === 'InterareasPendientes'" />
    </div>
    <nav>
      <button @click="currentSection = 'DocumentosPendientes'">Presupuestos</button>
      <button @click="currentSection = 'InterareasPendientes'">Interareas</button>
    </nav>
  </div>
</template>

<script>
import DocumentosPendientes from "@/components/pendientes/DocumentosPendientes.vue";
import InterareasPendientes from "@/components/pendientes/InterareasPendientes.vue";

export default {
  components: { DocumentosPendientes, InterareasPendientes },
  data() {
    return {
      currentSection: "DocumentosPendientes",  // Cambié aquí a DocumentosPendientes para hacer que la sección inicial se muestre correctamente
    };
  },
};
</script>

<style scoped>
.app {
  text-align: center;
  font-family: Arial, sans-serif;
}

nav button {
  margin: 0 10px;
  padding: 10px 20px;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  cursor: pointer;
}

nav button:hover {
  background-color: #dcdcdc;
}

h1 {
  margin-bottom: 20px;
}
</style>
