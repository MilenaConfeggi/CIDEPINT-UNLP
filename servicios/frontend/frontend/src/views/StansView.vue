<template>
    <main>
      <button class="stans-button" @click="cargarStan">Cargar Stan</button>
      <ListadoStans />
    </main>
  </template>
  
  <script setup>
  import ListadoStans from '../components/stans/ListadoStans.vue';
  
  const cargarStan = () => {
    // Por ahora no hace nada
    console.log('Cargar Stan');
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
  </style>