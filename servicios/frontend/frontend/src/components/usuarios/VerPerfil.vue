<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        <i class="fas fa-user-circle user-icon"></i>
        <h2>Mi Perfil</h2>
      </div>
      <div v-if="loading" class="loading-spinner"></div>
      <div v-else class="profile-info">
        <p><strong>Nombre:</strong> {{ nombre }}</p>
        <p><strong>Apellido:</strong> {{ apellido }}</p>
        <p><strong>Mail:</strong> {{ mail }}</p>
      </div>
      <button @click="cambiar_contra_vieja">Cambiar Contraseña</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

export default {
  data() {
    return {
      errorMessage: "",
      nombre: "",
      apellido: "",
      mail: "",
      loading: true,
    };
  },
  async mounted() {
    const authStore = useAuthStore();
    const token = authStore.getToken();

    if (!token) {
      this.$router.push({ name: "logIn" });
      return;
    }

    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/usuarios/ver_perfil`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      this.nombre = response.data.nombre;
      this.apellido = response.data.apellido;
      this.mail = response.data.email;
    } catch (error) {
      this.errorMessage =
        error.response?.data?.Error || "Error al cargar el perfil";
    } finally {
      this.loading = false;
    }
  },

  methods: {
    async cambiar_contra_vieja() {
      try {
        this.$router.push({ name: 'cambiar_contra_vieja' }).then(() => {
        });
      } catch (error) {
        this.errorMessage = error.response?.data?.Error || 'Error al cambiar contraseña';
      }
    }
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

body {
  background: radial-gradient(circle, #dfe9f3, #ffffff);
}

.profile-container {
  margin: 0 !important;
  padding: 0 !important;
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(circle, #dfe9f3, #ffffff);
}

.profile-card {
  background: white;
  padding: 4rem;
  border-radius: 12px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 600px;
  width: 80%;
  border: 1px solid #e0e0e0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.user-icon {
  font-size: 6rem;
  color: #4a90e2;
  margin-bottom: 1rem;
}

.profile-info p {
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.3rem;
}

.profile-info p strong {
  color: #555;
}

button {
  width: 100%;
  padding: 1rem;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease, box-shadow 0.3s ease;
  margin-top: 1.5rem;
}

button:hover {
  background: #357ab8;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

button:active {
  transform: scale(0.98);
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #4a90e2;
  border-radius: 50%;
  width: 3rem;
  height: 3rem;
  animation: spin 1s linear infinite;
  margin: 2rem auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  margin-top: 1.5rem;
  color: #ff4d4f;
  font-size: 1rem;
}
</style>