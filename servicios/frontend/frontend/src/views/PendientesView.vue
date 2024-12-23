<template>
  <div class="app container my-5">
    <div class="nav-container">
      <nav class="nav">
        <button @click="currentSection = 'DocumentosPendientes'" :class="['nav-btn', currentSection === 'DocumentosPendientes' ? 'active' : '']">
          Presupuestos
        </button>
        <button @click="currentSection = 'InformesPendientes'" :class="['nav-btn', currentSection === 'InformesPendientes' ? 'active' : '']">
          Informes
        </button>
        <button @click="currentSection = 'InterareasPendientes'" :class="['nav-btn', currentSection === 'InterareasPendientes' ? 'active' : '']">
          Interareas
        </button>
      </nav>
    </div>
    <div>
      <DocumentosPendientes v-if="currentSection === 'DocumentosPendientes'" />
      <InterareasPendientes v-if="currentSection === 'InterareasPendientes'" />
    </div>
  </div>
</template>

<script>
import DocumentosPendientes from "@/components/pendientes/DocumentosPendientes.vue";
import InterareasPendientes from "@/components/pendientes/InterareasPendientes.vue";

export default {
  components: { DocumentosPendientes, InterareasPendientes },
  data() {
    return {
      currentSection: "DocumentosPendientes",
    };
  },
};
</script>

<style scoped>
.app {
  text-align: center;
}

.nav-container {
  border: 1px solid #ccc;
  border-radius: 5px;
  overflow: hidden;
  display: inline-block;
}

.nav {
  display: flex;
}

.nav-btn {
  flex: 1;
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  background-color: white;
  color: black;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.nav-btn:not(:last-child) {
  border-right: 1px solid #ccc;
}

.nav-btn.active {
  background-color: #007bff;
  color: white;
}

.nav-btn:hover:not(.active) {
  background-color: #f2f2f2;
}
</style>
