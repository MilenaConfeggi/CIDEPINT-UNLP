<template>
  <main>
    <button class="stans-button" @click="mostrarFormularioSubir">Cargar Stan</button>
    <ListadoStans />

    <!-- Modal de SubirStan -->
    <div v-if="mostrarSubirStan" class="modal-overlay" @click="cerrarFormularioSubir">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarFormularioSubir">&times;</button>
        <SubirStan />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import ListadoStans from '../components/stans/ListadoStans.vue';
import SubirStan from '../components/stans/SubirStan.vue';

const mostrarSubirStan = ref(false);

const mostrarFormularioSubir = () => {
  mostrarSubirStan.value = true;
};

const cerrarFormularioSubir = () => {
  mostrarSubirStan.value = false;
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
  margin-right: 10px; /* Añadir margen entre los botones */
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