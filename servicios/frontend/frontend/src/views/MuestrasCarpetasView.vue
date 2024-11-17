<template>
  <main>
    <!-- Botón para cambiar la vista a MuestrasIdentificadasView -->
    <button class="muestras-button" @click="cambiarVistaMuestras">Ver Muestras</button>

    <ListadoCarpetas :legajo-id="legajoId" />
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ListadoCarpetas from '../components/muestras/ListadoCarpetas.vue';

const route = useRoute();
const router = useRouter();
const legajoId = Number(route.params.legajoId);

// Función para cambiar la vista a MuestrasIdentificadasView
const cambiarVistaMuestras = () => {
  router.push({ name: 'muestras', params: { legajoId } });
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
  margin-bottom: 20px; /* Añadir margen inferior para separar del contenido */
}

.muestras-button:hover {
  background-color: #345a88; 
}
</style>