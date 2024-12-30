<template>
  <main>
    <RouterLink to="/legajos" class="back-button">
      <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24">
        <g fill="none">
          <path d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z" />
          <path fill="black" d="M3.283 10.94a1.5 1.5 0 0 0 0 2.12l5.656 5.658a1.5 1.5 0 1 0 2.122-2.122L7.965 13.5H19.5a1.5 1.5 0 0 0 0-3H7.965l3.096-3.096a1.5 1.5 0 1 0-2.122-2.121z" />
        </g>
      </svg>
    </RouterLink>
    <div class="d-flex justify-content-center align-items-center border-2 border-blue-500 rounded-lg p-4 m-4">
      <p v-if="loading">Cargando...</p>
      <p v-if="error">{{ error }}</p>
      <p v-if="!legajo && !loading">No se encontró el legajo</p>
      <div v-else class="w-100">
        <div class="d-flex flex-column justify-content-center align-items-center">
          <h1 class="text-center">LEG_{{ legajo.id }}</h1>
          <StateBadge v-if="legajo.estado" :state="legajo.estado?.nombre" />
        </div>
        <p>Fecha entrada: {{ formatDate(legajo.fecha_entrada) }}</p>
        <p>Objetivo: {{ legajo.objetivo }}</p>
        <hr class="">
        <div v-if="legajo.cliente">
          <h1 class="text-center">Cliente</h1>
          <p>{{ legajo.cliente.nombre }}</p>
          <p>CUIT: {{ legajo.cliente.cuit }}</p>
        </div>
        <div class="d-flex justify-content-end gap-3 mb-2">
          <button v-if="!legajo.admin_habilitado" class="btn btn-dark" @click="adminLegajo">
            Habilitar para administración
          </button>
        </div>
        <div v-if="legajo && tipos_documentos?.length">
          <table class="table w-100">
            <thead>
              <tr>
                <th scope="col">Documentación</th>
                <th scope="col">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="documento in tipos_documentos" :key="documento.id">
                <td>{{ documento.nombre }}</td>
                <td>
                  <div class="dropdown">
                    <button class="btn btn-dark dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                      Acciones
                    </button>
                    <ul class="dropdown-menu">
                      <template v-if="documento.nombre === 'Informe'">
                        <li v-if="hasPermission('cargar_documentacion')">
                          <label :for="`upload-doc-${documento.id}`" class="dropdown-item">
                            Subir Documentación
                            <input :id="`upload-doc-${documento.id}`" type="file" accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx" @change="uploadDocumentacion($event, documento.id, legajo.id)" hidden />
                          </label>
                        </li>
                        <li v-if="hasPermission('ver documentacion')">
                          <button type="button" class="dropdown-item" @click="verDocumentacion(legajo.id)">
                            Ver Documentación
                          </button>
                        </li>
                        <li v-if="hasPermission('cargar_informe')">
                          <label :for="`upload-informe-${documento.id}`" class="dropdown-item">
                            Subir Informe
                            <input :id="`upload-informe-${documento.id}`" type="file" accept="application/pdf" @change="uploadInforme($event, documento.id, legajo.id)" hidden />
                          </label>
                        </li>
                        <li v-if="hasPermission('ver informe')">
                          <button type="button" class="dropdown-item" @click="verInforme(legajo.id)">
                            Ver Informe
                          </button>
                        </li>
                        <li v-if="hasPermission('cargar_informe_firmado')">
                          <label :for="`upload-informe-firmado-${documento.id}`" class="dropdown-item">
                            Subir Informe Firmado
                            <input :id="`upload-informe-firmado-${documento.id}`" type="file" accept="application/pdf" @change="uploadInformeFirmado($event, documento.id, legajo.id)" hidden />
                          </label>
                        </li>
                        <li v-if="legajo?.estado?.nombre === 'Informado'">
                          <button type="button" class="dropdown-item" @click="enviarInforme(documento.id)">
                            Enviar Informe
                          </button>
                        </li>
                      </template>
                      <template v-else-if="documento.nombre === 'Certificado CIDEPINT'">
                        <li v-if="hasPermission('generar_certificado')">
                          <RouterLink :to="`/generar_certificado/${legajo.id}`" class="dropdown-item">
                            Generar
                          </RouterLink>
                        </li>
                        <li v-if="hasPermission('ver_certificado') && existeDocumento(documento.nombre)">
                          <button type="button" class="dropdown-item" @click="viewCertificado(documento.id, documento.nombre, legajo.id)">
                            Ver
                          </button>
                        </li>
                      </template>
                      <template v-else-if="documento.nombre === 'Presupuesto CIDEPINT'">
                        <li v-if="hasPermission('generar_presupuesto')">
                          <RouterLink :to="`/generar_presupuesto/${legajo.id}`" class="dropdown-item">
                            Generar
                          </RouterLink>
                        </li>
                        <li v-if="hasPermission('ver_presupuesto') && existeDocumento(documento.nombre)">
                          <button type="button" class="dropdown-item" @click="viewPresupuesto(documento.id, documento.nombre, legajo.id)">
                            Ver
                          </button>
                        </li>
                        <li v-if="hasPermission('cargar_presupuesto_firmado') && existeDocumento(documento.nombre)">
                          <label :for="`upload-presupuesto-firmado-${documento.id}`" class="dropdown-item">
                            Subir Presupuesto Firmado
                            <input :id="`upload-presupuesto-firmado-${documento.id}`" type="file" accept="application/pdf" @change="uploadPresupuestoFirmado($event, documento.id, legajo.id)" hidden />
                          </label>
                        </li>
                      </template>
                      <template v-else-if="documento.nombre === 'adicional'">
                        <li v-for="adicional in adicionales" :key="adicional.id" class="dropdown-item" @click="viewAdicional(adicional.id)">
                          {{ adicional.nombre_documento }}
                        </li>
                      </template>
                      <template v-else>
                        <li v-if="existeDocumento(documento.nombre)">
                          <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#exampleModal" @click="viewFile(documento.id, documento.nombre)">
                            Ver documento
                          </button>
                        </li>
                        <li v-if="existeDocumento(documento.nombre)">
                          <button type="button" class="dropdown-item" @click="downloadDocumento(documento.id, legajo.id)">
                            Descargar
                          </button>
                        </li>
                        <li v-if="existeDocumento(documento.nombre)">
                          <label :for="`edit-pdf-${documento.id}`" class="dropdown-item">
                            Editar
                            <input :id="`edit-pdf-${documento.id}`" type="file" accept="application/pdf" @change="handleFileUpload($event, documento.id, legajo.id, true)" hidden />
                          </label>
                        </li>
                      </template>
                      <template v-if="documento.nombre !== 'Informe' && documento.nombre !== 'Certificado CIDEPINT' && documento.nombre !== 'Presupuesto CIDEPINT' && documento.nombre !== 'Factura' && documento.nombre !== 'adicional'">
                        <li v-if="!existeDocumento(documento.nombre)">
                          <label :for="`upload-pdf-${documento.id}`" class="dropdown-item">
                            Cargar
                            <input :id="`upload-pdf-${documento.id}`" type="file" accept="application/pdf" @change="handleFileUpload($event, documento.id, legajo.id)" hidden />
                          </label>
                        </li>
                      </template>
                      <template v-if="documento.nombre === 'Factura'">
                        <li v-if="!existeDocumento(documento.nombre)">
                          <button data-bs-toggle="modal" data-bs-target="#exampleModal3" class="dropdown-item" @click="cargarFactura(documento.id)">
                            Cargar
                          </button>
                        </li>
                      </template>
                    </ul>
                  </div>
                </td>
              </tr>
              <tr>
                <td>Mails</td>
                <td>
                  <RouterLink :to="`/mails/${legajo.id}`" class="btn btn-primary">Ver Mails</RouterLink>
                </td>
              </tr>
              <tr>
                <td class="">Muestras</td>
                <td>
                  <RouterLink :to="`/muestras/${legajo.id}`" class="btn btn-primary">Ver Muestras</RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="modal fade" id="exampleModal3" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Cargar factura</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <input v-model="nroFactura" :placeholder="`Ingrese el número de la factura`" class="form-control" type="text" />
          </div>
          <div class="modal-footer">
            <input :id="`upload-pdf-${documentoID}`" type="file" accept="application/pdf" @change="handleFileUpload($event, documentoID, legajo.id)" class="btn btn-primary" :hidden="nroFactura === ''" />
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showToast" class="toast-container position-fixed bottom-0 end-0 p-3">
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <strong class="me-auto">{{ errorMessage ? 'Error' : 'Éxito' }}</strong>
          <button type="button" class="btn-close" @click="showToast = false" aria-label="Close"></button>
        </div>
        <div class="toast-body">{{ errorMessage || successMessage }}</div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useLegajosStore } from '../../stores/legajos'
