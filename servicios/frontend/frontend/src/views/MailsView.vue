<script setup>
import { useRoute } from 'vue-router'
import ListadoMails from '../components/mails/ListadoMails.vue'
import SubirMails from '../components/mails/SubirMails.vue'

const route = useRoute()
const legajoId = route.params.legajoId
</script>

<template>
  <main>
    <ListadoMails :legajo-id="legajoId" />
    <SubirMails :legajo-id="legajoId" />
  </main>
</template>