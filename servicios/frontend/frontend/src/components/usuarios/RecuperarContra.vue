<template>
    <div class="login-container">
      <div class="login-card">
        <h2>Recuperar Contraseña</h2>
        <form @submit.prevent="recuperar_contra">
          <div class="form-group">
            <label for="password">Ingrese su mail:</label>
            <input type="email" v-model="mail" placeholder="Ingrese su mail" required />
          </div>
          <button type="submit">Recuperar Contraseña</button>
        </form>
        <div v-if="successMessage" class="alert alert-success" role="alert">{{ successMessage }}</div>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {

    data() {
      return {
        mail: '',
        errorMessage: '',
        successMessage: null,
      };
    },
    mounted() {
  },
    methods: {
      async recuperar_contra() {
        try {
          const response = await axios.post(`${import.meta.env.VITE_API_URL}/usuarios/recuperar_contra`, {
            mail: this.mail
          }
        );
        this.successMessage = response.data.message;
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

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}
  </style>
  