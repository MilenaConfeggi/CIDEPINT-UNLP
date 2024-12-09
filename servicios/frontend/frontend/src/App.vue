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

// Computada para verificar si el usuario está logueado
const estaLogueado = computed(() => {
  return !!token.value; // Si el token existe, significa que el usuario está logueado
});

// WatchEffect para actualizar los permisos cuando cambien en localStorage
watchEffect(() => {
  permisos.value = JSON.parse(localStorage.getItem('permisos')) || [];
});

const logout = () => {
  authStore.removeToken();
  localStorage.removeItem('permisos');
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
        <RouterLink to="/legajos">Legajos</RouterLink>
        <RouterLink to="/documentos">Documentos</RouterLink>
        
        <!-- Mostrar el botón de Stans solo si el usuario está logueado y tiene el permiso "listar_stans" -->
        <RouterLink v-if="estaLogueado && tienePermisoListarStans" to="/stans">Stans</RouterLink>
        
        <button @click="logout">Logout</button>
        <RouterLink to="/log-in">Login</RouterLink>
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