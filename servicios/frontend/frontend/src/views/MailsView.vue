<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import ListadoMails from '../components/mails/ListadoMails.vue';
import SubirMails from '../components/mails/SubirMails.vue';

const route = useRoute();
const legajoId = Number(route.params.legajoId);

// Propiedad reactiva para controlar la visibilidad de la ventana modal
const mostrarSubirMails = ref(false);

// Función para mostrar el modal
const mostrarFormularioSubir = () => {
  mostrarSubirMails.value = true;
};

// Función para cerrar el modal
const cerrarFormularioSubir = () => {
  mostrarSubirMails.value = false;
};
</script>

<template>
  <main>
    <!-- Botón para mostrar la ventana modal -->
    <button class="upload-button" @click="mostrarFormularioSubir">Subir imagen</button>

    <!-- ListadoMails siempre visible -->
    <ListadoMails :legajo-id="legajoId" />

    <!-- Modal de SubirMails -->
    <div v-if="mostrarSubirMails" class="modal-overlay" @click="cerrarFormularioSubir">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarFormularioSubir">&times;</button>
        <SubirMails :legajo-id="legajoId" />
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

/* Estilos para el botón de subir imagen */
.upload-button {
  background-color: #4CAF50; /* Verde */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.upload-button:hover {
  background-color: #45a049; /* Verde más oscuro al pasar el ratón */
}
</style>
