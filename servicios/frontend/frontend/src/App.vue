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
      <RouterLink to="/">
        <img alt="Vue logo" class="logo" src="@/assets/Logo.png" width="50" height="50" />
      </RouterLink>
      <div class="nav-links">
        <RouterLink to="/legajos">Legajos</RouterLink>
        <RouterLink to="/documentos">Documentos</RouterLink>
        <RouterLink to="/stans">Stans</RouterLink>
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
