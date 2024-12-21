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
      <div v-else class="w-100">
        <div class="d-flex flex-column justify-content-center align-items-center">
          <h1 class="text-center">LEG_{{ legajo.id }}</h1>
          <StateBadge v-if="legajo.estado" :state="legajo.estado?.nombre" />
        </div>
        <p>Fecha entrada: {{ formatDate(legajo.fecha_entrada) }}</p>
        <p>Objetivo: {{ legajo.objetivo }}</p>
        <hr />
        <div v-if="legajo.cliente">
          <h1 class="text-center">Cliente</h1>
          <p>{{ legajo.cliente.nombre }}</p>
          <p>CUIT: {{ legajo.cliente.cuit }}</p>
        </div>
        <EncuestaGenerator />
        <button v-if="!legajo.admin_habilitado" class="btn btn-dark" @click="adminLegajo">
          Habilitar para administración
        </button>
        <div v-if="legajo && tipos_documentos?.length">
          <table class="table w-100">
            <thead>
              <tr>
                <th scope="col">Documentacion</th>
                <th scope="col">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="documento in tipos_documentos" :key="documento.id">
                <td >{{ documento.nombre }}</td>
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
                      <template v-if="documento.nombre === 'Informe'">
                        <li v-if="hasPermission('cargar_documentacion')">
                          <label :for="`upload-doc-${documento.id}`" class="dropdown-item">
                            Subir Documentacion
                            <input
                              :id="`upload-doc-${documento.id}`"
                              type="file"
                              accept="application/pdf"
                              @change="uploadDocumentacion($event, documento.id, legajo.id)"
                              class="dropdown-item"
                              hidden
                            />
                          </label>
                        </li>
                        <li v-if="hasPermission('ver documentacion')">
                          <button
                            type="button"
                            class="dropdown-item"
                            @click="verDocumentacion(legajo.id)"
                          >
                            Ver Documentacion
                          </button>
                        </li>
                        <li v-if="hasPermission('cargar_informe')">
                          <label :for="`upload-informe-${documento.id}`" class="dropdown-item">
                            Subir Informe
                            <input
                              :id="`upload-informe-${documento.id}`"
                              type="file"
                              accept="application/pdf"
                              @change="uploadInforme($event, documento.id, legajo.id)"
                              class="dropdown-item"
                              hidden
                            />
                          </label>
                        </li>
                        <li v-if="hasPermission('ver informe')">
                          <button
                            type="button"
                            class="dropdown-item"
                            @click="verInforme(legajo.id)"
                          >
                            Ver Informe
                          </button>
                        </li>
                        <li v-if="hasPermission('cargar_informe_firmado')">
                          <label
                            :for="`upload-informe-firmado-${documento.id}`"
                            class="dropdown-item"
                          >
                            Subir Informe Firmado
                            <input
                              :id="`upload-informe-firmado-${documento.id}`"
                              type="file"
                              accept="application/pdf"
                              @change="uploadInformeFirmado($event, documento.id, legajo.id)"
                              class="dropdown-item"
                              hidden
                            />
                          </label>
                        </li>
                      </template>
                      <template v-else-if="documento.nombre === 'Certificado CIDEPINT'">
                        <li v-if="hasPermission('generar_certificado')">
                          <RouterLink
                            :to="`/generar_certificado/${legajo.id}`"
                            class="dropdown-item"
                          >
                            Generar
                          </RouterLink>
                        </li>
                        <li
                          v-if="
                            hasPermission('ver_certificado') && existeDocumento(documento.nombre)
                          "
                        >
                          <button
                            type="button"
                            class="dropdown-item"
                            @click="viewCertificado(documento.id, documento.nombre, legajo.id)"
                          >
                            Ver
                          </button>
                        </li>
                      </template>
                      <template v-else>
                        <li v-if="existeDocumento(documento.nombre)">
                          <button
                            type="button"
                            class="dropdown-item"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal"
                            @click="viewFile(documento.id, documento.nombre)"
                          >
                            Ver documento
                          </button>
                        </li>
                        <li v-if="existeDocumento(documento.nombre)">
                          <button
                            type="button"
                            class="dropdown-item"
                            @click="downloadDocumento(documento.id, legajo.id)"
                          >
                            Descargar
                          </button>
                        </li>
                        <li v-if="existeDocumento(documento.nombre)">
                          <label :for="`edit-pdf-${documento.id}`" class="dropdown-item">
                            Editar
                            <input
                              :id="`edit-pdf-${documento.id}`"
                              type="file"
                              accept="application/pdf"
                              @change="handleFileUpload($event, documento.id, legajo.id, true)"
                              class="dropdown-item"
                              hidden
                            />
                          </label>
                        </li>
                      </template>
                      <li v-if="!existeDocumento(documento.nombre)">
                        <label :for="`upload-pdf-${documento.id}`" class="dropdown-item">
                          <div v-if="documento.nombre !== 'Factura'" class="dropdown-item">
                            Cargar
                            <input
                              :id="`upload-pdf-${documento.id}`"
                              type="file"
                              accept="application/pdf"
                              @change="handleFileUpload($event, documento.id, legajo.id)"
                              class="dropdown-item"
                              hidden
                            />
                          </div>
                          <button
                            v-if="documento.nombre === 'Factura'"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal3"
                            class="dropdown-item"
                            @click="cargarFactura(documento.id)"
                          >
                            Cargar
                          </button>
                        </label>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
              <tr>
                <td>Mails</td>
                <td>
                  <RouterLink :to="`/mails/${legajo.id}`" class="btn btn-primary"
                    >Ver Mails</RouterLink
                  >
                </td>
              </tr>
              <tr>
                <td class="">Muestras</td>
                <td>
                  <RouterLink :to="`/muestras/${legajo.id}`" class="btn btn-primary"
                    >Ver Muestras</RouterLink
                  >
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
              <vue-pdf-app :pdf="fileUrl" :page-number="1"></vue-pdf-app>
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
    <div
      class="modal fade"
      id="exampleModal3"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Cargar factura</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <input
              v-model="nroFactura"
              :placeholder="`Ingrese el numero de la factura`"
              class="form-control"
              type="text"
            />
          </div>
          <div class="modal-footer">
            <input
              :id="`upload-pdf-${documentoID}`"
              type="file"
              accept="application/pdf"
              @change="handleFileUpload($event, documentoID, legajo.id)"
              class="btn btn-primary"
              :hidden="nroFactura === ''"
            />
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showToast" class="toast-container position-fixed bottom-0 end-0 p-3">
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <strong class="me-auto">{{ errorMessage ? 'Error' : 'Éxito' }}</strong>
          <button
            type="button"
            class="btn-close"
            @click="showToast = false"
            aria-label="Close"
          ></button>
        </div>
        <div class="toast-body">{{ errorMessage || successMessage }}</div>
      </div>
    </div>
  </main>
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
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useLegajosStore } from '../../stores/legajos'
import { useDocumentosStore } from '../../stores/documentos'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import StateBadge from '../StateBadge.vue'
import { useAuthStore } from '../../stores/auth'
import EncuestaGenerator from '../EncuestaGenerator.vue'

