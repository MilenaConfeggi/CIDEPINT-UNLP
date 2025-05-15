<template>
  <div class="mt-3 d-flex justify-content-between align-items-center">
    <RouterLink
      to="/legajos/newLegajo"
      class="btn btn-success d-flex align-items-center gap-2"
      v-if="hasPermission('crear_legajo')"
      aria-label="Crear nuevo legajo"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" viewBox="0 0 16 16" aria-hidden="true">
        <path fill="currentColor" fill-rule="evenodd"
          d="M3.5 1.5v13h5.75a.75.75 0 0 1 0 1.5H3a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h6.644a1 1 0 0 1 .72.305l3.355 3.476a1 1 0 0 1 .281.695V6.25a.75.75 0 0 1-1.5 0V6H9.75A1.75 1.75 0 0 1 8 4.25V1.5zm6 .07l2.828 2.93H9.75a.25.25 0 0 1-.25-.25zM13 15a.75.75 0 0 1-.75-.75v-1.5h-1.5a.75.75 0 0 1 0-1.5h1.5v-1.5a.75.75 0 0 1 1.5 0v1.5h1.5a.75.75 0 0 1 0 1.5h-1.5v1.5A.75.75 0 0 1 13 15"
          clip-rule="evenodd" />
      </svg>
      Nuevo legajo
    </RouterLink>
    <button @click="borrarFiltros()" class="btn btn-outline-primary d-flex align-items-center gap-2" aria-label="Borrar filtros">
      <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" viewBox="0 0 1024 1024" aria-hidden="true">
        <path fill="#0d6efd"
          d="m899.1 869.6l-53-305.6H864c14.4 0 26-11.6 26-26V346c0-14.4-11.6-26-26-26H618V138c0-14.4-11.6-26-26-26H432c-14.4 0-26 11.6-26 26v182H160c-14.4 0-26 11.6-26 26v192c0 14.4 11.6 26 26 26h17.9l-53 305.6c-.3 1.5-.4 3-.4 4.4c0 14.4 11.6 26 26 26h723c1.5 0 3-.1 4.4-.4c14.2-2.4 23.7-15.9 21.2-30M204 390h272V182h72v208h272v104H204zm468 440V674c0-4.4-3.6-8-8-8h-48c-4.4 0-8 3.6-8 8v156H416V674c0-4.4-3.6-8-8-8h-48c-4.4 0-8 3.6-8 8v156H202.8l45.1-260H776l45.1 260z" />
      </svg>
      Limpiar filtros
    </button>
  </div>
  <div class="flex flex-col justify-center items-center mt-4 w-100">
    <p v-if="error" class="alert alert-danger w-75" role="alert">{{ error }}</p>
    <form class="input-group mb-3 d-flex flex-row flex-wrap gap-2 w-100 justify-content-center align-items-center" @submit.prevent>
      <label class="input-group-text" for="ensayos">Ensayos</label>
      <input v-model="ensayo" id="ensayos" type="text" aria-label="Ensayos" class="form-control" placeholder="Ingresar ensayo." />

      <label v-if="userRol === ''" class="input-group-text" for="area">Áreas</label>
      <select v-if="userRol === '' && areas" v-model="area" class="form-select" id="area">
        <option selected value="">Elige un área</option>
        <option v-for="area in areas" :key="area.id" :value="area.id">
          {{ area.nombre }}
        </option>
      </select>

      <label class="input-group-text" for="empresa">Empresa</label>
      <input v-model="empresa" id="empresa" type="text" aria-label="nombre del cliente" class="form-control"
        placeholder="Ingresar nombre de empresa." />

      <label class="input-group-text" for="date">Fecha de carga</label>
      <input id="date" type="date" v-model="fecha" @input="validateDates" :max="today" placeholder="Fecha de inicio" class="form-control" />
    </form>

    <div v-if="legajos.items?.length && !error" class="table-responsive w-100">
      <table class="table table-hover table-bordered align-middle" aria-label="Listado de legajos">
        <caption class="visually-hidden">Listado de legajos</caption>
        <thead class="thead-dark">
          <tr>
            <th scope="col" class="col-numero">Nro interno</th>
            <th scope="col" class="col-ensayos">Ensayos</th>
            <th scope="col" class="col-area">Área</th>
            <th scope="col" class="col-estado">Estado</th>
            <th scope="col" class="col-acciones">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="legajo in legajos.items" :key="legajo.id" tabindex="0" :aria-label="`Legajo ${legajo.id}`">
            <th scope="row">{{ legajo.id }}/{{ legajo.fecha_entrada ? legajo.fecha_entrada.substring(2, 4) : '' }}</th>
            <td>
              <div v-if="legajo.presupuesto_cidepint">
                <ul class="list-unstyled mb-0">
                  <li v-for="presupuesto in legajo.presupuesto_cidepint" :key="presupuesto.id">
                    <ul class="list-unstyled mb-0">
                      <li v-for="stan in presupuesto.stans" :key="stan.id">
                        <span v-for="(ensayo, idx) in stan.ensayos" :key="ensayo.id">
                          {{ ensayo.nombre }}<span v-if="idx < stan.ensayos.length - 1">, </span>
                        </span>
                      </li>
                    </ul>
                  </li>
                </ul>
              </div>
              <span v-else class="text-muted">Sin ensayos</span>
            </td>
            <td>{{ legajo.area.nombre }}</td>
            <td>
              <StateBadge :state="legajo.estado?.nombre" />
            </td>
            <td>
              <div class="d-flex flex-wrap gap-2 justify-content-center align-items-center">
                <RouterLink
                  :to="`/legajos/${legajo.id}`"
                  class="btn btn-primary btn-sm"
                  v-if="hasPermission('ver_legajo')"
                  aria-label="Ver detalle del legajo"
                  title="Ver detalle"
                >
                  <i class="fas fa-eye" aria-hidden="true"></i>
                </RouterLink>
                <RouterLink
                  :to="`/legajos/cancelar/${legajo.id}`"
                  v-if="hasPermission('cancelar_legajo')"
                  aria-label="Cancelar legajo"
                  title="Cancelar legajo"
                >
                  <button v-if="legajo.estado?.nombre === 'En curso'" class="btn btn-danger btn-sm">
                    <i class="fas fa-ban" aria-hidden="true"></i>
                  </button>
                </RouterLink>
                <button
                  v-if="hasPermission('cancelar_legajo')"
                  @click="eliminarLegajo(legajo.id)"
                  class="btn btn-danger btn-sm"
                  aria-label="Eliminar legajo"
                  title="Eliminar legajo"
                >
                  <i class="fas fa-trash-alt" aria-hidden="true"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <nav aria-label="Paginación" class="mt-3">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="prevPage" :disabled="currentPage === 1" aria-label="Página anterior">
              Anterior
            </button>
          </li>
          <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
            <button class="page-link" @click="goToPage(page)" :aria-current="currentPage === page ? 'page' : undefined">
              {{ page }}
            </button>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="nextPage" :disabled="currentPage === totalPages" aria-label="Página siguiente">
              Siguiente
            </button>
          </li>
        </ul>
      </nav>
    </div>
    <p v-else-if="loading" class="font-bold text-center mt-4">Cargando...</p>
    <p v-else class="font-bold text-center mt-4">No hay legajos</p>
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

