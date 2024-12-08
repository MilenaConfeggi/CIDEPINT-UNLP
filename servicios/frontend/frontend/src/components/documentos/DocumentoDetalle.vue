<template>
  <div v-if="doc">
    <p>Nombre del documento: {{ doc.nombre_documento }}</p>
    <button @click="viewFile(doc.nombre_documento, doc.tipo_documento)">Ver Archivo</button> 
  <div v-if="fileUrl" class="file-preview">
      <iframe :src="fileUrl" frameborder="0" width="100%" height="600px"></iframe>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useDocumentosStore } from '../../stores/documentos'
import { storeToRefs } from 'pinia'

const props = defineProps({
  id: {
    type: Number,
    required: true,
  }
})

const documentosStore = useDocumentosStore()
const { doc } = storeToRefs(documentosStore)
const fileUrl = ref(null)

onMounted(async () => {
  await documentosStore.getDocumento(props.id)
})

const viewFile = async (filename, tipo) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/view/${filename}`, {
      params: { tipo },
      responseType: 'blob', // Importante para manejar archivos binarios
    })

    // Crear una URL para visualizar el archivo
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    fileUrl.value = URL.createObjectURL(blob)
  } catch (error) {
    console.error('Error al obtener el archivo:', error)
    alert('No se pudo cargar el archivo.')
  }
}
</script>

<style>
.file-preview {
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}
</style>
