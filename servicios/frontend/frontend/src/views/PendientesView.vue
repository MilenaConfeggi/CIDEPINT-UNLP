<template>
  <div class="app container my-5">
    <div class="nav-container">
      <nav class="nav">
        <button v-if="permisos.includes('ver_presupuesto_pendiente')" @click="currentSection = 'PresupuestosPendientes'" :class="['nav-btn', currentSection === 'PresupuestosPendientes' ? 'active' : '']">
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
      <PresupuestosPendientes
        v-if="currentSection === 'PresupuestosPendientes' && permisos.includes('ver_presupuesto_pendiente')"
      />
      <InformesPendientes v-if="currentSection === 'InformesPendientes'" />
      <InterareasPendientes v-if="currentSection === 'InterareasPendientes'" />
    </div>
  </div>
</template>

<script>
import InformesPendientes from "@/components/pendientes/InformesPendientes.vue";
import InterareasPendientes from "@/components/pendientes/InterareasPendientes.vue";
import PresupuestosPendientes from "@/components/pendientes/PresupuestosPendientes.vue";

export default {
  components: { InformesPendientes, InterareasPendientes, PresupuestosPendientes },
  data() {
    return {
      permisos: JSON.parse(localStorage.getItem("permisos")) || [],
      currentSection: null,
    };
  },
  created() {
    if (this.permisos.includes("ver_presupuesto_pendiente")) {
      this.currentSection = "PresupuestosPendientes";
    } else {
      this.currentSection = "InformesPendientes";
    }
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
