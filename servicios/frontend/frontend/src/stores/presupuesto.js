import axios from 'axios'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const usePresupuestoStore = defineStore('presupuesto', {
  state: () => ({
    successMessage: '',
    errorMessage: '',
    showToast: false,
  }),
  actions: {
    async uploadPresupuestoFirmado(event, id, legajoId) {
      const file = event.target.files[0]
      const token = useAuthStore().getToken()
      if (file && file.type === 'application/pdf') {
        try {
          const formData = new FormData()
          formData.append('archivo', file)
          const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/presupuestos/cargar_presupuesto_firmado/${legajoId}`,
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
            this.successMessage = 'Presupuesto firmado subido correctamente'
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
    async viewPresupuesto(id, legajoId) {
      const token = useAuthStore().getToken()
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/presupuestos/ver_documento/${legajoId}`, {
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
        this.errorMessage = error.message || 'Error al obtener el documento'
        this.showToast = true
      }
    },
    async verPresupuestoFirmado(id, legajoId) {
      const token = useAuthStore().getToken()
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/presupuestos/ver_documento_firmado/${legajoId}`, {
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
        this.errorMessage = error.message || 'Error al obtener el documento'
        this.showToast = true
      }
    },
  },
})