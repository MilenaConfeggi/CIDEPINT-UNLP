<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // Importa tu store de autenticación
import { ref, computed, watchEffect } from 'vue';

const authStore = useAuthStore();

// Recuperar el token desde el store o localStorage
const token = ref(authStore.getToken() || localStorage.getItem('access_token'));

// Recuperar los permisos desde localStorage
const permisos = ref(JSON.parse(localStorage.getItem('permisos')) || []);

// Computada para verificar si el usuario tiene el permiso "listar_stans"
const tienePermisoListarStans = computed(() => {
  return permisos.value.includes('listar_stans');
});

// Computada para verificar si el usuario tiene el permiso "listar_usuarios"
const tienePermisoListarUsuarios = computed(() => {
  return permisos.value.includes('listar_usuarios');
});

// Computada para verificar si el usuario está logueado
const estaLogueado = computed(() => {
  console.log(token.value);
  return !!token.value; // Si el token existe, significa que el usuario está logueado
});

// WatchEffect para actualizar los permisos cuando cambien en localStorage
watchEffect(() => {
  permisos.value = JSON.parse(localStorage.getItem('permisos')) || [];
});

const logout = () => {
  authStore.removeToken();
  localStorage.removeItem('access_token'); // Remove the token from localStorage
  localStorage.removeItem('permisos');
  localStorage.removeItem('area');
  location.reload(); // Recarga la página para que se aplique el guard
  console.log('Logout');
};
</script>

<template>
  <div>
    <nav class="navbar">
      <RouterLink to="/">
        <img alt="Vue logo" class="logo" src="@/assets/Logo.png" width="50" height="50" />
      </RouterLink>
      <div class="nav-links">
        <RouterLink v-if="estaLogueado" to="/ver_perfil">Mi Perfil</RouterLink>
        <RouterLink v-if="estaLogueado" to="/estadisticas">Estadísticas</RouterLink>
        <RouterLink v-if="estaLogueado" to="/legajos">Legajos</RouterLink>
        <RouterLink v-if="estaLogueado" to="/documentos">Documentos</RouterLink>
        <RouterLink v-if="estaLogueado" to="/pendientes">Pendientes</RouterLink>
        <RouterLink v-if="estaLogueado && tienePermisoListarStans" to="/stans">Stans</RouterLink>

        <RouterLink v-if="estaLogueado && tienePermisoListarUsuarios" to="/usuarios">Usuarios</RouterLink>
        
        <RouterLink v-if="!estaLogueado" to="/log-in">Iniciar Sesión</RouterLink>
        <button v-if="estaLogueado" @click="logout">Cerrar Sesión</button>
      </div>
    </nav>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  background-color: darkred;
  padding: 1rem;
}

.logo {
  margin-right: 1rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  cursor: pointer;
}

.nav-links a:hover {
  text-decoration: underline;
}

.nav-links button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  text-decoration: none;
  font-size: 1rem;
}

.nav-links button:hover {
  text-decoration: underline;
}

main {
  padding: 1rem;
}
</style>