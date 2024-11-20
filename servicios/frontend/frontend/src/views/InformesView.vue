<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Vista de prueba para informes</h1>
    <button class="btn btn-primary" @click="mostrarFormularioSubir">Subir Documentación</button>
    <button class="btn btn-secondary" @click="verDocumentacion">Ver Documentación</button>

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

// Propiedades reactivas para controlar la visibilidad de las ventanas modales
const mostrarSubirDocumentacion = ref(false);

// Función para mostrar el modal de subir documentación
const mostrarFormularioSubir = () => {
  mostrarSubirDocumentacion.value = true;
};

// Función para cerrar el modal de subir documentación
const cerrarFormularioSubir = () => {
  mostrarSubirDocumentacion.value = false;
};

// Función para abrir el documento en una nueva pestaña
const verDocumentacion = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/informes/ver_documento/${legajoId}`);
    if (!response.ok) {
      throw new Error('Error al obtener el documento');
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
  } catch (error) {
    console.error('Error al obtener el documento:', error);
  }
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