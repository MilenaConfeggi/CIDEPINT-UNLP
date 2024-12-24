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
      <RouterLink to="/" class="navbar-brand">
        <img alt="Vue logo" class="logo" src="@/assets/Logo.png" width="50" height="50" />
      </RouterLink>
      <div class="nav-links">
        <RouterLink to="/" class="nav-item">
          <i class="fas fa-home"></i> Home
        </RouterLink>
        <RouterLink v-if="estaLogueado" to="/ver_perfil" class="nav-item">
          <i class="fas fa-user"></i> Mi Perfil
        </RouterLink>
        <RouterLink v-if="estaLogueado && tienePermisoListarUsuarios" to="/usuarios" class="nav-item">
          <i class="fas fa-users"></i> Usuarios
        </RouterLink>
        <RouterLink v-if="estaLogueado" to="/legajos" class="nav-item">
          <i class="fas fa-folder"></i> Legajos
        </RouterLink>
        <RouterLink v-if="estaLogueado" to="/documentos" class="nav-item">
          <i class="fas fa-file-alt"></i> Documentos
        </RouterLink>
        <RouterLink v-if="estaLogueado && tienePermisoListarStans" to="/stans" class="nav-item">
          <i class="fas fa-list"></i> Stans
        </RouterLink>
        <RouterLink v-if="estaLogueado" to="/estadisticas" class="nav-item">
          <i class="fas fa-chart-bar"></i> Estadísticas
        </RouterLink>
        <RouterLink v-if="estaLogueado" to="/pendientes" class="nav-item">
          <i class="fas fa-bell"></i> Pendientes
        </RouterLink>
        <RouterLink v-if="estaLogueado" to="/jefe_de_area" class="nav-item">
          <i class="fas fa-users"></i> Cambiar Jefe de Area
        </RouterLink>
        <RouterLink v-if="!estaLogueado" to="/log-in" class="nav-item">
          <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
        </RouterLink>
        <button v-if="estaLogueado" @click="logout" class="nav-item logout-button">
          <i class="fas fa-sign-out-alt"></i> Cerrar Sesión
        </button>
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
  justify-content: space-between;
  background-color: #962929;
  padding: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
}

.logo {
  margin-right: 1rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-item {
  color: white;
  text-decoration: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-item:hover {
  background-color: #391111;
  color: #f8f9fa;
}

.logout-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  text-decoration: none;
  font-size: 1rem;
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.logout-button:hover {
  background-color: #3d1313;
  color: #f8f9fa;
}

.nav-links i {
  margin-right: 0.5rem;
}

main {
  padding: 1rem;
}
</style>