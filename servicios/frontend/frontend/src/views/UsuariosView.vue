<template>
    <div>
        <right><button 
            @click="irACrearUsuario"
            class="stans-button right">
            Crear Usuario
        </button></right>
        <ListadoUsuarios />
    </div>
</template>
<script setup>
import ListadoUsuarios from '../components/usuarios/ListadoUsuarios.vue'
import { useRouter } from 'vue-router';

const router = useRouter();

const irACrearUsuario = () => {
  router.push({ name: 'usuarios_crear' });
};
</script>

<style>
.stans-button {
    background-color: #28a745;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }

</style>