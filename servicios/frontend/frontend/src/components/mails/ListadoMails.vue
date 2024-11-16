<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Mails para el legajo {{ legajoId }}</h1>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="mails.length" class="row">
      <div v-for="mail in mails" :key="mail.id" class="col-md-3 mb-4">
        <div class="card">
          <div class="card-img-container">
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
  </div>
</template>

<script>
import { useMailsStore } from '@/stores/mails';
import { storeToRefs } from 'pinia';
import { onMounted, watch } from 'vue';
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

    const fetchMails = async () => {
      await store.fetchMails(props.legajoId);
    };

    const getImageUrl = (legajoId, filename) => {
      return `http://127.0.0.1:5000/mails/imagenes/${legajoId}/${filename}`;
    };

    const confirmarEliminarMail = (idMail) => {
      if (confirm("¿Estás seguro de que deseas eliminar este mail?")) {
        eliminarMail(idMail);
      }
    };

    const eliminarMail = async (idMail) => {
      try {
        const response = await axios.post(`http://127.0.0.1:5000/mails/eliminar_mail/${idMail}`);
        if (response.status === 200) {
          fetchMails(); // Refrescar la lista de mails después de eliminar
        }
      } catch (error) {
        console.error('Error al eliminar el mail:', error);
      }
    };

    onMounted(() => {
      fetchMails();
    });

    watch(() => props.legajoId, fetchMails);

    return { mails, error, getImageUrl, confirmarEliminarMail };
  }
};
</script>

<style scoped>
.card-img-container {
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa; 
}

.card-img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.card-body {
  position: relative;
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
</style>