const route = useRoute()
const legajosStore = useLegajosStore()
const documentosStore = useDocumentosStore()

const { legajo, loading, error } = storeToRefs(legajosStore)
const { tipos_documentos } = storeToRefs(documentosStore)
const showToast = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const actualFile = ref(null)
const fileName = ref(null)
const fileUrl = ref(null)
const authStore = useAuthStore()
const permisos = JSON.parse(localStorage.getItem('permisos')) || []

const hasPermission = (permiso) => {
  return permisos.includes(permiso)
}
const nroFactura = ref('')
const documentoID = ref('')

const formatDate = (dateString) => {
  const options = { year: 'numeric', day: '2-digit', month: '2-digit' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const cargarFactura = (id) => {
  documentoID.value = id
}

const uploadDocumentacion = async (event, id, legajoId) => {
  const file = event.target.files[0]
  const token = authStore.getToken()
  if (file && file.type === 'application/pdf') {
    try {
      const formData = new FormData()
      formData.append('archivo', file)
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/informes/cargar_documentacion/${legajoId}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        },
      )
      console.log(response)
      if (response.status === 200) {
        successMessage.value = 'Documentación subida correctamente'
        showToast.value = true
        setTimeout(() => window.location.reload(), 2000)
      } else {
        throw new Error(response.data.error || 'No se pudo subir el archivo')
      }
    } catch (error) {
      console.error('Error al subir el archivo:', error)
      errorMessage.value = error.response?.data?.error || 'Error al subir el archivo'
      showToast.value = true
    }
  } else {
    alert('Por favor selecciona un archivo PDF.')
  }
}

