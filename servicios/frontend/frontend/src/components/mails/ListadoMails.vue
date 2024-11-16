<template>
  <div>
    <h1>Listado de Mails</h1>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="mails.length" class="cards-container">
      <div v-for="mail in mails" :key="mail.id" class="card">
        <img :src="getImageUrl(mail.legajo_id, mail.nombre_archivo)" alt="Imagen de mail" class="card-img" />
        <div class="card-body">
          <p>ID: {{ mail.id }}</p>
          <p>Fecha: {{ mail.fecha }}</p>
          <p>Nombre de Archivo: {{ mail.nombre_archivo }}</p>
          <p>Legajo ID: {{ mail.legajo_id }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      No hay mails disponibles.
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
      const url = `http://127.0.0.1:5000/mails/imagenes/${legajoId}/${filename}`;
      console.log(url);  // Imprimir la URL en la consola
      return url;
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
.error {
  color: red;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  width: 200px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.card-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.card-body {
  padding: 1rem;
}
</style>