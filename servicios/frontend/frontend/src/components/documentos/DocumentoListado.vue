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
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Nro de legajo</th>
            <th scope="col">Nro de presupuesto</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="documento in documentos.items" :key="documento.id">
            <th scope="row">{{ documento?.nombre_documento }}</th>
            <td>{{ documento?.legajo_id }}</td>
            <td>{{ documento?.tipo_documento?.nombre }}</td>
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
              <RouterLink :to="`/`" class="btn btn-primary ml-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                  <path
                    fill="currentColor"
                    d="m12 16l-5-5l1.4-1.45l2.6 2.6V4h2v8.15l2.6-2.6L17 11zm-6 4q-.825 0-1.412-.587T4 18v-3h2v3h12v-3h2v3q0 .825-.587 1.413T18 20z"
                  />
                </svg>
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
    <div v-else>No hay Documentos</div>
  </div>
  <div
    class="modal fade"
    id="exampleModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            {{ actualFile?.nombre_documento }}
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div v-if="fileUrl" style="height: 100vh">
            <vue-pdf-app :pdf="fileUrl" :page-number="1" :page-scale="page - fit"></vue-pdf-app>
          </div>
          <div v-else>
            <p>No se encontro el archivo</p>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Descargar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VuePdfApp from 'vue3-pdf-app'
import 'vue3-pdf-app/dist/icons/main.css'
export default {
  components: {
    VuePdfApp,
  },
}
</script>

<script setup>
import { onMounted, watch } from 'vue'
import { useDocumentosStore } from '../../stores/documentos'
import { useAreasStore } from '@/stores/areas'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

const documentosStore = useDocumentosStore()
const areasStore = useAreasStore()
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
}

const fetchAreas = async () => {
  await areasStore.getAreas()
}

const viewFile = async (doc) => {
  actualFile.value = doc
  const tipo = doc.tipo_documento.nombre
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/api/documentos/view/${actualFile.value.nombre_documento}`,
      {
        params: { tipo },
        responseType: 'blob',
      },
    )

    // Crear una URL para visualizar el archivo
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    fileUrl.value = URL.createObjectURL(blob)
  } catch (error) {
    console.error('Error al obtener el archivo:', error)
    alert('No se pudo cargar el archivo.')
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

onMounted(() => {
  fetchAreas()
  fetchDocumentos()
})

watch([tipo_documento, currentPage, area, empresa, fecha, ensayo], () => {
  fetchDocumentos()
})
</script>
