import { defineStore } from "pinia";
import axios from "axios";

export const useMailsStore = defineStore("mails", {
    state: () => ({
        mails: [],
        error: null,
    }),
    actions: {
        async fetchMails(id_legajo) {
            try {
                this.error = null;
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/mails/${id_legajo}`);
                this.mails = response.data;
            } catch (error) {
                this.error = "error";
                console.error(error);
            }  
        },
    },
});