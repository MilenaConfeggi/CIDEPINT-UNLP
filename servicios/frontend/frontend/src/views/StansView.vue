<template>
  <main>
    <!-- Mostrar el botón solo si el usuario tiene el permiso "cargar_stan" -->
    <button v-if="tienePermisoCargarStan" class="stans-button" @click="mostrarFormularioSubir">Cargar STAN</button>
    <ListadoStans @modificar-stan="mostrarFormularioModificar" />

    <!-- Modal de SubirStan -->
    <div v-if="mostrarSubirStan" class="modal-overlay" @click="cerrarFormularioSubir">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarFormularioSubir">&times;</button>
        <SubirStan />
      </div>
    </div>

    <!-- Modal de ModificarStan -->
    <div v-if="mostrarModificarStan" class="modal-overlay" @click="cerrarFormularioModificar">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarFormularioModificar">&times;</button>
        <ModificarStan :id="stanId" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore();
const router = useRouter();

// Verificación del token al montar el componente
onMounted(() => {
  if (!authStore.getToken()) {
    router.push({ name: 'logIn' });
  }
});

// Recuperar los permisos desde localStorage (o Vuex)
const permisos = JSON.parse(localStorage.getItem('permisos')) || [];

// Computada para verificar si el usuario tiene el permiso "cargar_stan"
const tienePermisoCargarStan = computed(() => {
  return permisos.includes('cargar_stan');
});

import ListadoStans from '../components/stans/ListadoStans.vue';
import SubirStan from '../components/stans/SubirStan.vue';
import ModificarStan from '../components/stans/ModificarStan.vue';

const mostrarSubirStan = ref(false);
const mostrarModificarStan = ref(false);
const stanId = ref(null);

const mostrarFormularioSubir = () => {
  mostrarSubirStan.value = true;
};

const cerrarFormularioSubir = () => {
  mostrarSubirStan.value = false;
};

const mostrarFormularioModificar = (id) => {
  stanId.value = id;
  mostrarModificarStan.value = true;
};

const cerrarFormularioModificar = () => {
  mostrarModificarStan.value = false;
};
</script>

<style scoped>
main {
  padding: 20px;
}

.stans-button {
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.stans-button:hover {
  background-color: #218838;
}

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

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
</style>
