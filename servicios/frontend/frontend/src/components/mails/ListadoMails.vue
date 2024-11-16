<template>
    <div>
        <h1>Listado de Mails</h1>
        <div v-if="error" class="error">{{ error }}</div>
        <ul v-if="mails.length">
            <li v-for="mail in mails" :key="mail.id">
                <p>ID: {{ mail.id }}</p>
                <p>Fecha: {{ mail.fecha }}</p>
                <p>Nombre de Archivo: {{ mail.nombre_archivo }}</p>
                <p>Legajo ID: {{ mail.legajo_id }}</p>
            </li>
        </ul>
        <div v-else>
            No hay mails disponibles.
        </div>
    </div>
</template>

<script>
import { useMailsStore } from '@/stores/mails';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

export default {
  setup() {
    const store = useMailsStore();
    const { mails, error } = storeToRefs(store);
    const fetchMails = async () => {
      await store.fetchMails();
    };
    onMounted(() => {
      fetchMails();
    });
    return { mails, error };
  }
};
</script>

<style scoped>
.error {
    color: red;
}
</style>