import { defineStore } from 'pinia'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'

export const useEncuestasStore = defineStore('encuestas', {
  state: () => ({
    encuestas: [],
    done: false,
    link: '',
  }),
  actions: {
    async createEncuestas() {
      this.done = false
      const uniqueKey = uuidv4()
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/encuestas/add`, {
          params: {
            unique_key: uniqueKey,
          },
          
        })
        console.log(response)
        if (!response.status === 200) {
            throw new Error('No se pudo crear la encuesta')
        } else {
            this.link = `http://localhost:5173/encuesta?id=${uniqueKey}`
        }
      } catch (error) {
        console.error('Error al obtener las encuestas:', error)
      } finally {
        this.done = true
      }
    },
    async mandarMail(mail, link, arch, id) {
      try {
        const data = {
          mail,
          link,
          arch,
          legajo_id: id,
        }
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/legajos/mandar_informe`, data)
        if (!response.status === 200) {
          throw new Error('No se pudo mandar el correo')
        }
      } catch (error) {
        console.error('Error al mandar el correo:', error)
      }
    }
  },
})
