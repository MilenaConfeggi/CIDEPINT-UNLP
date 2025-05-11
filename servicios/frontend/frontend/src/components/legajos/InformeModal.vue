<template>
  <div class="modal-backdrop" v-if="isOpen" role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <div class="modal-content">
      <div class="modal-header">
        <h2 id="modal-title" class="modal-title">Detalles del Informe</h2>
        <button class="close-button" @click="closeModal" aria-label="Cerrar modal">×</button>
      </div>
      <div class="modal-body">
        <!-- Mostrar lista de informes agrupados -->
        <div v-if="informesAgrupados && Object.keys(informesAgrupados).some(key => informesAgrupados[key].length > 0)">
          <div v-for="(informes, categoria) in informesAgrupados" :key="categoria" class="category-section">
            <h3 class="category-title">{{ categoria }}</h3>
            <ul class="document-list">
              <li v-for="informe in informes" :key="informe.id" class="document-item">
                <button type="button" class="btn btn-link document-button" @click="verInforme(informe.id)">
                    {{ informe.nombre_documento }}
                </button>
                </li>
            </ul>
          </div>
        </div>

        <!-- Botones para subir documentos -->
        <div class="upload-section">
          <h3 class="section-title">Acciones</h3>
          <ul class="action-list">
            <li v-if="hasPermission('cargar_documentacion')" class="action-item">
              <label :for="`upload-doc-${documentoId}`" class="action-button">
                Subir Documentación
                <input
                  :id="`upload-doc-${documentoId}`"
                  type="file"
                  accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
                  @change="handleUploadDocumentacion"
                  hidden
                />
              </label>
            </li>
            <li v-if="hasPermission('cargar_informe')" class="action-item">
              <label :for="`upload-informe-${documentoId}`" class="action-button">
                Subir Informe
                <input
                  :id="`upload-informe-${documentoId}`"
                  type="file"
                  accept="application/pdf"
                  @change="handleUploadInforme"
                  hidden
                />
              </label>
            </li>
            <li v-if="hasPermission('cargar_informe_firmado')" class="action-item">
              <label :for="`upload-informe-firmado-${documentoId}`" class="action-button">
                Subir Informe Firmado
                <input
                  :id="`upload-informe-firmado-${documentoId}`"
                  type="file"
                  accept="application/pdf"
                  @change="handleUploadInformeFirmado"
                  hidden
                />
              </label>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useInformeStore } from '../../stores/informe';
import { storeToRefs } from 'pinia';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '../../stores/auth';

const props = defineProps({
  isOpen: Boolean,
  legajoId: Number,
  documentoId: Number,
  hasPermission: Function,
});

const emit = defineEmits(['close']);

const informeStore = useInformeStore();
const { informesAgrupados } = storeToRefs(informeStore);
const { uploadInforme, uploadInformeFirmado, uploadDocumentacion } = informeStore;
const { verInforme } = informeStore;
const closeModal = () => {
  emit('close');
};

const fetchInformes = async () => {
  try {
    const token = useAuthStore().getToken();
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/informes/ver_todos_informes/${props.legajoId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (response.status === 200) {
      const data = response.data;
      informesAgrupados.value = {
        DOCUMENTACIONES: data.DOCUMENTACIONES || [],
        INFORMES: data.INFORMES || [],
        INFORMES_FIRMADOS_JA: data.INFORMES_FIRMADOS_JA || [],
        INFORMES_FIRMADOS_DIRECTOR: data.INFORMES_FIRMADOS_DIRECTOR || [],
      };
    }
  } catch (error) {
    console.error('Error al obtener los informes:', error);
    useToast().error('Error al obtener los informes');
  }
};

watch(
  () => props.isOpen,
  async (newVal) => {
    if (newVal) {
      console.log('Modal abierto, obteniendo informes...');
      await fetchInformes();
    }
  }
);

const handleUploadDocumentacion = async (event) => {
  console.log('Subiendo documentación...');
  try {
    await uploadDocumentacion(event, props.documentoId, props.legajoId);
    console.log('Documentación subida correctamente');
    await fetchInformes();
  } catch (error) {
    console.error('Error al subir documentación:', error);
  }
};

const handleUploadInforme = async (event) => {
  console.log('Subiendo informe...');
  try {
    await uploadInforme(event, props.documentoId, props.legajoId);
    console.log('Informe subido correctamente');
    await fetchInformes();
  } catch (error) {
    console.error('Error al subir informe:', error);
  }
};

const handleUploadInformeFirmado = async (event) => {
  try {
    await uploadInformeFirmado(event, props.documentoId, props.legajoId);
    await fetchInformes();
  } catch (error) {
    console.error('Error al subir informe firmado:', error);
  }
};
</script>

<style scoped>
/* Fondo del modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

/* Contenido del modal */
.modal-content {
  background: #ffffff;
  border-radius: 10px;
  width: 90%;
  max-width: 700px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease-in-out;
}

/* Encabezado del modal */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

/* Botón de cierre */
.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.close-button:hover {
  color: #000;
}

/* Cuerpo del modal */
.modal-body {
  margin-top: 20px;
}

.category-section {
  margin-bottom: 20px;
}

.category-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #555;
  margin-bottom: 10px;
}

.document-list {
  list-style: none;
  padding: 0;
}

.document-item {
  margin-bottom: 5px;
}

.document-button {
  color: #007bff;
  text-decoration: none;
  font-size: 1rem;
}

.document-button:hover {
  text-decoration: underline;
}

/* Sección de acciones */
.upload-section,
.action-section {
  margin-top: 20px;
}

.section-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #555;
  margin-bottom: 10px;
}

.action-list {
  list-style: none;
  padding: 0;
}

.action-item {
  margin-bottom: 10px;
}

.action-button {
  display: inline-block;
  color: #007bff;
  cursor: pointer;
}

.action-button:hover {
  text-decoration: underline;
}

/* Pie del modal */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-success {
  background-color: #28a745;
  color: #fff;
  border: none;
}

.btn-success:hover {
  background-color: #218838;
}

/* Animación */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>