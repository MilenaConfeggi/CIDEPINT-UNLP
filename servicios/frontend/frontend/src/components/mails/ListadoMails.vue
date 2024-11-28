<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Mails para el legajo {{ legajoId }}</h1>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="mails.length" class="row">
      <div v-for="mail in mails" :key="mail.id" class="col-md-3 mb-4">
        <div class="card">
          <div class="card-img-container" @click="mostrarVerMail(mail)">
            <img
              :src="getImageUrl(mail.legajo_id, mail.nombre_archivo)"
              alt="Imagen de mail"
              class="card-img"
            />
          </div>
          <div class="card-body">
            <h5 class="card-title">{{ mail.nombre_archivo }}</h5>
            <p class="card-text">Fecha de carga: {{ mail.fecha }}</p>
            <button @click="confirmarEliminarMail(mail.id)" class="btn-icon">
              <i class="fas fa-trash-alt"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center">
      <p class="text-muted">No hay mails disponibles.</p>
    </div>

    <!-- Modal de VerMail -->
    <div v-if="mostrarVerMailModal" class="modal-overlay" @click="cerrarVerMail">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="cerrarVerMail">&times;</button>
        <div v-if="mailSeleccionado">
          <div class="text-center">
            <img :src="getImageUrl(mailSeleccionado.legajo_id, mailSeleccionado.nombre_archivo)" alt="Imagen de mail" class="img-fluid large-image" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useMailsStore } from '@/stores/mails';
import { storeToRefs } from 'pinia';
import { onMounted, watch, ref } from 'vue';
import axios from 'axios';

export default {
  props: {
    legajoId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const store = useMailsStore();
    const { mails, error } = storeToRefs(store);

    const mostrarVerMailModal = ref(false);
    const mailSeleccionado = ref(null);

    const fetchMails = async () => {
      await store.fetchMails(props.legajoId);
    };

    const getImageUrl = (legajoId, filename) => {
      return `${import.meta.env.VITE_API_URL}/mails/imagenes/${legajoId}/${filename}`;
    };

    const confirmarEliminarMail = (idMail) => {
      if (confirm("¿Estás seguro de que deseas eliminar este mail?")) {
        eliminarMail(idMail);
      }
    };

    const eliminarMail = async (idMail) => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/mails/eliminar_mail/${idMail}`);
        if (response.status === 200) {
          fetchMails(); // Refrescar la lista de mails después de eliminar
        }
      } catch (error) {
        console.error('Error al eliminar el mail:', error);
      }
    };

    const mostrarVerMail = (mail) => {
      mailSeleccionado.value = mail;
      mostrarVerMailModal.value = true;
    };

    const cerrarVerMail = () => {
      mostrarVerMailModal.value = false;
      mailSeleccionado.value = null;
    };

    onMounted(() => {
      fetchMails();
    });

    watch(() => props.legajoId, fetchMails);

    return { mails, error, getImageUrl, confirmarEliminarMail, mostrarVerMail, cerrarVerMail, mostrarVerMailModal, mailSeleccionado };
  }
};
</script>

<style scoped>
.card-img-container {
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff; 
  cursor: pointer;
}

.card-img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.card-body {
  position: relative;
  color: #000000;
  background-color: #ffffff; 
  padding-bottom: 40px; 
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); 
}

.btn-icon {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-size: 1.2rem;
}

.btn-icon:hover {
  color: #a71d2a;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; 
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 80%;
  width: 100%;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.img-fluid.large-image {
  max-width: 100%;
  height: auto;
  max-height: 80vh; 
}
</style>