const permisos = JSON.parse(localStorage.getItem('permisos')) || []

const hasPermission = (permiso) => {
  return permisos.includes(permiso)
}

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
  if (new Date(fecha.value) > new Date()) {
    toast.warning('La fecha no puede ser en el futuro.')
    fecha.value = ''
  }
}

const borrarFiltros = () => {
  area.value = ''
  ensayo.value = ''
  empresa.value = ''
  fecha.value = ''
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

const eliminarLegajo = async (id) => {
  if (confirm('¿Está seguro de que desea eliminar este legajo?')) {
    try {
      await legajosStore.deleteLegajo(id);
      toast.success('Legajo eliminado con éxito.');
      fetchLegajos();
    } catch (error) {
      toast.error('Error al eliminar el legajo.');
    }
  }
};

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
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.07);
  border-radius: 8px;
  overflow: hidden;
}

.table th,
.table td {
  text-align: center;
  vertical-align: middle;
  padding: 10px;
  border: 1px solid #e3e3e3;
}

.table-hover tbody tr:hover {
  background-color: #eaf4fb;
  cursor: pointer;
}

.thead-dark th {
  background-color: #343a40;
  color: white;
}

.col-numero {
  width: 10%;
}
.col-ensayos {
  width: 40%;
}
.col-area {
  width: 15%;
}
.col-estado {
  width: 15%;
}
.col-acciones {
  width: 20%;
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

.page-link:hover,
.page-item.active .page-link {
  background-color: #007bff;
  color: white;
}

.page-item.disabled .page-link {
  color: #ccc;
  cursor: not-allowed;
  background-color: #f8f9fa;
  border-color: #ddd;
}

.btn {
  transition: box-shadow 0.2s;
}

.btn:focus {
  outline: 2px solid #0056b3;
  outline-offset: 2px;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.95rem;
}

.visually-hidden {
  position: absolute !important;
  height: 1px; width: 1px;
  overflow: hidden;
  clip: rect(1px, 1px, 1px, 1px);
  white-space: nowrap;
}
</style>