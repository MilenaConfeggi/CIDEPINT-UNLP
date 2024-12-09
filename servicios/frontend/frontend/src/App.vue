<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // Importa tu store de autenticación

const authStore = useAuthStore();

const logout = () => {
  authStore.removeToken();
  location.reload(); // Recarga la página para que se aplique el guard
};
</script>

<template>
  <div>
    <nav class="navbar">
      <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="50" height="50" />
      <div class="nav-links">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/mails/1">Mails</RouterLink>
        <RouterLink to="/muestras/1">Muestras</RouterLink> 
        <RouterLink to="/informes/1">Informes</RouterLink>
        <RouterLink to="/stans">Stans</RouterLink>
        <button @click="logout">Logout</button> <!-- Botón de logout -->
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
  background-color: #333;
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