const uploadInforme = async (event, id, legajoId) => {
  const file = event.target.files[0]
  const token = authStore.getToken()
  if (file && file.type === 'application/pdf') {
    try {
      const formData = new FormData()
      formData.append('archivo', file)
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/informes/cargar_informe/${legajoId}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        },
      )
      console.log(response)
      if (response.status === 200) {
        successMessage.value = 'Informe subido correctamente'
        showToast.value = true
        setTimeout(() => window.location.reload(), 2000)
      } else {
        throw new Error(response.data.error || 'No se pudo subir el archivo')
      }
    } catch (error) {
      console.error('Error al subir el archivo:', error)
      errorMessage.value = error.response?.data?.error || 'Error al subir el archivo'
      showToast.value = true
    }
  } else {
    alert('Por favor selecciona un archivo PDF.')
  }
}

const uploadInformeFirmado = async (event, id, legajoId) => {
  const file = event.target.files[0]
  const token = authStore.getToken()
  if (file && file.type === 'application/pdf') {
    try {
      const formData = new FormData() // Definir formData aquí
      formData.append('archivo', file)
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/informes/cargar_informe_firmado/${legajoId}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        },
      )
      console.log(response)
      if (response.status === 200) {
        successMessage.value = 'Informe firmado subido correctamente'
        showToast.value = true
        setTimeout(() => window.location.reload(), 2000)
      } else {
        throw new Error(response.data.error || 'No se pudo subir el archivo')
      }
    } catch (error) {
      console.error('Error al subir el archivo:', error)
      errorMessage.value = error.response?.data?.error || 'Error al subir el archivo'
      showToast.value = true
    }
  } else {
    alert('Por favor selecciona un archivo PDF.')
  }
}

const handleFileUpload = async (event, id, legajoId, editar = false) => {
  const file = event.target.files[0]
  console.log(id)
  if (file && file.type === 'application/pdf') {
    try {
      fileName.value = file.name
      let facturaNumber = nroFactura.value
      const response = await documentosStore.subirArchivo(file, id, legajoId, editar, facturaNumber)
      console.log(response)
      if (response.status === 200) {
        window.location.reload()
      } else {
        throw new Error('No se pudo subir el archivo')
      }
    } catch (error) {
      console.error('Error al subir el archivo:', error)
      showToast.value = true
    }
  } else {
    alert('Por favor selecciona un archivo PDF.')
  }
}
const existeDocumento = (nombreDocumento) => {
  return legajo.value.documento?.some((doc) => doc.tipo_documento.nombre === nombreDocumento)
}

const downloadDocumento = async (tipo, legajo_id) => {
  actualFile.value = legajo.value.documento.find((doc) => doc.tipo_documento_id === tipo)
  const response = await documentosStore.download(
    actualFile.value.nombre_documento,
    tipo,
    legajo_id,
  )
  console.log(response)
}

const viewFile = async (id, tipo) => {
  actualFile.value = legajo.value.documento.find((doc) => doc.tipo_documento_id === id)
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
    console.log(response.data)
    fileUrl.value = URL.createObjectURL(blob)
  } catch (error) {
    console.error('Error al obtener el archivo:', error)
    alert('No se pudo cargar el archivo.')
  }
}
const viewCertificado = async (id, tipo, legajoId) => {
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
    errorMessage.value = error.message || 'El documento no existe, prueba generar uno primero'
    showToast.value = true
  }
}
const verDocumentacion = async (id) => {
  const token = authStore.getToken()
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/informes/ver_documento/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    })
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.message || 'Error al obtener el documento')
    }
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
  } catch (error) {
    console.error('Error al obtener el documento:', error)
    errorMessage.value = error.message || 'Error al obtener el documento'
    showToast.value = true
  }
}

const verInforme = async (id) => {
  const token = authStore.getToken()
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/informes/ver_informe/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    })
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.message || 'Error al obtener el informe')
    }
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
  } catch (error) {
    console.error('Error al obtener el informe:', error)
    errorMessage.value = error.message || 'Error al obtener el informe'
    showToast.value = true
  }
}

const adminLegajo = async () => {
  await legajosStore.habilitar(route.params.id)
}

onMounted(async () => {
  try {
    await legajosStore.getLegajo(route.params.id)
    await documentosStore.getTiposDocumentos()
  } catch (err) {
    console.error('Error al cargar el legajo:', err)
    errorMessage.value = err.message || 'Error al cargar el legajo'
    showToast.value = true
  }
})
</script>
