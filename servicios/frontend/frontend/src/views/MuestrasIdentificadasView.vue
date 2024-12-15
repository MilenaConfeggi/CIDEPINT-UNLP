<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import ListadoMuestras from '../components/muestras/ListadoMuestras.vue';
import IdentificarMuestras from '../components/muestras/IdentificarMuestras.vue';

const route = useRoute();
const router = useRouter();
const legajoId = Number(route.params.legajoId);

const permisos = JSON.parse(localStorage.getItem('permisos')) || [];

const tienePermisoCargar = computed(() => {
  return permisos.includes('cargar_muestra');
});

// Propiedad reactiva para controlar la visibilidad de la ventana modal
const mostrarIdentificarMuestras = ref(false);

// Función para mostrar el modal
const mostrarFormularioIdentificar = () => {
  mostrarIdentificarMuestras.value = true;
};

// Función para cerrar el modal
const cerrarFormularioIdentificar = () => {
  mostrarIdentificarMuestras.value = false;
};

// Función para cambiar la vista a MuestrasCarpetasView
const cambiarVistaCarpetas = () => {
  router.push({ name: 'muestrasCarpetas', params: { legajoId } });
};
</script>

<template>
  <main>
    <!-- Botón para cambiar la vista a MuestrasCarpetasView -->
    <button class="carpetas-button" @click="cambiarVistaCarpetas">Ver Carpetas</button>
    <!-- Botón para mostrar la ventana modal -->
    <button v-if="tienePermisoCargar" class="upload-button" @click="mostrarFormularioIdentificar">Identificar muestra</button>


    <!-- ListadoMuestras siempre visible -->
    <ListadoMuestras :legajo-id="legajoId" />

    <!-- Modal de IdentificarMuestras -->
    <div v-if="mostrarIdentificarMuestras" class="modal-overlay" @click="cerrarFormularioIdentificar">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarFormularioIdentificar">&times;</button>
        <IdentificarMuestras :legajo-id="legajoId" />
      </div>
    </div>
  </main>
</template>

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

.upload-button {
  background-color: #4CAF50; 
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
  margin-right: 10px; /* Añadir margen entre los botones */
}
.carpetas-button {
  background-color: #4caaaf; 
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
  margin-right: 10px; /* Añadir margen entre los botones */
}

.upload-button:hover {
  background-color: #45a049; 
}

.carpetas-button:hover {
  background-color: #345a88; 
}
</style>