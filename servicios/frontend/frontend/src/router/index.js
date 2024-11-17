import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
    },
    {
      path: "/muestras/:legajoId/carpetas",
      name: "muestrasCarpetas",
      component: () => import("../views/MuestrasCarpetasView.vue"),
      props: true,
    },
  ],
})

export default router
