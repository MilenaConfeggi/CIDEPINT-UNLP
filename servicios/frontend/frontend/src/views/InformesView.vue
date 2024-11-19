<template>
    <div class="container mt-4">
      <h1 class="text-center mb-4">Vista de prueba para informes</h1>
      <button class="btn btn-primary" @click="mostrarFormularioSubir">Subir Documentación</button>
  
      <!-- Modal de SubirDocumentacion -->
      <div v-if="mostrarSubirDocumentacion" class="modal-overlay" @click="cerrarFormularioSubir">
        <div class="modal-content" @click.stop>
          <button class="close-button" @click="cerrarFormularioSubir">&times;</button>
          <SubirDocumentacion :legajo-id="legajoId" />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRoute } from 'vue-router';
  import SubirDocumentacion from '../components/informes/SubirDocumentacion.vue';
  
  const route = useRoute();
  const legajoId = Number(route.params.legajoId);
  
  // Propiedad reactiva para controlar la visibilidad de la ventana modal
  const mostrarSubirDocumentacion = ref(false);
  
  // Función para mostrar el modal
  const mostrarFormularioSubir = () => {
    mostrarSubirDocumentacion.value = true;
  };
  
  // Función para cerrar el modal
  const cerrarFormularioSubir = () => {
    mostrarSubirDocumentacion.value = false;
  };
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