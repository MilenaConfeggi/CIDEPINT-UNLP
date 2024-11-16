import { defineStore } from "pinia";
import axios from "axios";

export const useMuestrasStore = defineStore("muestras", {
    state: () => ({
        muestras: [],
        error: null,
    }),
    actions: {
        async fetchMuestras(id_legajo) {
            try {
                this.error = null;
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/muestras/${id_legajo}`);
                this.muestras = response.data;
            } catch (error) {
                this.error = "error";
                console.error(error);
            }  
        },
    },
});