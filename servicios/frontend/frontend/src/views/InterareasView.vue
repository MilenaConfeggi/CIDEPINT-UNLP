<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Interareas</h1>
    <button v-if="tienePermisoCargarInterarea" class="btn btn-success mb-4" @click="mostrarFormularioInterarea = true">Nueva Interarea</button>
    <div v-if="mostrarFormularioInterarea" class="modal-overlay" @click="cerrarFormularioInterarea">
      <div @click.stop>
        <button class="btn-close" aria-label="Cerrar" @click="cerrarFormularioInterarea"></button>
        <NuevaInterarea />
      </div>
    </div>
    <ListadoInterareas @interareasFetched="setInterareas" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import ListadoInterareas from '@/components/interareas/ListadoInterareas.vue';
import NuevaInterarea from '@/components/interareas/NuevaInterarea.vue';

const authStore = useAuthStore();
const router = useRouter();

const mostrarFormularioInterarea = ref(false);

const interareas = ref([]);

const permisos = JSON.parse(localStorage.getItem('permisos')) || [];

const cerrarFormularioInterarea = () => {
  mostrarFormularioInterarea.value = false;
};

const setInterareas = (data) => {
  interareas.value = data;
};

const tienePermisoCargarInterarea = computed(() => {
  return permisos.includes('cargar_interarea');
});

onMounted(() => {
  if (!authStore.getToken()) {
    router.push({ name: 'logIn' });
  }
});

</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; 
}

.modal-content .btn-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.modal-overlay .modal-content {
  transform: translateY(-50px);
  opacity: 0;
  animation: slideIn 0.3s forwards;
}

@keyframes slideIn {
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
