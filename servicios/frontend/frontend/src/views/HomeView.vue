<template>
  <main>
    <div class="d-flex flex-column justify-content-center align-items-center">

      <img alt="cidepint logo" class="logo d-flex justify-content-center" src="/CIDEPINT_full_logo.png" width="400em" height="100em" > 
      
      <p class="text-center">
        Bienvenido a la aplicación de gestión de legajos de la Universidad Nacional de La Plata.
      </p>
    </div>
    <div v-if="estaLogeado" class="row row-cols-3 row-cols-md-3 g-4">
      <div class="col">
        <div class="card border-danger">
          <img src="/legajos.png" class="card-img-top" alt="legajos" />
          <div class="card-body text-danger">
            <h5 class="card-title">Legajos</h5>
            <p class="card-text">
              Aqui se encuentran los legajos que se encuentran en el sistema.
            </p>
            <RouterLink to="/legajos" class="btn btn-danger">Ver Legajos</RouterLink>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card border-primary">
          <img src="/docs.png" class="card-img-top" alt="documentos" />
          <div class="card-body text-primary">
            <h5 class="card-title">Documentos</h5>
            <p class="card-text">
              Listado de los documentos que se encuentran en el sistema.
            </p>
            <RouterLink to="/documentos" class="btn btn-primary">Ver Documentos</RouterLink>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card border-warning">
          <img src="/informe.png" class="card-img-top" alt="stan" />
          <div class="card-body">
            <h5 class="card-title">STAN</h5>
            <p class="card-text">
              Aqui se encuentran la infomarción referida a los STANs.
            </p>
            <RouterLink to="/stans" class="btn btn-warning">Ver STAN</RouterLink>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card border-danger-subtle">
          <img src="/users.jpg" class="card-img-top" alt="stan" />
          <div class="card-body text-danger-emphasis">
            <h5 class="card-title">Usuarios</h5>
            <p class="card-text">
              Listado de los usuarios que se encuentran en el sistema.
            </p>
            <RouterLink to="/usuarios" class="btn btn-secondary">Ver Usuarios</RouterLink>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <img src="/interareas.png" class="card-img-top" alt="interareas" />
          <div class="card-body">
            <h5 class="card-title">Interareas</h5>
            <p class="card-text">
              Menejo de interáreas para realizar solicitudes y subir resultados.
            </p>
            <RouterLink to="/interareas" class="btn btn-dark">Ver Interareas</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
const authStore = useAuthStore()

const estaLogeado = computed(() => authStore.checkLogin())
</script>