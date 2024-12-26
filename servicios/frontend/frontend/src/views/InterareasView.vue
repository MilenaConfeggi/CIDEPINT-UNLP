<template>
  <div class="container mt-4">
    <ListadoInterareas @interareasFetched="setInterareas" />
    <div class="text-center mt-4">
      <button v-if="tienePermisoCargarInterarea" @click="redirigirANuevaInterarea" class="btn btn-success">Nueva Interarea</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import ListadoInterareas from '@/components/interareas/ListadoInterareas.vue';

const authStore = useAuthStore();
const router = useRouter();
const interareas = ref([]);
const permisos = JSON.parse(localStorage.getItem('permisos')) || [];

const setInterareas = (data) => {
  interareas.value = data;
};

const tienePermisoCargarInterarea = computed(() => {
  return permisos.includes('cargar_interarea');
});

const redirigirANuevaInterarea = () => {
  router.push({ name: 'NuevaInterarea' }); 
};

onMounted(() => {
  if (!authStore.getToken()) {
    router.push({ name: 'logIn' });
  }
});
</script>
