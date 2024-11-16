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

    onMounted(() => {
      fetchMails();
    });

    watch(() => props.legajoId, fetchMails);

    return { mails, error, getImageUrl };
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
</style>