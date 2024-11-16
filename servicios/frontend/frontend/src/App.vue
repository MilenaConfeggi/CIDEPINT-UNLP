<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div>
    <nav class="navbar">
      <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="50" height="50" />
      <div class="nav-links">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/mails">Mails</RouterLink>
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
}

.nav-links a:hover {
  text-decoration: underline;
}

main {
  padding: 1rem;
}
</style>
