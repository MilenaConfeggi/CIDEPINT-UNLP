import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from '@/stores/auth';

export const useMuestrasStore = defineStore("muestras", {
    state: () => ({
        muestras: [],
        error: null,
    }),
    actions: {
        async fetchMuestras(id_legajo) {
            const authStore = useAuthStore();
            const token = authStore.getToken();
            try {
                this.error = null;
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/muestras/${id_legajo}`, {
                    headers: {
                      "Authorization": `Bearer ${token}`,
                      "Content-Type": "application/json"
                    },
                });
                this.muestras = response.data;
            } catch (error) {
                this.error = "error";
                console.error(error);
            }  
        },
    },
});