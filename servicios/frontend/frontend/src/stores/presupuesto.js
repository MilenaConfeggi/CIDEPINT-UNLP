import axios from 'axios'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'
export const usePresupuestoStore = defineStore('presupuesto', {
  state: () => ({
    successMessage: '',
    errorMessage: '',
    showToast: false,
  }),
  actions: {
    async uploadPresupuestoFirmado(event, id, legajoId) {
    const toast = useToast();
    const router = useRouter();
    const file = event.target.files[0];
    const token = useAuthStore().getToken();
    if (file && file.type === 'application/pdf') {
      toast.info('Subiendo presupuesto firmado...');
      try {
        const formData = new FormData();
        formData.append('archivo', file);
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/presupuestos/cargar_presupuesto_firmado/${legajoId}`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data',
            },
          }
        );
        if (response.status === 200) {
          setTimeout(() => window.location.reload(), 2000);
        } else {
          throw { status: response.status, message: `Error: ${response.status}` };
        }
      } catch (error) {
        console.error('Error al subir el archivo:', error);
        if (error.status === 401 || error.status === 422) {
          useAuthStore().logout();
          router.push('/log-in');
        }
        toast.error(error.response?.data?.error || 'Error al subir el archivo');
      }
    } else {
      toast.warning('Por favor selecciona un archivo PDF.');
    }
  },
    async viewPresupuesto(legajoId) {
      const token = useAuthStore().getToken()
      const toast = useToast()
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/presupuestos/ver_documento/${legajoId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data',
            },
          },
        )
        if (response.status !== 200) {
          throw new Error('Error al obtener el documento')
        }
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        window.open(url, '_blank')
      } catch (error) {
        console.error('Error al obtener el documento:', error)
        toast.error('Error al obtener el documento o no existe')
      }
    },
    async verPresupuestoFirmado(id, legajoId) {
      const token = useAuthStore().getToken()
      const toast = useToast()
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/presupuestos/ver_documento_firmado/${legajoId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data',
            },
          },
        )
        if (response.status !== 200) {
          throw new Error('Error al obtener el documento')
        }
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        window.open(url, '_blank')
      } catch (error) {
        console.error('Error al obtener el documento:', error)
        toast.error('Error al obtener el documento o no existe')
      }
    },
    async fetchPresupuestos(legajoId) {
  const token = useAuthStore().getToken();
  const toast = useToast();
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/presupuestos/listar_presupuestos/${legajoId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data; // Devuelve la lista de presupuestos
  } catch (error) {
    console.error('Error al obtener los presupuestos:', error);
    toast.error('Error al obtener los presupuestos.');
    return [];
  }
},

async fetchPresupuestosFirmados(legajoId) {
  const token = useAuthStore().getToken();
  const toast = useToast();
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/presupuestos/listar_presupuestos_firmados/${legajoId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data; // Devuelve la lista de presupuestos firmados
  } catch (error) {
    console.error('Error al obtener los presupuestos firmados:', error);
    toast.error('Error al obtener los presupuestos firmados.');
    return [];
  }
},
  },
})
