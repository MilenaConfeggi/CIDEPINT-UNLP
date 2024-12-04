<template>
    <div class="login-container">
      <form @submit.prevent="submitForm" class="login-form">
        <h2>Login</h2>
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Ingrese email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Ingrese su contraseña"
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: "",
        password: "",
      };
    },
    methods: {
        async submitForm() {
            const userData = {
                mail: this.email,
                password: this.password,
            };
            try {
                //const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/authenticate`,{
                //    method: "POST",
                //    headers: {
                //        "Content-Type": "application/json",
                //    },
                //    body: JSON.stringify(userData),
                //});
                // Construir los parámetros de consulta (query params)
                const queryParams = new URLSearchParams({
                    mail: this.email,
                    password: this.password,
                }).toString();

                // Hacer la solicitud GET con los parámetros en la URL
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/auth/authenticate?${queryParams}`,
                    {
                    method: "GET", // Cambiar el método a GET
                    credentials: 'include',
                    }
                );
                const data = await response.json();
                console.log("Respuesta del servidor:", data);
            } catch (error) {
            console.error("Error al enviar los datos:", error);
        }
  },
},
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f0f4f8;
  }
  .login-form {
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
  }
  .login-form h2 {
    margin-bottom: 1.5rem;
    color: #333;
    text-align: center;
  }
  .form-group {
    margin-bottom: 1rem;
  }
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #555;
  }
  .form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
  }
  button {
    width: 100%;
    padding: 0.75rem;
    background-color: #4CAF50;
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
  }
  button:hover {
    background-color: #45a049;
  }
  </style>
  