<template>
  <button
    @click="generarEncuesta"
    data-bs-toggle="modal"
    data-bs-target="#exampleModal2"
    class="btn btn-dark"
  >
    Generar Encuesta
  </button>
  <div
    class="modal fade"
    id="exampleModal2"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            Comparte este link con tus clientes
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div v-if="done && link" class="modal-body">
          <p>Encuesta generada</p>
          <a :href="link" target="_blank">{{ link }}</a>
        </div>
        <div class="modal-footer d-flex justify-content-between">
          <div>
            <button @click="copyLink" type="button" class="btn btn-primary">Copiar link</button>
          </div>
          <p v-if="copiado" class="mensaje">¡Enlace copiado al portapapeles!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEncuestasStore } from '../stores/encuestas'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'
const encuestasStore = useEncuestasStore()
const { done, link } = storeToRefs(encuestasStore)
const copiado = ref(false)

const generarEncuesta = async () => {
  await encuestasStore.createEncuestas()
}

const copyLink = () => {
  navigator.clipboard
    .writeText(link.value)
    .then(() => {
      copiado.value = true
      setTimeout(() => {
        copiado.value = false
      }, 2000)
    })
    .catch((err) => {
      console.error('Error al copiar el enlace: ', err)
    })
}
</script>
