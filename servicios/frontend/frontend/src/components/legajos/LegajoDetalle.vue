<template>
  <main>
    <RouterLink to="/legajos" class="back-button">
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
    <div class="d-flex justify-content-center align-items-center rounded p-4 m-4">
      <p v-if="loading">Cargando...</p>
      <p v-if="error">{{ error }}</p>
      <p v-if="!legajo && !loading">No se encontró el legajo</p>
      <div v-else class="card border-dark text-center w-75">
        <div class="card-header">
          <StateBadge v-if="legajo.estado" :state="legajo.estado?.nombre" />
        </div>
        <div class="card-body">
          <h1 class="card-title">LEG_{{ legajo.id }}/{{ legajo.fecha_entrada ? legajo.fecha_entrada.substring(2, 4) : '' }}</h1>
          <span v-if="isAdmin" class="badge rounded-pill text-bg-dark">{{ legajo.area?.nombre }}</span>
          <div class="row row-cols-2">
            <p class="col">Objetivo: {{ legajo.objetivo }}</p>
            <p class="col" v-if="legajo.necesita_facturacion">Necesita facturación</p>
            <p class="col" v-else>No necesita facturación</p>
            <p class="col" v-if="legajo.es_juridico">No requiere presupuesto</p>
            <p class="col" v-else>Requiere presupuesto</p>
            <p class="col" v-if="legajo.motivo_cancelacion">
              Motivo de cancelación: {{ legajo.motivo_cancelacion }}
            </p>
          </div>
          <hr class="" />
          <div v-if="legajo.cliente">
            <h1 class="text-center">Cliente</h1>
            <div class="row row-cols-2">
              <p class="col">Nombre: {{ legajo.cliente.nombre }}</p>
              <p class="col">CUIT: {{ legajo.cliente.cuit }}</p>
              <p class="col">Email: {{ legajo.cliente.email }}</p>
              <p class="col">Contacto telefónico: {{ legajo.cliente.telefono }}</p>
            </div>
          </div>
          <div class="d-flex justify-content-center gap-3 mb-2">
            <button
              v-if="
                !legajo.admin_habilitado &&
                existeDocumento('Presupuesto CIDEPINT') &&
                existeDocumento('Presupuesto CONICET')
              "
              class="btn btn-dark"
              @click="adminLegajo"
            >
              Habilitar para administración
            </button>
          </div>
          <div v-if="legajo && tipos_documentos?.length">
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">Documentación</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody class="table-group-divider">
                <tr v-for="documento in tipos_documentos" :key="documento.id">
                  <td>{{ documento.nombre }}</td>
                  <td>
                    <div class="dropdown">
                      <button
                          :class="['btn dropdown-toggle', existeDocumento(documento.nombre) ? 'btn-success' : 'btn-dark']"
                          type="button"
                          :data-bs-toggle="documento.nombre === 'Informe' || documento.nombre === 'Presupuesto CIDEPINT' ? '' : 'dropdown'"
                          aria-expanded="false"
                          @click="documento.nombre === 'Informe' ? openModal(documento.id) : documento.nombre === 'Presupuesto CIDEPINT' ? openPresupuestoModal() : handleInformeDropdown(documento.nombre)"
                      >
                        Acciones
                      </button>
                      <ul v-if="documento.nombre !== 'Informe' && documento.nombre !== 'Presupuesto CIDEPINT'" class="dropdown-menu">
                        <template v-if="documento.nombre === 'Certificado CIDEPINT'">
                          <li v-if="hasPermission('generar_certificado')">
                            <RouterLink
                              :to="`/generar_certificado/${legajo.id}`"
                              class="dropdown-item"
                            >
                              Generar
                            </RouterLink>
                          </li>
                          <li
                            v-if="hasPermission('ver_certificado') && existeDocumento(documento.nombre)"
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
                        <template v-else-if="documento.nombre === 'Presupuesto CIDEPINT'">
                          <button
                            type="button"
                            class="btn dropdown-toggle"
                            @click="openPresupuestoModal"
                          >
                            Acciones
                          </button>
                        </template>
                        <template v-else-if="documento.nombre === 'Legajo'">
                          <li>
                            <button
                              type="button"
                              class="dropdown-item"
                              @click="viewLegajo(legajo.id)"
                            >
                              Ver
                            </button>
                          </li>
                        </template>
                        <template v-else-if="documento.nombre === 'Adicional'">
                          <li
                            v-for="adicional in adicionales"
                            :key="adicional.id"
                            class="dropdown-item"
                            @click="viewAdicional(adicional.id)"
                          >
                            {{ adicional.nombre_documento }}
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
                          <li v-if="existeDocumento(documento.nombre) && documento.nombre !== 'Orden Facturación'">
                            <label :for="`edit-pdf-${documento.id}`" class="dropdown-item">
                              Editar
                              <input
                                :id="`edit-pdf-${documento.id}`"
                                type="file"
                                accept="application/pdf"
                                @change="handleFileUpload($event, documento.id, legajo.id, true)"
                                hidden
                              />
                            </label>
                          </li>
                        </template>
                        <template
                          v-if="
                            documento.nombre !== 'Informe' &&
                            documento.nombre !== 'Certificado CIDEPINT' &&
                            documento.nombre !== 'Presupuesto CIDEPINT' &&
                            documento.nombre !== 'Factura' &&
                            documento.nombre !== 'Adicional' &&
                            documento.nombre !== 'Legajo' &&
                            documento.nombre !== 'Orden Facturación'
                          "
                        >
                          <li v-if="!existeDocumento(documento.nombre)">
                            <label :for="`upload-pdf-${documento.id}`" class="dropdown-item">
                              Cargar
                              <input
                                :id="`upload-pdf-${documento.id}`"
                                type="file"
                                accept="application/pdf"
                                @change="handleFileUpload($event, documento.id, legajo.id)"
                                hidden
                              />
                            </label>
                          </li>
                        </template>
                        <template v-if="documento.nombre === 'Factura'">
                          <li v-if="!existeDocumento(documento.nombre)">
                            <button
                              data-bs-toggle="modal"
                              data-bs-target="#exampleModal3"
                              class="dropdown-item"
                              @click="cargarFactura(documento.id)"
                            >
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
        <div class="card-footer">
          <p>Fecha entrada: {{ formatDate(legajo.fecha_entrada) }}</p>
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
              :placeholder="`Ingrese el número de la factura`"
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
    <InformeModal
      :isOpen="isModalOpen"
      :legajoId="legajo.id"
      :documentoId="selectedDocumentoId"
      :hasPermission="hasPermission"
      @close="closeModal"
    />
    <PresupuestoModal
      :isOpen="isPresupuestoModalOpen"
      :legajoId="legajo.id"
      :hasPermission="hasPermission"
      @close="closePresupuestoModal"
    />
  </main>
