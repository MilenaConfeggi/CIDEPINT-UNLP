<template>
  <div>
    <button @click="mostrarFormularioCrear" class="stans-button">Crear Usuario</button>
    <button @click="mostrarJefeArea" class="stans-button">Cambiar Jefe de Área</button>
    <ListadoUsuarios />

    <!-- Modal de CrearUsuario -->
    <div v-if="mostrarCrearUsuario" class="modal-overlay" @click="cerrarFormularioCrear">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarFormularioCrear">&times;</button>
        <CrearUsuario />
      </div>
    </div>
    <div v-if="mostrarCambiarJefe" class="modal-overlay" @click="cerrarJefeArea">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarJefeArea">&times;</button>
        <CambiarJefeArea />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ListadoUsuarios from '../components/usuarios/ListadoUsuarios.vue';
import CrearUsuario from '../components/usuarios/CrearUsuario.vue';
import CambiarJefeArea from '../components/areas/CambiarJefeArea.vue';

const mostrarCrearUsuario = ref(false);

const mostrarFormularioCrear = () => {
  mostrarCrearUsuario.value = true;
};

const cerrarFormularioCrear = () => {
  mostrarCrearUsuario.value = false;
};

const mostrarCambiarJefe = ref(false);

const mostrarJefeArea = () => {
  mostrarCambiarJefe.value = true;
};

const cerrarJefeArea = () => {
  mostrarCambiarJefe.value = false;
};
</script>

<style scoped>
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
  max-width: 600px;
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