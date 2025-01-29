<template>
  <div class="d-flex flex-column min-vh-100">
    <nav v-if="showNavbar" class="navbar">
      <RouterLink to="/" class="navbar-brand">
        <img alt="Vue logo" class="logo" src="@/assets/Logo.png" width="50" height="50" />
      </RouterLink>
      <button class="navbar-toggler" @click="toggleMenu">
        <i class="fas fa-bars"></i>
      </button>
      <div :class="['nav-links', { 'nav-links-mobile': isMenuOpen }]">
        <RouterLink to="/" class="nav-item">
          <i class="fas fa-home"></i> Home
        </RouterLink>
        <RouterLink v-if="estaLogueado" to="/ver_perfil" class="nav-item">
          <i class="fas fa-user"></i> Mi Perfil
        </RouterLink>
        <RouterLink v-if="estaLogueado && tienePermisoListarUsuarios" to="/usuarios" class="nav-item">
          <i class="fas fa-users"></i> Usuarios
        </RouterLink>
        <RouterLink v-if="estaLogueado && hasPermission('listar_legajos')" to="/legajos" class="nav-item">
          <i class="fas fa-folder"></i> Legajos
        </RouterLink>
        <RouterLink v-if="estaLogueado" to="/documentos" class="nav-item">
          <i class="fas fa-file-alt"></i> Documentos
        </RouterLink>
        <RouterLink v-if="estaLogueado && tienePermisoListarStans" to="/stans" class="nav-item">
            <i class="fas fa-list"></i> Stans
          </RouterLink>
          <RouterLink v-if="estaLogueado" to="/interareas" class="nav-item">
            <i class="fas fa-exchange-alt"></i> Interareas
          </RouterLink>
        <RouterLink v-if="estaLogueado && tienePermisoVerEstadisticas" to="/estadisticas" class="nav-item">
          <i class="fas fa-chart-bar"></i> Estadísticas
        </RouterLink>
        <RouterLink v-if="estaLogueado && tienePermisoPendientes" to="/pendientes" class="nav-item">
          <i class="fas fa-bell"></i> Pendientes
        </RouterLink>
        <RouterLink v-if="!estaLogueado" to="/log-in" class="nav-item">
          <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
        </RouterLink>
        <button v-if="estaLogueado" @click="logout" class="nav-item logout-button">
          <i class="fas fa-sign-out-alt"></i> Cerrar Sesión
        </button>
      </div>
    </nav>
    <main class="flex-grow-1">
      <RouterView />
    </main>
    <footer class="bg-light text-center border py-4 mt-auto">
      <div class="container">
        <div class="row">
          <div class="col d-flex justify-content-start">
            <a href="https://unlp.edu.ar/" target="_blank" rel="noopener noreferrer">
              <img alt="UNLP" src="@/assets/UNLP.png" class="img-fluid" width="150" height="150" />
            </a>
          </div>
          <div class="col d-flex justify-content-center">
            <a href="https://www.cic.gba.gob.ar/" target="_blank" rel="noopener noreferrer">
              <img alt="CIC" src="@/assets/CIC.png" class="img-fluid" width="150" height="150" />
            </a>
          </div>
          <div class="col d-flex justify-content-end">
            <a href="https://www.conicet.gov.ar/" target="_blank" rel="noopener noreferrer">
              <img alt="CONICET" src="@/assets/CONICET.png" class="img-fluid" width="150" height="150" style="margin-top: -10px;"/>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // Importa tu store de autenticación
import { ref, computed, watchEffect } from 'vue';

const authStore = useAuthStore();
const route = useRoute();

const token = ref(authStore.getToken() || localStorage.getItem('access_token'));
const permisos = ref(JSON.parse(localStorage.getItem('permisos')) || []);

const hasPermission = (permiso) => {
  return permisos.value.includes(permiso);
}

const tienePermisoListarStans = computed(() => {
  return permisos.value.includes('listar_stans');
});

const tienePermisoListarUsuarios = computed(() => {
  return permisos.value.includes('listar_usuarios');
});

const tienePermisoPendientes = computed(() => {
  return permisos.value.includes('ver_pendientes');
});

const tienePermisoVerEstadisticas = computed(() => {
  return permisos.value.includes('ver_estadisticas');
});

const estaLogueado = computed(() => {
  return !!token.value;
});

const showNavbar = computed(() => {
  return route.meta.showNavbar;
});

watchEffect(() => {
  permisos.value = JSON.parse(localStorage.getItem('permisos')) || [];
});

const logout = () => {
  authStore.removeToken();
  localStorage.removeItem('access_token');
  localStorage.removeItem('permisos');
  localStorage.removeItem('area');
  location.reload();
  console.log('Logout');
};

const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #962929;
  padding: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative; /* Asegura que el menú desplegable se posicione correctamente */
  z-index: 1000; /* Asegura que la navbar esté por encima de otros elementos */
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

.navbar-toggler {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-links-mobile {
  display: none;
  flex-direction: column; /* Cambia la dirección del flex a columna */
  gap: 0.5rem; /* Reduce el espacio entre los elementos */
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: #962929;
  padding: 0.5rem; /* Reduce el padding */
  z-index: 1001; /* Asegura que el menú desplegable esté por encima de otros elementos */
}

.nav-item {
  color: white;
  text-decoration: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0.5rem; /* Reduce el padding */
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-item:hover {
  background-color: #6c2222;
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
  padding: 0.5rem; /* Reduce el padding */
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.logout-button:hover {
  background-color: #6c2222;
  color: #f8f9fa;
}

.nav-links i {
  margin-right: 0.5rem;
}

main {
  padding: 1rem;
}

@media (max-width: 768px) {
  .navbar-toggler {
    display: block;
  }

  .nav-links {
    display: none;
  }

  .nav-links-mobile {
    display: flex;
  }
}
</style>