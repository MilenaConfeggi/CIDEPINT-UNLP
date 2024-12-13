<template>
    <div class="login-container">
      <div class="login-card">
        <h2>Cambiar Contraseña</h2>
        <form @submit.prevent="cambiar_contra_vieja">
          <div class="form-group">
            <label for="oldpassword">Ingrese su contraseña anterior:</label>
            <input type="password" v-model="oldpassword" placeholder="Ingrese su contraseña anterior" required />
          </div>
          <div class="form-group">
            <label for="password">Ingrese una nueva contraseña:</label>
            <input type="password" v-model="password" placeholder="Ingrese una nueva contraseña" required />
          </div>
          <div class="form-group">
            <label for="passw2">Ingrese de nuevo la nueva contraseña:</label>
            <input type="password" v-model="passw2" placeholder="Confirma tu contraseña" required />
          </div>
          <button type="submit">Cambiar Contraseña</button>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useAuthStore } from '@/stores/auth';
  const authStore = useAuthStore();
  
  export default {
    data() {
      return {
        oldpassword: '',
        password: '',
        passw2: '',
        errorMessage: ''
      };
    },
    mounted() {
        const authStore = useAuthStore();
        if (!authStore.getToken()) {
            this.$router.push({ name: 'logIn' });
        }
  },
    methods: {
      async cambiar_contra_vieja() {
        const token = authStore.getToken();
        try {
            if (this.password != this.passw2){
                this.errorMessage = "Las nuevas contraseñas no coinciden"
                return;
            }
          const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/cambiar_contra_vieja`, {
            oldpassword: this.oldpassword,
            password: this.password,
            passw2: this.passw2
          },
          {
            headers: {
              Authorization: `Bearer ${token}` // Agrega el token en el encabezado
            }
          }
        );
          this.$router.push({ name: 'home' }).then(() => {
            location.reload();
          });
        } catch (error) {
          this.errorMessage = error.response?.data?.Error || 'Error al cambiar contraseña';
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
  </style>
  