</template>

<script setup>
import InformeModal from './InformeModal.vue';
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useLegajosStore } from '../../stores/legajos'
import { useDocumentosStore } from '../../stores/documentos'
import { useInformeStore } from '../../stores/informe'
import { usePresupuestoStore } from '../../stores/presupuesto'
import { storeToRefs } from 'pinia'
import { useToast } from 'vue-toastification'
import axios from 'axios'
import StateBadge from '../StateBadge.vue'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'
import PresupuestoModal from '../presupuestos/PresupuestoModal.vue';
const route = useRoute()
const router = useRouter()
const legajosStore = useLegajosStore()
const documentosStore = useDocumentosStore()
const informeStore = useInformeStore()
const presupuestoStore = usePresupuestoStore()
const toast = useToast()

const { legajo, loading, error } = storeToRefs(legajosStore)
const { tipos_documentos } = storeToRefs(documentosStore)
const { successMessage, errorMessage, showToast } = storeToRefs(informeStore)
const {
  uploadInforme,
  uploadInformeFirmado,
  verInforme,
  uploadDocumentacion,
  verDocumentacion,
  enviarInforme,
} = informeStore
const { uploadPresupuestoFirmado, viewPresupuesto } = presupuestoStore
const actualFile = ref(null)
const fileName = ref(null)
const fileUrl = ref(null)
const authStore = useAuthStore()
const permisos = JSON.parse(localStorage.getItem('permisos')) || []
const isAdmin = ref(localStorage.getItem('area') === 'null')
const isModalOpen = ref(false);
const selectedDocumentoId = ref(null);

const openModal = (documentoId) => {
  selectedDocumentoId.value = documentoId;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedDocumentoId.value = null;
};
const isPresupuestoModalOpen = ref(false);

const openPresupuestoModal = () => {
  isPresupuestoModalOpen.value = true;
};

