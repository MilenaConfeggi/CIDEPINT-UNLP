<template>
  <main>
    <!-- Botón para cambiar la vista a MuestrasIdentificadasView -->
    <button class="muestras-button" @click="cambiarVistaMuestras">Ver Muestras</button>
    <button class="upload-button" @click="mostrarFormularioSubir">Subir Fotos</button>

    <ListadoCarpetas :legajo-id="legajoId" />

    <!-- Modal de SubirFotos -->
    <div v-if="mostrarSubirFotos" class="modal-overlay" @click="cerrarFormularioSubir">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarFormularioSubir">&times;</button>
        <SubirFotos :legajo-id="legajoId" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ListadoCarpetas from '../components/muestras/ListadoCarpetas.vue';
import SubirFotos from '../components/muestras/SubirFotos.vue';

const route = useRoute();
const router = useRouter();
const legajoId = Number(route.params.legajoId);

const mostrarSubirFotos = ref(false);

// Función para cambiar la vista a MuestrasIdentificadasView
const cambiarVistaMuestras = () => {
  router.push({ name: 'muestras', params: { legajoId } });
};

// Función para mostrar el modal de SubirFotos
const mostrarFormularioSubir = () => {
  mostrarSubirFotos.value = true;
};

// Función para cerrar el modal de SubirFotos
const cerrarFormularioSubir = () => {
  mostrarSubirFotos.value = false;
};
</script>

<style scoped>
main {
  padding: 20px;
}

.muestras-button {
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

.muestras-button:hover {
  background-color: #345a88; 
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
}

.upload-button:hover {
  background-color: #45a049;
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