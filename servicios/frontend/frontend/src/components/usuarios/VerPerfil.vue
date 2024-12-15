<template>
    <div class="login-container">
      <div class="login-card">
        <h2>Mi Perfil</h2>
        <p>Nombre: {{ nombre }}</p>
        <p>Apellido: {{ apellido }}</p>
        <p>Mail: {{ mail }}</p>
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
      };
    },
    async mounted() {
      const authStore = useAuthStore();
      const token = authStore.getToken();
  
      // Verifica si el token no existe y redirige
      if (!token) {
        this.$router.push({ name: "logIn" });
        return; // Detén la ejecución del resto del código
      }
  
      try {
        // Realiza la petición al servidor
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/usuarios/ver_perfil`,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Incluye el token en el encabezado
            },
          }
        );
  
        // Asigna los datos a las variables del componente
        this.nombre = response.data.nombre;
        this.apellido = response.data.apellido;
        this.mail = response.data.email;
      } catch (error) {
        // Maneja errores de la petición
        this.errorMessage =
          error.response?.data?.Error || "Error al cargar el perfil";
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
  