const closePresupuestoModal = () => {
  isPresupuestoModalOpen.value = false;
};
const hasPermission = (permiso) => {
  return permisos.includes(permiso)
}
const nroFactura = ref('')
const documentoID = ref('')
const adicionales = ref([])

const presupuestont = ref('')

const formatDate = (dateString) => {
  const options = { year: 'numeric', day: '2-digit', month: '2-digit' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const cargarFactura = (id) => {
  documentoID.value = id
}

const handleInformeDropdown = async (documentoNombre) => {
  if (documentoNombre === 'Informe' && informes.value.length === 0) {
    await fetchInformes(route.params.id);
  }
};
const handleFileUpload = async (event, id, legajoId, editar = false) => {
  const file = event.target.files[0]
  if (file && file.type === 'application/pdf') {
    try {
      fileName.value = file.name
      let facturaNumber = nroFactura.value
      const response = await documentosStore.subirArchivo(file, id, legajoId, editar, facturaNumber)
      if (response.status === 200) {
        toast.success('Archivo subido correctamente')
        setTimeout(() => {
          window.location.reload()
        }, 2000)
      } else {
        throw new Error('No se pudo subir el archivo')
      }
    } catch (error) {
      console.error('Error al subir el archivo:', error)
      toast.error('Error al subir el archivo', error)
    }
  } else {
    toast.warning('Por favor selecciona un archivo PDF.')
  }
}
const existeDocumento = (nombreDocumento) => {
  return legajo.value.documento?.some((doc) => doc.tipo_documento.nombre === nombreDocumento)
}

const viewFile = async (id, tipo) => {
  actualFile.value = legajo.value.documento.find((doc) => doc.tipo_documento_id === id)
  try {
    const token = authStore.getToken()
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/api/documentos/view/${actualFile.value.nombre_documento}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
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
    toast.warning('No se pudo cargar el archivo.') 
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

    if (response.status !== 200) {
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

const fetchAdicionales = async (legajoId) => {
  const token = authStore.getToken()
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/api/documentos/adicionales/${legajoId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
    if (response.status !== 200) {
      throw ({message: 'Error al obtener los documentos adicionales', status: response.status})
    }
    adicionales.value = response.data
  } catch (error) {
    if (error.status === 422 || error.status === 401) {
      authStore.logout()
      router.push('/log-in')
    } else {
      toast.error('Error al obtener los documentos adicionales', error)
    }
    console.error('Error al obtener los documentos adicionales:', error)
  }
}

const fetchSinPresupuesto = async (legajoId) => {
  const token = authStore.getToken()
  if (!hasPermission('generar_presupuestont')) {
    return
  }
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/presupuestos/sin_presu/${legajoId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
    if (response.status !== 200) {
      throw ({message: 'Error al obtener el presupuesto', status: response.status})
    }
    presupuestont.value = response.data
    console.log(presupuestont)
  } catch (error) {
    if (error.status === 422 || error.status === 401) {
      authStore.logout()
      router.push('/log-in')
    } else {
      toast.error('Error al obtener el presupuesto', error)
    }
    console.error('Error al obtener presupuesto:', error)
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
    toast.warning('No se pudo cargar el archivo adicional.')
  }
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
const informes = ref([]);

const informesAgrupados = ref({
  DOCUMENTACIONES: [],
  INFORMES: [],
  INFORMES_FIRMADOS_JA: [],
  INFORMES_FIRMADOS_DIRECTOR: [],
});


// Llamar a `fetchInformes` al montar el componente
onMounted(async () => {
  await fetchInformes(route.params.id);
});
const adminLegajo = async () => {
  await legajosStore.habilitar(route.params.id)
}

onMounted(async () => {
  try {
    await legajosStore.getLegajo(route.params.id)
    await documentosStore.getTiposDocumentos()
    await fetchAdicionales(route.params.id)
    await fetchSinPresupuesto(route.params.id)
  } catch (err) {
    console.error('Error al cargar el legajo:', err)
    toast.error('Error al cargar el legajo', err)
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

.dropdown-item input[type='file'] {
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
.small-title {
  font-size: 1rem; /* Ajusta el tamaño del texto */
  font-weight: normal; /* Opcional: cambia el peso de la fuente */
  margin-bottom: 0.5rem; /* Opcional: ajusta el margen inferior */
}
</style>
