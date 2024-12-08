<template>
  <RouterLink to="/legajos/newLegajo" class="hover:underline">
    <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 16 16">
      <path
        fill="currentColor"
        fill-rule="evenodd"
        d="M3.5 1.5v13h5.75a.75.75 0 0 1 0 1.5H3a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h6.644a1 1 0 0 1 .72.305l3.355 3.476a1 1 0 0 1 .281.695V6.25a.75.75 0 0 1-1.5 0V6H9.75A1.75 1.75 0 0 1 8 4.25V1.5zm6 .07l2.828 2.93H9.75a.25.25 0 0 1-.25-.25zM13 15a.75.75 0 0 1-.75-.75v-1.5h-1.5a.75.75 0 0 1 0-1.5h1.5v-1.5a.75.75 0 0 1 1.5 0v1.5h1.5a.75.75 0 0 1 0 1.5h-1.5v1.5A.75.75 0 0 1 13 15"
        clip-rule="evenodd"
      />
    </svg>
  </RouterLink>
  <p v-if="legajos">{{ legajos.items?.length }} Legajos</p>
  <div class="flex flex-col justify-center items-center">
    <p v-if="loading">Cargando...</p>
    <p v-if="error">{{ error }}</p>
    <div class="input-group mb-3 d-flex flex-row">
      <label class="input-group-text" for="documento">Ensayos</label>
      <select v-model="documento" class="form-select" id="documento">
        <option selected value="">Choose...</option>
        <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option>
      </select>
      <label class="input-group-text" for="area">Areas</label>
      <select v-if="areas" v-model="area" class="form-select" id="area">
        <option selected value="">Choose...</option>
        <option v-for="area in areas" :key="area.id" :value="area.id">
          {{ area.nombre }}
        </option>
      </select>
      <span class="input-group-text">Empresa</span>

      <input
        v-model="empresa"
        type="text"
        aria-label="nombre del cliente"
        class="form-control"
      />
      <input type="date" v-model="fecha" @input="validateDates" placeholder="Fecha de inicio" />
    </div>
    <div v-if="legajos.items?.length && !error">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Nro interno</th>
            <th scope="col">Ensayos</th>
            <th scope="col">Area</th>
            <th scope="col">Estado</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="legajo in legajos.items" :key="legajo.id">
            <th scope="row">{{ legajo.id }}</th>
            <td>{{ legajo.cliente?.nombre }}</td>
            <td>{{ legajo.area.nombre }}</td>
            <td><StateBadge :state="legajo.estado?.nombre" /></td>
            <td>
              <RouterLink :to="`/legajos/${legajo.id}`" class="hover:underline">
                Ver detalle
              </RouterLink>
              <RouterLink :to="`/legajos/cancelar/${legajo.id}`" class="hover:underline">
                <button
                v-if="legajo.estado?.nombre === 'En curso'"
                class="btn btn-danger"
                >
                Cancelar
              </button>
            </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="totalPages > 1" class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>

        <span>Página {{ currentPage }} de {{ totalPages }}</span>

        <button @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
      </div>
    </div>
    <div v-else>
      No hay legajos
    </div>
  </div>
</template>
<script setup>
import { onMounted, watch } from 'vue'
import StateBadge from '../StateBadge.vue'
import { useLegajosStore } from '../../stores/legajos'
import { useAreasStore } from '../../stores/areas'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'

const legajosStore = useLegajosStore()
const areasStore = useAreasStore()
const currentPage = ref(1)

var documento = ref('')
var area = ref('')
var empresa = ref('')
var fecha = ref('')

const { legajos, loading, error, totalPages } = storeToRefs(legajosStore)
const { areas } = storeToRefs(areasStore)

const validateDates = () => {
  if (new Date(this.startDate) > new Date()) {
    alert('La fecha no puede ser en el futuro.')
    fecha.value = ''
  }
}

const fetchLegajos = async () => {
  const params = {
    //documento: documento.value,
    area: area.value,
    empresa: empresa.value,
    fecha: fecha.value,
    page: currentPage.value,
    per_page: 10,
  }
  await legajosStore.getLegajos(params)
}

const fetchAreas = async () => {
  await areasStore.getAreas()
}



const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

onMounted(() => {
  fetchAreas()
  fetchLegajos()
})

watch([documento, area, empresa, fecha, currentPage], () => {
  fetchLegajos()
})

</script>
