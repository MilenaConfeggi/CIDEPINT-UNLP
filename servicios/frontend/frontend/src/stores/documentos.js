import axios from 'axios'
import { defineStore } from 'pinia'

export const useDocumentosStore = defineStore('documentos', {
  state: () => ({
    documentos: [],
    tipos_documentos: [],
    loading: false,
    error: null,
    doc: null,
    totalPages: 0,
  }),
  actions: {
    async getDocumentos(params) {
      const { page, per_page, tipo_documento, empresa, fecha, area, ensayo } = params
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/`, {
          params: {
            page,
            per_page,
            tipo_documento,
            empresa,
            fecha,
            area,
            ensayo,
          },
        })
        this.totalPages = response.data.pages
        this.documentos = response.data
        return response
      } catch (error) {
        this.error = error
        throw new Error(error)
      } finally {
        this.loading = false
      }
    },
    async getTiposDocumentos() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/tipos_documentos`)
        this.tipos_documentos = response.data
      } catch (error) {
        this.error = error
        console.log(error)
      } finally {
        this.loading = false
      }
    },
    async subirArchivo(file, tipo, legajoId, editar = false, nroFactura = null) {
      this.loading = true
      this.error = null
      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('tipo', tipo)
        formData.append('legajo_id', legajoId)
        formData.append('editar', editar)
        formData.append('nro_factura', nroFactura)
        
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/documentos/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        this.documentos = response.data
        return response
      } catch (error) {
        this.error = error
        throw new Error(error)
      } finally {
        this.loading = false
      }
    },
    async download(nombreDocumento, tipo, legajo_id) {
      this.loading = true
      this.error = null
      console.log(nombreDocumento, tipo, legajo_id)
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/documentos/download`, {
          params: {
            nombre_documento: nombreDocumento,
            tipo_documento_id: tipo,
            legajo_id: legajo_id,
          },
          responseType: 'blob',
        })
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = nombreDocumento
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)

        return response.data
      } catch (error) {
        this.error = error
        console.log(error)
      } finally {
        this.loading = false
      }
    },
    async getDocumento(id) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/documentos/${id}`)
        this.doc = response.data
      } catch (error) {
        this.error = error
        console.log(error)
      } finally {
        this.loading = false
      }
    },
  },
})
