import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import HomeView from '../views/HomeView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/mails/:legajoId',
    name: "mails",
    component: () => import("../views/MailsView.vue"),
    props: true,
  },
  {
    path: "/muestras/:legajoId",
    name: "muestras",
    component: () => import("../views/MuestrasIdentificadasView.vue"),
    props: true,
    meta: { requiresAuth: true} 
  },
  {
    path: "/muestras/:legajoId/carpetas",
    name: "muestrasCarpetas",
    component: () => import("../views/MuestrasCarpetasView.vue"),
    props: true,
    meta: { requiresAuth: true } 
  },
  {
    path: "/informes/:legajoId",
    name: "informes",
    component: () => import("../views/InformesView.vue"),
    props: true,
    meta: { requiresAuth: true } 
  },
  {
    path: "/legajos",
    name: "legajos",
    component: () => import("../views/LegajoView.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/legajos/:id",
    name: "legajo",
    component: () => import("../components/legajos/LegajoDetalle.vue"),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: "/legajos/cancelar/:id",
    name: "cancelar",
    component: () => import("../components/legajos/LegajoCancel.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/legajos/newLegajo",
    name: "newLegajo",
    component: () => import("../components/legajos/LegajoForm.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/documentos",
    name: "documento",
    component: () => import("../components/documentos/DocumentoListado.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/stans",
    name: "stans",
    component: () => import("../views/StansView.vue"),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: "/interareas",
    name: "interareas",
    component: () => import("../views/InterareasView.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/interarea-detalle/:id",
    name: "InterareaDetalle",
    component: () => import("../components/interareas/DetalleInterarea.vue"),
    props: true, 
    meta: { requiresAuth: true }
  },
  {
    path: "/log-in",
    name: "logIn",
    component: () => import("../views/LogIn.vue"),
    props: true,
  },
    {
      path: "/usuarios",
      name: "usuarios",
      component: () => import("../views/UsuariosView.vue"),
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: "/usuarios/crear",
      name: "usuarios_crear",
      component: () => import("../components/usuarios/CrearUsuario.vue"),
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: "/cambiar_contra",
      name: "cambiar_contra",
      component: () => import("../components/usuarios/CambiarContra.vue"),
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: "/cambiar_contra_vieja",
      name: "cambiar_contra_vieja",
      component: () => import("../components/usuarios/CambiarContraVieja.vue"),
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: "/ver_perfil",
      name: "ver_perfil",
      component: () => import("../components/usuarios/VerPerfil.vue"),
      props: true,
      meta: { requiresAuth: true }
    },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// Guardias de navegación global
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = !!authStore.getToken(); // Verificar si el usuario está autenticado
  const userPermissions = JSON.parse(localStorage.getItem('permisos')) || []; // Obtener permisos del usuario

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    // Si la ruta requiere autenticación y el usuario no está autenticado, redirigir a la página de inicio de sesión
    next({ name: 'logIn' });
  } else if (to.matched.some(record => record.meta.requiredPermission)) {
    const requiredPermission = to.meta.requiredPermission;
    if (!userPermissions.includes(requiredPermission)) {
      // Si el usuario no tiene el permiso requerido, redirigir a una página de acceso denegado o a la página de inicio
      next({ name: 'home' });
    } else {
      // Si el usuario tiene el permiso requerido, permitir el acceso a la ruta
      next();
    }
  } else {
    // De lo contrario, permitir el acceso a la ruta
    next();
  }
});

export default router;