<template>
    <div class="container mt-4">
      <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
      <div v-if="mail">
        <div class="text-center">
          <img :src="getImageUrl(mail.legajo_id, mail.nombre_archivo)" alt="Imagen de mail" class="img-fluid large-image" />
        </div>
      </div>
      <div v-else class="text-center">
        <p class="text-muted">Cargando...</p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import axios from 'axios';
  import { useAuthStore } from '../../stores/auth';
  import { useRouter } from 'vue-router';

  export default {
    setup() {
      const route = useRoute();
      const mailId = Number(route.params.mailId);
      const mail = ref(null);
      const error = ref(null);
      const authStore = useAuthStore();
      const router = useRouter();

      const fetchMail = async () => {
        try {
          const response = await axios.get(`${import.meta.env.VITE_API_URL}/mails/${mailId}`);
          if (response.status !== 200) {
            throw ({message: 'Error al obtener el mail', status: response.status})
          }
          mail.value = response.data;
        } catch (err) {
          if (err.status === 401 || err.status === 422) {
            authStore.logout()
            router.push('/log-in')
          } else {
            error.value = 'Error al cargar el mail';
            console.error(err);
          }
        }
      };
  
      const getImageUrl = (legajoId, filename) => {
        return `${import.meta.env.VITE_API_URL}/mails/imagenes/${legajoId}/${filename}`;
      };
  
      onMounted(() => {
        fetchMail();
      });
  
      return { mail, error, getImageUrl };
    }
  };
  </script>
  
  <style scoped>
  .img-fluid.large-image {
    max-width: 100%;
    height: auto;
    max-height: 80vh; 
  }
  </style>