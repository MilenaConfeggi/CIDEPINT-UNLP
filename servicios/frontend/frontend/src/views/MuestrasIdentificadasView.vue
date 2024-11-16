<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import ListadoMuestras from '../components/muestras/ListadoMuestras.vue';

const route = useRoute();
const legajoId = Number(route.params.legajoId);
</script>

<template>
  <main>
    <ListadoMuestras :legajo-id="legajoId" />
  </main>
</template>

<style scoped>
</style>