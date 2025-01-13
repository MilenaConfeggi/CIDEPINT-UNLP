import axios from 'axios'
import { defineStore } from 'pinia'
import { useToast } from 'vue-toastification'
import { useAuthStore } from './auth'
import { useEncuestasStore } from './encuestas'
import { useLegajosStore } from './legajos'

export const useInformeStore = defineStore('informe', {
  state: () => ({
    successMessage: '',
    errorMessage: '',
    showToast: false,
  }),
  actions: {
    async uploadInforme(event, id, legajoId) {
      const toast = useToast()
      const file = event.target.files[0]
      const token = useAuthStore().getToken()
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
            toast.success('Informe subido correctamente')
            setTimeout(() => window.location.reload(), 2000)
          } else {
            throw new Error(response.data.error || 'No se pudo subir el archivo')
          }
        } catch (error) {
          console.error('Error al subir el archivo:', error)
          toast.error(error.response?.data?.error || 'Error al subir el archivo')
        }
      } else {
        toast.warning('Por favor selecciona un archivo PDF.')
      }
    },
    async uploadInformeFirmado(event, id, legajoId) {
      const toast = useToast()
      const file = event.target.files[0]
      const token = useAuthStore().getToken()
      if (file && file.type === 'application/pdf') {
        try {
          const formData = new FormData()
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
            toast.success('Informe firmado subido correctamente')
            setTimeout(() => window.location.reload(), 2000)
          } else {
            throw new Error(response.data.error || 'No se pudo subir el archivo')
          }
        } catch (error) {
          console.error('Error al subir el archivo:', error)
          toast.error(error.response?.data?.error || 'Error al subir el archivo')
        }
      } else {
        toast.warning('Por favor selecciona un archivo PDF.')
      }
    },
    async verInforme(id) {
      const token = useAuthStore().getToken()
      const toast = useToast()
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
        toast.error(error.message || 'Error al obtener el informe')
      }
    },
    async uploadDocumentacion(event, id, legajoId) {
      const toast = useToast()
      const file = event.target.files[0]
      const token = useAuthStore().getToken()
      const allowedTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
      ]
      if (file && allowedTypes.includes(file.type)) {
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
            toast.success('Documentación subida correctamente')
            setTimeout(() => window.location.reload(), 2000)
          } else {
            throw new Error(response.data.error || 'No se pudo subir el archivo')
          }
        } catch (error) {
          console.error('Error al subir el archivo:', error)
          toast.error(error.response?.data?.error || 'Error al subir el archivo')
        }
      } else {
        toast.warning('Por favor selecciona un archivo PDF, Word, Excel o PowerPoint.')
      }
    },
    async verDocumentacion(id) {
      const token = useAuthStore().getToken()
      const toast = useToast()
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
        toast.error(error.message || 'Error al obtener el documento')
      }
    },
    async enviarInforme(id, leg_id) {
      const toast = useToast()
      const legajosStore = useLegajosStore()
      const encuestasStore = useEncuestasStore()
      const legajo = legajosStore.legajo
      console.log(legajo)
      let archivo = legajo?.documento?.find((doc) => doc.tipo_documento_id === id)
      const legajoId = leg_id
      try {
        toast.info('Mandando correo...')
        await encuestasStore.createEncuestas()
        const link = encuestasStore.link
        await encuestasStore.mandarMail(legajo?.cliente?.email, link, archivo.id, legajoId)
        toast.success('Correo enviado con éxito')
      } catch (error) {
        console.error('Error al enviar el correo:', error)
        toast.error(error.message || 'Error al enviar el correo')
      }
    },
  },
})