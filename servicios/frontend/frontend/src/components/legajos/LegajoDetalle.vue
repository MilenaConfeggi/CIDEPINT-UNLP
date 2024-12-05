<template>
  <main>
    <RouterLink to="/legajos" class="">
      <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24">
        <g fill="none">
          <path
            d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"
          />
          <path
            fill="black"
            d="M3.283 10.94a1.5 1.5 0 0 0 0 2.12l5.656 5.658a1.5 1.5 0 1 0 2.122-2.122L7.965 13.5H19.5a1.5 1.5 0 0 0 0-3H7.965l3.096-3.096a1.5 1.5 0 1 0-2.122-2.121z"
          />
        </g>
      </svg>
    </RouterLink>
    <div
      class="d-flex justify-content-center align-items-center border-2 border-blue-500 rounded-lg p-4 m-4"
    >
      <p v-if="loading">Cargando...</p>
      <p v-if="error">{{ error }}</p>
      <p v-if="!legajo && !loading">No se encontro el legajo</p>
      <div v-else>
        <p>{{ legajo.id }}</p>
        <StateBadge v-if="legajo.estado" :state="legajo.estado?.nombre" />
        <p>Fecha entrada: {{ formatDate(legajo.fecha_entrada) }}</p>
        <p>Objetivo: {{ legajo.objetivo }}</p>
        <p>Es juridico: {{ legajo.es_juridico }}</p>
        <p>Necesita facturacion: {{ legajo.necesita_facturacion }}</p>
        <p>Motivo cancelación: {{ legajo.motivo_cancelacion }}</p>
        <div v-if="legajo.cliente">
          <h6>Cliente</h6>
          <p>Email: {{ legajo.cliente.email }}</p>
          <p>Teléfono: {{ legajo.cliente.telefono }}</p>
          <p>Dirección: {{ legajo.cliente.direccion }}</p>
          <p>CUIT: {{ legajo.cliente.cuit }}</p>
          <p>Fecha de nacimiento: {{ legajo.cliente.fecha_nacimiento }}</p>
        </div>
        <div v-if="legajo.documento">
          <table class="table">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Nombre</th>
            <th scope="col">tipo</th>
            <th scope="col">Estado</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in legajo.documento" :key="doc.id">
            <td>{{ doc.id }}</td>
            <td>{{ doc.nombre_documento }}</td>
            <td>{{ doc.tipo_documento.nombre }}</td>
            <td>{{ doc.estado.nombre }}</td>
          </tr>
        </tbody>
      </table>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useLegajosStore } from '../../stores/legajos'
import { storeToRefs } from 'pinia'
import StateBadge from '../StateBadge.vue'

const route = useRoute()
const legajosStore = useLegajosStore()

const { legajo, loading, error } = storeToRefs(legajosStore)

const formatDate = (dateString) => {
  const options = { year: 'numeric', day: '2-digit', month: '2-digit' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

onMounted(async () => {
  try {
    await legajosStore.getLegajo(route.params.id)
  } catch (err) {
    console.error('Error al cargar el legajo:', err)
  }
})
</script>
