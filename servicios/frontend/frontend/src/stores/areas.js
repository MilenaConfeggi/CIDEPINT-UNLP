import axios from "axios"; 
import { defineStore } from "pinia";
import { useAuthStore } from './auth';
import { useRouter } from 'vue-router';

export const useAreasStore = defineStore("areas", {
    state: () => ({
        areas: [],
        loading: false,
        error: null,
    }),
    actions: {
        async getAreas() {
            const authStore = useAuthStore();
            const token = authStore.token;
            const router = useRouter();
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/area/`,
                    { headers: { Authorization: `Bearer ${token}`} },
                );
                if (response.status !== 200) {
                    throw ({message: 'Error al obtener las areas', status: response.status})
                }
                this.areas = response.data;
                return response;
            } catch (error) {
                if (error.status === 401 || error.status === 422) {
                    authStore.logout()
                    router.push('/log-in')
                } else {
                    this.error = error;
                    throw new Error(error);
                }
            } finally {
                this.loading = false;
            }
        },
    },
});