<template>
  <h1 class="text-center">Listado de documentos</h1>
  <div class="flex flex-col justify-center items-center">
    <p v-if="loading">Cargando...</p>
    <p v-if="error">{{ error }}</p>
    <div class="input-group mb-3 d-flex flex-row">
      <label class="input-group-text" for="tipo_documento">Tipo de documento</label>
      <select v-model="tipo_documento" class="form-select" id="tipo_documento">
        <option selected value="">Todos</option>
        <option v-for="tipo in tipos_documentos" :key="tipo.id" :value="tipo.id">
          {{ tipo?.nombre }}
        </option>
      </select>
      <label v-if="area === ''" class="input-group-text" for="area">Areas</label>
      <select v-model="area" v-if="areas && area === ''" class="form-select" id="area">
        <option selected value="">Todos</option>
        <option v-for="area in areas" :key="area.id" :value="area.id">
          {{ area.nombre }}
        </option>
      </select>
      <label class="input-group-text" for="empresa">Empresa</label>
      <input
        v-model="empresa"
        type="text"
        aria-label="nombre del cliente"
        class="form-control"
        id="empresa"
      />
      <label class="input-group-text" for="ensayo">Ensayo</label>
      <input
        v-model="ensayo"
        class="form-control"
        id="ensayo"
        type="text"
        aria-label="nombre del ensayo"
      />
      <label class="input-group-text" for="date">Fecha de carga</label>
      <input
        type="date"
        v-model="fecha"
        @input="validateDates"
        placeholder="Fecha de inicio"
        id="fecha"
      />
    </div>
    <div v-if="documentos.items?.length">
      <div></div>
      <table class="table table-hover table-bordered">
        <thead class="thead-dark">
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Fecha de carga</th>
            <th scope="col">Tipo de documento</th>
            <th scope="col">Nro de legajo</th>
            <th scope="col">Nro de presupuesto</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="documento in documentos.items" :key="documento.id">
            <th scope="row">{{ documento?.nombre_documento }}</th>
            <td>{{ new Date(documento?.fecha_creacion).toLocaleDateString() }}</td>
            <td>{{ documento?.tipo_documento?.nombre }}</td>
            <td>{{ documento?.legajo_id }}</td>
            <td>
              {{
                documento.tipo_documento.nombre === 'Presupuesto CIDEPINT'
                  ? documento?.legajo.presupuesto_cidepint?.id
                  : '-'
              }}
            </td>
            <td>
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-toggle="modal"
                data-bs-target="#exampleModal"
                @click="viewFile(documento)"
              >
                Ver documento
              </button>
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
    <div v-else>No hay Documentos</div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useDocumentosStore } from '../../stores/documentos'
import { useAreasStore } from '@/stores/areas'
import { usePresupuestoStore } from '../../stores/presupuesto'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '../../stores/auth'
import { useInformeStore } from '../../stores/informe'

const documentosStore = useDocumentosStore()
const presupuestosStore = usePresupuestoStore()
const informeStore = useInformeStore()
const toast = useToast()
const areasStore = useAreasStore()
const authStore = useAuthStore()
const currentPage = ref(1)
const actualFile = ref(null)
const fileUrl = ref(null)
var tipo_documento = ref('')
const areaRol = localStorage.getItem('area') == 'null' ? '' : localStorage.getItem('area')
var area = ref(areaRol)
var empresa = ref('')
var fecha = ref('')
var ensayo = ref('')

const { documentos, loading, error, totalPages, tipos_documentos } = storeToRefs(documentosStore)
const { areas } = storeToRefs(areasStore)

const validateDates = () => {
  if (new Date(this.startDate) > new Date()) {
    alert('La fecha no puede ser en el futuro.')
    fecha.value = ''
  }
}

const fetchDocumentos = async () => {
  await documentosStore.getTiposDocumentos()
  const params = {
    tipo_documento: tipo_documento.value,
    page: currentPage.value,
    per_page: 10,
    empresa: empresa.value,
    fecha: fecha.value,
    area: area.value,
    ensayo: ensayo.value,
  }
  await documentosStore.getDocumentos(params)
  console.log(documentosStore.documentos)
}

const fetchAreas = async () => {
  await areasStore.getAreas()
}

const viewLegajo = async (legajoId) => {
  const token = authStore.getToken()
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/presupuestos/ver_legajo/${legajoId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: 'blob',
      },
    )

    // Crear una URL para visualizar el archivo
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    const fileUrl = URL.createObjectURL(blob)
    window.open(fileUrl, '_blank')
  } catch (error) {
    console.error('Error al obtener el archivo del legajo:', error)
    toast.warning('No se pudo cargar el archivo del legajo.')
  }
}

const viewFile = async (doc) => {
  console.log(doc)
  if (doc.tipo_documento.nombre === 'Presupuesto CIDEPINT'){
    presupuestosStore.viewPresupuesto(doc.legajo_id)
    return
  }
  if (doc.tipo_documento.nombre === 'Certificado CIDEPINT'){
    viewCertificado(doc.legajo_id)
    return
  }
  if (doc.tipo_documento.nombre === 'Informe'){
    if ([8, 9].includes(doc.estado_id)) {
      informeStore.verDocumentacion(doc.legajo_id)
    }
    else {
      informeStore.verInforme(doc.legajo_id)
    }
    return
  }
  if (doc.tipo_documento.nombre === 'Legajo'){
    viewLegajo(doc.legajo_id)
    return
  }
  actualFile.value = doc
  const tipo = doc.tipo_documento.nombre
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/api/documentos/view/${actualFile.value.nombre_documento}`,
      {
        params: { tipo },
        responseType: 'blob',
      },
    )

    // Crear una URL para visualizar el archivo
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    fileUrl.value = URL.createObjectURL(blob)
    window.open(fileUrl.value, '_blank')
  } catch (error) {
    console.error('Error al obtener el archivo:', error)
    toast.error('No se pudo cargar el archivo', error)
  }
}

const viewCertificado = async (legajoId) => {
  const token = authStore.getToken()
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/certificado/ver_documento/${legajoId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      },
    )

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.message || 'El documento no existe, prueba generar uno primero')
    }
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
  } catch (error) {
    console.error('Error al obtener el documento:', error)
    toast.error(error.message || 'El documento no existe, prueba generar uno primero')
  }
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
  fetchDocumentos()
})

watch([tipo_documento, currentPage, area, empresa, fecha, ensayo], () => {
  fetchDocumentos()
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
