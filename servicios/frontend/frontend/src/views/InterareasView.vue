<template>
    <div class="container mt-4">
        <h1 class="text-center mb-4">Interareas</h1>
        <!-- Botón para mostrar el formulario en un modal -->
        <button class="btn btn-success" @click="mostrarFormularioInterarea = true">Nueva Interarea</button>
        
        <!-- Modal de Solicitar Interarea -->
        <div v-if="mostrarFormularioInterarea" class="modal-overlay" @click="cerrarFormularioInterarea">
            <div class="modal-content" @click.stop>
                <button class="close-button" @click="cerrarFormularioInterarea">&times;</button>
                <NuevaInterarea />
            </div>
        </div>

        <!-- Listado de interareas (esto se mantendrá visible debajo del modal) -->
        <ListadoInterareas @interareasFetched="setInterareas"/>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import ListadoInterareas from '@/components/interareas/ListadoInterareas.vue';
import NuevaInterarea from '@/components/interareas/NuevaInterarea.vue';

// Usamos ref para controlar el estado del modal
const mostrarFormularioInterarea = ref(false);

const interareas = ref([]);

// Método para cerrar el modal
const cerrarFormularioInterarea = () => {
    mostrarFormularioInterarea.value = false;
};

const setInterareas = (data) => {
    interareas.value = data;
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