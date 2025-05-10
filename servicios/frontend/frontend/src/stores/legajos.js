import axios from 'axios'
import { defineStore } from 'pinia'
import { useToast } from 'vue-toastification'
import { useAuthStore } from './auth'


export const useLegajosStore = defineStore('legajos', {
  state: () => ({
    legajos: [],
    legajo: {},
    loading: false,
    error: null,
    totalPages: 0,
    toast: useToast(),
  }),
  actions: {
    async getLegajos(params) {
      const { page, per_page, empresa, fecha, area, ensayo } = params
      const authStore = useAuthStore();
      const token = authStore.getToken();
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/legajos/`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            },
            params: {
              page,
              per_page,
              empresa,
              fecha,
              area,
              ensayo,
            },
          })
        this.legajos = response.data
        console.log(response.data)
        this.totalPages = response.data.pages
      } catch (error) {
        this.error = error
        console.log(error)
      } finally {
        this.loading = false
      }
    },
    async getLegajo(id) {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/legajos/${id}`,
          {
            headers: { Authorization: `Bearer ${token}` }
          },
        )
        this.legajo = response.data
      } catch (error) {
        this.error = error
        console.log(error)
      } finally {
        this.loading = false
      }
    },
    async addLegajo(data) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/legajos/add`, data)
        if (response.status !== 200) {
          throw new Error('Error al crear el legajo')
        }
      } catch (error) {
        this.error = error
        console.log(error)
      } finally {
        this.loading = false
      }
    },
    async cancelLegajo(id, motivo, proc) {
      this.loading = true
      this.error = null
      const data = {
        motivo,
        proc,
      }
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/legajos/cancel/${id}`, data)
        if (response.status !== 200) {
          throw new Error('Error al cancelar el legajo')
        }
      } catch (error) {
        this.error = error
        console.log(error)
      } finally {
        this.loading = false
      }
    },
    async habilitar(id) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/legajos/admin/${id}`)
        if (response.status !== 200) {
          throw new Error('Error al habilitar el legajo')
        }
        else {
          this.toast.success('Legajo habilitado para el area de administracion')
        }
      } catch (error) {
        this.error = error
        this.toast.error('Error al habilitar el legajo')
        console.log(error)
      } finally {
        this.loading = false
      }
    },
    async deleteLegajo(id) {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/legajos/delete/${id}`)
        return response.data;
      } catch (error) {
        console.error('Error en la solicitud de eliminación:', error.response || error);
        throw error;
      }
    }
  },
})
