<script setup>
import { RouterLink, RouterView } from 'vue-router'
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

main {
  padding: 1rem;
}
</style>