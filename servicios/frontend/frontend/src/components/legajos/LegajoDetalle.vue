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
        <p>LEG_{{ legajo.id }}</p>
        <StateBadge v-if="legajo.estado" :state="legajo.estado?.nombre" />
        <p>Fecha entrada: {{ formatDate(legajo.fecha_entrada) }}</p>
        <p>Objetivo: {{ }}</p>
        <div v-if="legajo.cliente">
          <h6>Cliente</h6>
          <p>{{ legajo.cliente.nombre }}</p>
          <p>CUIT: {{ legajo.cliente.cuit }}</p>
        </div>

        <div v-if="legajo && tipos_documentos?.length ">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">Documentacion</th>
                <th scope="col">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="documento in tipos_documentos" :key="documento.id">
                <td>{{ documento.nombre }}</td>
                <td>
                  <div class="dropdown">
                    <button
                      class="btn btn-secondary dropdown-toggle"
                      type="button"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      Acciones
                    </button>
                    <ul class="dropdown-menu">
                      <template v-if="existeDocumento(documento.nombre)"> 
                        <li>
                          <button
                            type="button"
                            class="dropdown-item"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal"
                          >
                            Ver documento
                          </button>
                        </li>
                        <li>
                          <button type="button" class="dropdown-item" @click="downloadDocumento(documento.id, legajo.id)">
                            Descargar
                          </button>
                        </li>
                        <li><a class="dropdown-item" href="#">Editar</a></li>
                      </template>
                      <li v-else>
                        <label for="upload-pdf" class="dropdown-item">
                          Cargar
                          <input
                            id="upload-pdf"
                            type="file"
                            accept="application/pdf"
                            @change="handleFileUpload($event, documento.id, legajo.id)"
                            class="dropdown-item"
                            hidden
                          />
                        </label>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">...</div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Save changes</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showToast" class="toast-container position-fixed bottom-0 end-0 p-3">
        <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
          <div class="toast-header">
            <strong class="me-auto">Archivo Cargado</strong>
            <button type="button" class="btn-close" @click="showToast = false" aria-label="Close"></button>
          </div>
          <div class="toast-body">
            El archivo se cargó correctamente.
          </div>
        </div>
      </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useLegajosStore } from '../../stores/legajos'
import { useDocumentosStore } from '../../stores/documentos'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'
import StateBadge from '../StateBadge.vue'

const route = useRoute()
const legajosStore = useLegajosStore()
const documentosStore = useDocumentosStore()

const { legajo, loading, error } = storeToRefs(legajosStore)
const { tipos_documentos } = storeToRefs(documentosStore)
const showToast = ref(false)
const fileName = ref(null)

const formatDate = (dateString) => {
  const options = { year: 'numeric', day: '2-digit', month: '2-digit' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}
const handleFileUpload = async (event, id, legajoId) => {
  const file = event.target.files[0]
  if (file && file.type === 'application/pdf') {
    try {
      fileName.value = file.name 
      const response = await documentosStore.subirArchivo(file, id, legajoId)
      console.log(response)
      showToast.value = true
    } catch (error) {
      console.error('Error al subir el archivo:', error)
      alert('Ocurrió un error al subir el archivo. Inténtelo nuevamente.')
    }
  } else {
    alert('Por favor selecciona un archivo PDF.')
  }
}

const existeDocumento = (nombreDocumento) => {
      return legajo.value.documento.some(
        (doc) => doc.tipo_documento.nombre === nombreDocumento
      );
}

const downloadDocumento = async (tipo, legajo_id) => {
  const nombreDocumento = legajo.value.documento.find((doc) => doc.tipo_documento_id === tipo).nombre_documento
  const response = await documentosStore.download(nombreDocumento, tipo, legajo_id)
  console.log(response)
}



onMounted(async () => {
  try {
    await legajosStore.getLegajo(route.params.id)
    await documentosStore.getTiposDocumentos()
  } catch (err) {
    console.error('Error al cargar el legajo:', err)
  }
})
</script>
