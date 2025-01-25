<template>
  <div class="d-flex flex-column justify-content-center align-items-center">
    <h2 class="text-center">Bienvenido a la plataforma de</h2>
    <img
      alt="cidepint logo"
      class="logo d-flex justify-content-center"
      src="/CIDEPINT_full_logo.png"
      width="400em"
      height="100em"
    />
  </div>
  <div v-if="estaLogeado" class="d-flex flex-column justify-content-center align-items-center">
    <p class="fs-4 mt-5 mb-5">En ella podrás realizar las acciones para llevar a cabo las tareas diarias</p>
    
    <div class="container">
      <div class="row row-cols-1 row-cols-md-2 g-4">
        <!-- Columna 1 -->
        <div class="col">
          <!-- Tarjeta de Legajos -->
          <div class="card mb-3 border-danger">
            <div class="row g-0">
              <div class="col-md-4 d-flex justify-content-center align-items-center">
                <i class="fas fa-folder fa-5x text-danger"></i>
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">Legajos</h5>
                  <p class="card-text">Visualizar los legajos generados hasta la fecha.</p>
                  <RouterLink to="/legajos" class="btn btn-danger">Ver Legajos</RouterLink>
                </div>
              </div>
            </div>
          </div>

          <!-- Tarjeta de Documentos -->
          <div class="card mb-3 border-primary">
            <div class="row g-0">
              <div class="col-md-4 d-flex justify-content-center align-items-center">
                <i class="fas fa-file-alt fa-5x text-primary"></i>
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">Documentos</h5>
                  <p class="card-text">Ver el listado de los documentos que se encuentran en el sistema.</p>
                  <RouterLink to="/documentos" class="btn btn-primary">Ver Documentos</RouterLink>
                </div>
              </div>
            </div>
          </div>

          <!-- Tarjeta de STANs -->
          <div class="card mb-3 border-warning">
            <div class="row g-0">
              <div class="col-md-4 d-flex justify-content-center align-items-center">
                <i class="fas fa-list fa-5x text-warning"></i>
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">STANs</h5>
                  <p class="card-text">Recurrir a la información referida a los STANs.</p>
                  <RouterLink to="/stans" class="btn btn-warning">Ver STAN</RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Columna 2 -->
        <div class="col">
          <!-- Tarjeta de Usuarios -->
          <div class="card mb-3 border-danger-subtle">
            <div class="row g-0">
              <div class="col-md-4 d-flex justify-content-center align-items-center">
                <i class="fas fa-users fa-5x text-secondary"></i>
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">Usuarios</h5>
                  <p class="card-text">Ver los usuarios que se encuentran en el sistema.</p>
                  <RouterLink to="/usuarios" class="btn btn-secondary">Ver Usuarios</RouterLink>
                </div>
              </div>
            </div>
          </div>

          <!-- Tarjeta de Interáreas -->
          <div class="card mb-3">
            <div class="row g-0">
              <div class="col-md-4 d-flex justify-content-center align-items-center">
                <i class="fas fa-exchange-alt fa-5x text-dark"></i>
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">Interáreas</h5>
                  <p class="card-text">Manejar las interáreas para realizar solicitudes y subir resultados.</p>
                  <RouterLink to="/interareas" class="btn btn-dark">Ver Interareas</RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
const authStore = useAuthStore()

const estaLogeado = computed(() => authStore.checkLogin())
</script>
