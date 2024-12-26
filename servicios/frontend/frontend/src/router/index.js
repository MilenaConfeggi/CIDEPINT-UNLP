import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'
import axios from 'axios'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { showNavbar: true },
  },
  {
    path: '/mails/:legajoId',
    name: 'mails',
    component: () => import('../views/MailsView.vue'),
    props: true,
    meta: { requiresAuth: true, checkLegajoPermission: true, showNavbar: true },
  },
  {
    path: '/muestras/:legajoId',
    name: 'muestras',
    component: () => import('../views/MuestrasIdentificadasView.vue'),
    props: true,
    meta: { requiresAuth: true, checkLegajoPermission: true, showNavbar: true },
  },
  {
    path: '/muestras/:legajoId/carpetas',
    name: 'muestrasCarpetas',
    component: () => import('../views/MuestrasCarpetasView.vue'),
    props: true,
    meta: { requiresAuth: true, checkLegajoPermission: true, showNavbar: true },
  },
  {
    path: '/informes/:legajoId',
    name: 'informes',
    component: () => import('../views/InformesView.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/legajos',
    name: 'legajos',
    component: () => import('../views/LegajoView.vue'),
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/legajos/:id',
    name: 'legajo',
    component: () => import('../components/legajos/LegajoDetalle.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/legajos/cancelar/:id',
    name: 'cancelar',
    component: () => import('../components/legajos/LegajoCancel.vue'),
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/legajos/newLegajo',
    name: 'newLegajo',
    component: () => import('../components/legajos/LegajoForm.vue'),
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/documentos',
    name: 'documento',
    component: () => import('../components/documentos/DocumentoListado.vue'),
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/stans',
    name: 'stans',
    component: () => import('../views/StansView.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/interareas',
    name: 'interareas',
    component: () => import('../views/InterareasView.vue'),
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/interarea-detalle/:id',
    name: 'InterareaDetalle',
    component: () => import('../components/interareas/DetalleInterarea.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/nueva-interarea',
    name: 'NuevaInterarea',
    component: () => import('../components/interareas/NuevaInterarea.vue'),
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/nueva-interarea',
    name: 'NuevaInterarea',
    component: () => import('../components/interareas/NuevaInterarea.vue'),
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/log-in',
    name: 'logIn',
    component: () => import('../views/LogIn.vue'),
    props: true,
    meta: { showNavbar: true },
  },
  {
    path: '/usuarios',
    name: 'usuarios',
    component: () => import('../views/UsuariosView.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/usuarios/crear',
    name: 'usuarios_crear',
    component: () => import('../components/usuarios/CrearUsuario.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/cambiar_contra',
    name: 'cambiar_contra',
    component: () => import('../components/usuarios/CambiarContra.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/cambiar_contra_vieja',
    name: 'cambiar_contra_vieja',
    component: () => import('../components/usuarios/CambiarContraVieja.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/ver_perfil',
    name: 'ver_perfil',
    component: () => import('../components/usuarios/VerPerfil.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/recuperar_contra',
    name: 'recuperar_contra',
    component: () => import('../components/usuarios/RecuperarContra.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/generar_certificado/:id_legajo',
    name: 'generar_certificado',
    component: () => import('../components/certificados/CrearCertificado.vue'),
    props: true,
    meta: { requiresAuth: true, showNavbar: true },
  },
  {
    path: '/encuesta',
    name: 'encuesta',
    component: () => import('../views/EncuestaView.vue'),
    meta: { showNavbar: false },
  },
  {
    path: '/generar_presupuesto/:id_legajo',
    name: 'generar_presupuesto',
    component: () => import('../components/presupuestos/GenerarPresupuesto.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/pendientes',
    name: 'pendientes',
    component: () => import('../views/PendientesView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/estadisticas',
    name: 'estadisticas',
    component: () => import('../views/EstadisticasView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/jefe_de_area',
    name: 'jefe_de_area',
    component: () => import('../components/areas/CambiarJefeArea.vue'),
    meta: { requiresAuth: true, showNavbar: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Guardias de navegación global
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.getToken() // Verificar si el usuario está autenticado

  if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthenticated) {
    // Si la ruta requiere autenticación y el usuario no está autenticado
    return next({ name: 'logIn' })
  }

  // Verificar permiso para rutas que tienen checkLegajoPermission
  if (to.matched.some((record) => record.meta.checkLegajoPermission)) {
    const legajoId = to.params.legajoId

    if (!legajoId) {
      console.error('Falta legajoId para verificar permisos')
      return next({ name: 'home' })
    }

    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/muestras/permiso/${legajoId}`,
        {
          headers: { Authorization: `Bearer ${authStore.getToken()}` },
        },
      )

      if (response.status === 200) {
        // Permiso concedido
        return next()
      }
    } catch (error) {
      // Redirigir en caso de error (403 o cualquier otro error)
      if (error.response?.status === 403) {
        console.warn('No tiene permiso para acceder a esta muestra')
        return next({ name: 'home' })
      }
    }
  }

  // Continuar navegación si no hay restricciones
  next()
})

export default router
