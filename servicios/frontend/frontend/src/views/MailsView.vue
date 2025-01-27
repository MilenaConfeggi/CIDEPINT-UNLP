<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ListadoMails from '../components/mails/ListadoMails.vue';
import SubirMails from '../components/mails/SubirMails.vue';

const route = useRoute();
const router = useRouter();
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

// Función para ir hacia atrás
const irAtras = () => {
  router.back();
};
</script>

<template>
  <main>
    <!-- Botón para ir hacia atrás -->
    <button class="back-button" @click="irAtras">
      <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24">
        <g fill="none">
          <path
            d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"
          />
          <path
            fill="black"
            d="M3.283 10.94a1.5 1.5 0 0 0 0 2.12l5.656 5.658a1.5 1.5 0 1 0 2.122-2.122L7.965 13.5H19.5a1.5 1.5 0 0 0 0-3H7.965l3.096-3.096a1.5 1.5 0 1 0-2.122-2.121z"
          />
        </g>
      </svg>
    </button>

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
  margin-left: 10px; /* Añadir margen izquierdo para separar del botón de atrás */
}

.upload-button:hover {
  background-color: #45a049; /* Verde más oscuro al pasar el ratón */
}

/* Estilos para el botón de ir hacia atrás */
.back-button {
  display: inline-block;
  margin-bottom: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.back-button svg {
  fill: #000;
  transition: fill 0.3s ease;
}

.back-button:hover svg {
  fill: #007bff;
}
</style>