import { useDocumentosStore } from '../../stores/documentos'
import { useEncuestasStore } from '../../stores/encuestas'
import { useInformeStore } from '../../stores/informe'
import { usePresupuestoStore } from '../../stores/presupuesto'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import StateBadge from '../StateBadge.vue'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const legajosStore = useLegajosStore()
const documentosStore = useDocumentosStore()
const encuestasStore = useEncuestasStore()
const informeStore = useInformeStore()
const presupuestoStore = usePresupuestoStore()

const { legajo, loading, error } = storeToRefs(legajosStore)
const { tipos_documentos } = storeToRefs(documentosStore)
const { successMessage, errorMessage, showToast } = storeToRefs(informeStore)
const { uploadInforme, uploadInformeFirmado, verInforme, uploadDocumentacion, verDocumentacion, enviarInforme } = informeStore
const { uploadPresupuestoFirmado, viewPresupuesto, verPresupuestoFirmado } = presupuestoStore
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
const adicionales = ref([])

const formatDate = (dateString) => {
  const options = { year: 'numeric', day: '2-digit', month: '2-digit' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const cargarFactura = (id) => {
  documentoID.value = id
}

const handleFileUpload = async (event, id, legajoId, editar = false) => {
  const file = event.target.files[0]
  console.log(id)
  if (file && file.type === 'application/pdf') {
    try {
      fileName.value = file.name
      let facturaNumber = nroFactura.value
      const response = await documentosStore.subirArchivo(file, id, legajoId, editar, facturaNumber)
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
      `${import.meta.env.VITE_API_URL}/api/documentos/view/${actualFile.value.nombre_documento}`,
      {
        params: { tipo },
        responseType: 'blob',
      },
    )

    // Crear una URL para visualizar el archivo
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    console.log(response.data)
    fileUrl.value = URL.createObjectURL(blob)
    window.open(fileUrl.value, '_blank')
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

const fetchAdicionales = async (legajoId) => {
  const token = authStore.getToken()
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/adicionales/${legajoId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    adicionales.value = response.data
  } catch (error) {
    console.error('Error al obtener los documentos adicionales:', error)
  }
}

const viewAdicional = async (adicionalId) => {
  const token = authStore.getToken()
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/api/documentos/view_adicional/${adicionalId}`,
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
    console.error('Error al obtener el archivo adicional:', error)
    alert('No se pudo cargar el archivo adicional.')
  }
}

const adminLegajo = async () => {
  await legajosStore.habilitar(route.params.id)
}

onMounted(async () => {
  try {
    await legajosStore.getLegajo(route.params.id)
    await documentosStore.getTiposDocumentos()
    await fetchAdicionales(route.params.id)
  } catch (err) {
    console.error('Error al cargar el legajo:', err)
    errorMessage.value = err.message || 'Error al cargar el legajo'
    showToast.value = true
  }
})
</script>
<style scoped>
.back-button {
  display: inline-block;
  margin-bottom: 1rem;
  color: #000;
  text-decoration: none;
}

.back-button:hover {
  color: #007bff;
}

.table th,
.table td {
  vertical-align: middle;
}

.dropdown-toggle::after {
  margin-left: 0.5rem;
}

.dropdown-menu {
  min-width: 200px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  transition: background-color 0.3s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  color: #343a40;
}

.dropdown-item input[type="file"] {
  display: none;
}

.toast-container {
  z-index: 1055;
}

.toast {
  background-color: #fff;
  border: 1px solid #ccc;
}

.toast-header {
  background-color: #007bff;
  color: #fff;
}

.toast-body {
  color: #000;
}

.btn-dark {
  background-color: #343a40;
  border-color: #343a40;
}

.btn-dark:hover {
  background-color: #23272b;
  border-color: #1d2124;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}
</style>