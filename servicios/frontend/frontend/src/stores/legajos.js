import axios from 'axios'
import { defineStore } from 'pinia'

export const useLegajosStore = defineStore('legajos', {
    state: () => ({
        legajos: [],
        legajo: {},
        loading: false, 
        error: null,
        totalPages: 0,
        
    }),
    actions: {
        async getLegajos(params) {
            const { page, per_page, empresa, fecha, area, ensayo } = params
            this.loading = true
            this.error = null
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/legajos/', {
                    params: {
                        page,
                        per_page,
                        empresa,
                        fecha,
                        area,
                        ensayo
                    },
                })
                this.legajos = response.data
                this.totalPages = response.data.pages
            } catch (error) {
                this.error = error
                console.log(error)
            } finally {
                this.loading = false
            }
            
        },
        async getLegajo(id) {
            this.loading = true
            this.error = null
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/legajos/${id}`)
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
                const response = await axios.post('http://127.0.0.1:5000/api/legajos/add', data)
                if (response.status !== 200) {
                    throw new Error('Error al crear el legajo');
                }
            } catch (error) {
                this.error = error
                console.log(error)
            } finally {
                this.loading = false
            }
        },
        async cancelLegajo(id, motivo) {
            this.loading = true
            this.error = null
            const data = {
                motivo,
            }
            try {
                const response = await axios.post(`http://127.0.0.1:5000/api/legajos/cancel/${id}`, data)
                if (response.status !== 200) {
                    throw new Error('Error al cancelar el legajo');
                }
            } catch (error) {
                this.error = error
                console.log(error)
            } finally {
                this.loading = false
            }
        },
    },
})