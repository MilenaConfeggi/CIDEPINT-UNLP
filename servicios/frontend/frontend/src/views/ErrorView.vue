<template>
    <div class="d-flex flex-column justify-content-center align-items-center vh-100 text-center">
        <h1 class="display-4 fw-bold">Error 404</h1>
        <p class="fs-5 mt-3">La página que buscas no existe.</p>
        <router-link to="/" class="btn btn-primary mt-4">
            Volver al inicio
        </router-link>
    </div>
</template>
  
<script>
  export default {
    name: 'ErrorView',
  };
</script>
  
 