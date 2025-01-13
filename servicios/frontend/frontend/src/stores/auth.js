import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    getToken() {
      return this.token
    },
    removeToken() {
      this.token = null
      localStorage.removeItem('token')
    },
    tienePermiso(permiso) {
      return this.permisos.includes(permiso)
    },
    checkLogin() {
      return !!this.token
    },
    logout() {
      this.removeToken()
      localStorage.removeItem('access_token') // Remove the token from localStorage
      localStorage.removeItem('permisos')
      localStorage.removeItem('area')
      location.reload() // Recarga la página para que se aplique el guard
      console.log('Logout')
    },
  },
})
