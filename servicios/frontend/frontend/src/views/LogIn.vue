<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="mail">Correo Electrónico:</label>
          <input type="email" v-model="mail" placeholder="Ingresa tu email" required />
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" v-model="password" placeholder="Ingresa tu contraseña" required />
        </div>
        <button type="submit">Ingresar</button>
      </form>
        <button 
        class="recover-password-button" 
        @click="redirectToRecoverPassword">
        ¿Olvidaste tu contraseña?
      </button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export default {
  data() {
    return {
      mail: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      const authStore = useAuthStore();
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/authenticate`, {
          mail: this.mail,
          password: this.password
        });
        authStore.setToken(response.data.access_token);
        if (response.data.cambiar_contra){
          this.$router.push({ name: 'cambiar_contra' }).then(() => {
        });
        }
        else{
          localStorage.setItem('permisos', JSON.stringify(response.data.permisos));
        localStorage.setItem('area', JSON.stringify(response.data.area));
          this.$router.push({ name: 'home' }).then(() => {
            location.reload();
          });
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.Error || 'Error al iniciar sesión';
      }
    },
    redirectToRecoverPassword() {
      try {
        this.$router.push({ name: 'recuperar_contra' }).then(() => {
          });
      } catch (error) {
       console.error("Error al redirigir a la página de recuperación:", error);
      }
    }
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  overflow: hidden; /* Sin barras de desplazamiento */
}

body {
  background: radial-gradient(circle, #dfe9f3, #ffffff); /* Gradiente radial */
}

.login-container {
  margin: 0 !important;
  padding: 0 !important;
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(circle, #dfe9f3, #ffffff); /* Gradiente radial */
}


/* Tarjeta de inicio de sesión */
.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

/* Estilo del título */
h2 {
  margin-bottom: 2rem;
  color: #333;
  font-size: 1.8rem;
  font-weight: bold;
}

/* Grupos de formularios */
.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.85rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #6a11cb;
}

/* Botón */
button {
  width: 100%;
  padding: 0.85rem;
  background: #4a90e2; /* Azul mejorado */
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background: #357ab8;
}

/* Mensaje de error */
.error-message {
  margin-top: 1rem;
  color: #ff4d4f;
  font-size: 0.9rem;
}

.recover-password-button {
  margin-top: 10px;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.recover-password-button:hover {
  background-color: #0056b3;
}

</style>
