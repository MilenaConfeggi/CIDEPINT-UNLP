<template>
    <h2> <span :class="badgeClass">{{ stateLabel }}</span> </h2>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  
  // Props
  const {state} = defineProps({
    state: {
      type: String,
      required: true,
    },
  });
  
 
  // Computed properties
  const badgeClass = computed(() => {
    switch (state) {
      case 'En curso':
        return 'badge text-bg-success';
      case 'Cancelado':
        return 'badge text-bg-danger';
      case 'Inforamado':
        return 'badge text-bg-info';
      case 'Terminado':
        return 'badge text-bg-dark';
      default:
        return 'badge text-bg-secondary'; // Clase por defecto
    }
  });
  
  const stateLabel = computed(() => {
    const label = state
    return label ? label.charAt(0).toUpperCase() + label.slice(1) : 'Default';
  });
  </script>
  