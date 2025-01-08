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
  <div class="flex flex-col justify-center items-center">
    <p v-if="error">{{ error }}</p>
    <div class="input-group mb-3 d-flex flex-row">
      <label class="input-group-text" for="ensayos">Ensayos</label>
      <input v-model="ensayo" type="text" aria-label="Ensayos" class="form-control" />
      <label v-if="userRol === ''" class="input-group-text" for="area">Areas</label>
      <select v-if="userRol === '' && areas" v-model="area" class="form-select" id="area">
        <option selected value="">Elige un area</option>
        <option v-for="area in areas" :key="area.id" :value="area.id">
          {{ area.nombre }}
        </option>
      </select>
      <span class="input-group-text">Empresa</span>

      <input v-model="empresa" type="text" aria-label="nombre del cliente" class="form-control" />
      <label class="input-group-text" for="date">Fecha de carga</label>
      <input
        id="date"
        type="date"
        v-model="fecha"
        @input="validateDates"
        :max="today"
        placeholder="Fecha de inicio"
      />
    </div>
    <div v-if="legajos.items?.length && !error">
      <table class="table table-hover table-bordered">
        <thead class="thead-dark">
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
            <td>
              <div v-if="legajo.presupuesto_cidepint[0]?.stans">
                <div v-for="stan in legajo.presupuesto_cidepint[0].stans" :key="stan.id">
                  <span v-for="ensayo in stan.ensayos" :key="ensayo.id">{{
                    ensayo.nombre + ', '
                  }}</span>
                </div>
              </div>
            </td>
            <td>{{ legajo.area.nombre }}</td>
            <td><StateBadge :state="legajo.estado?.nombre" /></td>
            <td>
              <RouterLink :to="`/legajos/${legajo.id}`" class="btn btn-primary mr-3">
                Ver detalle
              </RouterLink>
              <RouterLink :to="`/legajos/cancelar/${legajo.id}`">
                <button v-if="legajo.estado?.nombre === 'En curso'" class="btn btn-danger">
                  Cancelar
                </button>
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
      <nav aria-label="Paginación" class="mt-3">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="prevPage" :disabled="currentPage === 1">
              Anterior
            </button>
          </li>
          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: currentPage === page }"
          >
            <button class="page-link" @click="goToPage(page)">{{ page }}</button>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="nextPage" :disabled="currentPage === totalPages">
              Siguiente
            </button>
          </li>
        </ul>
      </nav>
    </div>
    <p v-else-if="loading" class="font-bold text-center">Cargando...</p>
    <p v-else class="font-bold text-center">No hay legajos</p>
  </div>
</template>
<script setup>
import { onMounted, watch } from 'vue'
import StateBadge from '../StateBadge.vue'
import { useLegajosStore } from '../../stores/legajos'
import { useAreasStore } from '../../stores/areas'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()
const today = new Date().toISOString().split('T')[0]

const legajosStore = useLegajosStore()
const areasStore = useAreasStore()
const currentPage = ref(1)
const areaRol = localStorage.getItem('area') === 'null' ? '' : localStorage.getItem('area')
var ensayo = ref('')
var userRol = ref(areaRol)
var area = ref('')
var empresa = ref('')
var fecha = ref('')

const { legajos, loading, error, totalPages } = storeToRefs(legajosStore)
const { areas } = storeToRefs(areasStore)

const validateDates = () => {
  if (new Date(this.startDate) > new Date()) {
    toast.warning('La fecha no puede ser en el futuro.')
    fecha.value = ''
  }
}

const fetchLegajos = async () => {
  const params = {
    area: userRol.value === '' ? area.value : userRol.value,
    ensayo: ensayo.value,
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

const goToPage = (page) => {
  currentPage.value = page
}

onMounted(() => {
  fetchAreas()
  fetchLegajos()
})

watch([ensayo, area, empresa, fecha, currentPage], () => {
  fetchLegajos()
})
</script>

<style scoped>
.table {
  width: 100%;
  margin: auto;
  border-collapse: collapse;
  background-color: #f9f9f9; /* Fondo claro para la tabla */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Sombra para la tabla */
}

.table th,
.table td {
  text-align: center;
  vertical-align: middle;
  padding: 10px;
  border: 1px solid #ddd; /* Bordes ligeros para las celdas */
}

.table-hover tbody tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}

.table-active {
  background-color: #d1ecf1;
}

.thead-dark th {
  background-color: #343a40;
  color: white;
}

.line {
  border: 0;
  height: 1px;
  background: #333;
  background-image: linear-gradient(to right, #ccc, #333, #ccc);
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.page-item {
  list-style: none;
}

.page-link {
  display: inline-block;
  padding: 8px 12px;
  margin: 0 5px;
  border: 1px solid #007bff;
  border-radius: 4px;
  color: #007bff;
  background-color: white;
  text-decoration: none;
  transition: all 0.3s ease;
}

.page-link:hover {
  background-color: #007bff;
  color: white;
}

.page-item.active .page-link {
  background-color: #0056b3;
  color: white;
  border-color: #0056b3;
}

.page-item.disabled .page-link {
  color: #ccc;
  cursor: not-allowed;
  background-color: #f8f9fa;
  border-color: #ddd;
}

.page-item.previous .page-link,
.page-item.next .page-link {
  padding: 8px 16px;
  font-weight: bold;
}

/* Definir anchos fijos para las columnas */
.col-numero {
  width: 10%;
}

.col-ensayos {
  width: 50%;
}

.col-precio-por {
  width: 10%;
}

.col-precio-pesos {
  width: 10%;
}

.col-precio-dolares {
  width: 10%;
}

.col-acciones {
  width: 10%;
}

.fade-in {
  opacity: 0;
  animation: fadeIn 0.5s forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}
</style>
