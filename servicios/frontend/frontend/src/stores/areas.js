import axios from "axios"; 
import { defineStore } from "pinia";

export const useAreasStore = defineStore("areas", {
    state: () => ({
        areas: [],
        loading: false,
        error: null,
    }),
    actions: {
        async getAreas() {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get("http://127.0.0.1:5000/api/area/");
                this.areas = response.data;
                return response;
            } catch (error) {
                this.error = error;
                throw new Error(error);
            } finally {
                this.loading = false;
            }
        },
    },
});