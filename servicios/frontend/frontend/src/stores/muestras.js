import { defineStore } from 'pinia';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export const useMuestrasStore = defineStore('muestras', {
  state: () => ({
    muestras: [],
    error: null,
  }),
  actions: {
    async fetchMuestras(legajoId) {
      const authStore = useAuthStore();
      const token = authStore.getToken();
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/muestras/${legajoId}`, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          },
        });
        this.muestras = response.data;
      } catch (err) {
        this.error = err.response?.data?.message || 'Error al obtener las muestras';
        throw err;
      }
    },
    clearMuestras() {
      this.muestras = [];
      this.error = null;
    }
  }
});