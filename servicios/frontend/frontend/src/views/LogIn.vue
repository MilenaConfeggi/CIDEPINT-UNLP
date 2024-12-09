<template>
    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="mail">Email:</label>
          <input type="email" v-model="mail" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
      </form>
      <p v-if="errorMessage">{{ errorMessage }}</p>
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
          console.log(this.mail, this.password);
          const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/authenticate`, {
            mail: this.mail,
            password: this.password
          });
          authStore.setToken(response.data.access_token);
          localStorage.setItem('permisos', JSON.stringify(response.data.permisos));
          console.log(authStore.getToken());
          this.$router.push({ name: 'home' }); // Redirect to home or another page
        } catch (error) {
          this.errorMessage = error.response.data.Error || 'Login failed';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>