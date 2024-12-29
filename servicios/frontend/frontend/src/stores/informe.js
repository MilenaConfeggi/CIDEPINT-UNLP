import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'

export const useInformeStore = defineStore('informe', {
  state: () => ({
    successMessage: '',
    errorMessage: '',
    showToast: false,
  }),
  actions: {
    async uploadInforme(event, id, legajoId) {
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
            this.successMessage = 'Informe subido correctamente'
            this.showToast = true
            setTimeout(() => window.location.reload(), 2000)
          } else {
            throw new Error(response.data.error || 'No se pudo subir el archivo')
          }
        } catch (error) {
          console.error('Error al subir el archivo:', error)
          this.errorMessage = error.response?.data?.error || 'Error al subir el archivo'
          this.showToast = true
        }
      } else {
        alert('Por favor selecciona un archivo PDF.')
      }
    },
    async uploadInformeFirmado(event, id, legajoId) {
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
            this.successMessage = 'Informe firmado subido correctamente'
            this.showToast = true
            setTimeout(() => window.location.reload(), 2000)
          } else {
            throw new Error(response.data.error || 'No se pudo subir el archivo')
          }
        } catch (error) {
          console.error('Error al subir el archivo:', error)
          this.errorMessage = error.response?.data?.error || 'Error al subir el archivo'
          this.showToast = true
        }
      } else {
        alert('Por favor selecciona un archivo PDF.')
      }
    },
    async verInforme(id) {
      const token = useAuthStore().getToken()
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
        this.errorMessage = error.message || 'Error al obtener el informe'
        this.showToast = true
      }
    },
    async uploadDocumentacion(event, id, legajoId) {
      const file = event.target.files[0]
      const token = useAuthStore().getToken()
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
            this.successMessage = 'Documentación subida correctamente'
            this.showToast = true
            setTimeout(() => window.location.reload(), 2000)
          } else {
            throw new Error(response.data.error || 'No se pudo subir el archivo')
          }
        } catch (error) {
          console.error('Error al subir el archivo:', error)
          this.errorMessage = error.response?.data?.error || 'Error al subir el archivo'
          this.showToast = true
        }
      } else {
        alert('Por favor selecciona un archivo PDF.')
      }
    },
  },
})