<template>
  <main>
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
      <p class="fs-4 mt-5 mb-5" >En ella podras realizar las acciones para llevar a cabo las tareas diarias</p>
      <div
        id="carouselExampleCaptions"
        class="carousel slide w-50 d-flex justify-content-center align-items-center"
        data-bs-theme="dark"
      >
        <div class="carousel-indicators">
          <button
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide-to="0"
            class="active"
            aria-current="true"
            aria-label="Slide 1"
          ></button>
          <button
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide-to="1"
            aria-label="Slide 2"
          ></button>
          <button
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide-to="2"
            aria-label="Slide 3"
          ></button>
          <button
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide-to="3"
            aria-label="Slide 4"
          ></button>
          <button
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide-to="4"
            aria-label="Slide 5"
          ></button>
        </div>
        <div class="carousel-inner">
          <div class="carousel-item active">
            <div class="card border-danger" data-bs-theme="light">
              <div class="card-body text-center">
                <p class="card-text">
                  Visualizar los legajos generados hasta la fecha.
                </p>
                <RouterLink to="/legajos" class="btn btn-danger">Ver Legajos</RouterLink>
              </div>
              <img src="/legajos.png" class="card-img-bottom" alt="legajos" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="card border-primary" data-bs-theme="light">
              <div class="card-body text-center">
                <p class="card-text">Ver el listado de los documentos que se encuentran en el sistema.</p>
                <RouterLink to="/documentos" class="btn btn-primary">Ver Documentos</RouterLink>
              </div>
              <img src="/docs.png" class="card-img-bottom" alt="documentos" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="card border-warning" data-bs-theme="light">
              <div class="card-body text-center">
                <p class="card-text">Recurrir a la infomarción referida a los STANs.</p>
                <RouterLink to="/stans" class="btn btn-warning">Ver STAN</RouterLink>
              </div>
              <img src="/informe.png" class="card-img-bottom" alt="stan" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="card border-danger-subtle" data-bs-theme="light">
              <div class="card-body text-center">
                <p class="card-text">Ver los usuarios que se encuentran en el sistema.</p>
                <RouterLink to="/usuarios" class="btn btn-secondary">Ver Usuarios</RouterLink>
              </div>
              <img src="/users.jpg" class="card-img-bottom" alt="stan" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="card" data-bs-theme="light">
              <div class="card-body text-center">
                <p class="card-text">
                  Menejar las interáreas para realizar solicitudes y subir resultados.
                </p>
                <RouterLink to="/interareas" class="btn btn-dark">Ver Interareas</RouterLink>
                <img src="/interareas.png" class="card-img-bottom" alt="interareas" />
              </div>
            </div>
          </div>
        </div>
        <button
          class="carousel-control-prev"
          type="button"
          data-bs-target="#carouselExampleCaptions"
          data-bs-slide="prev"
        >
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button
          class="carousel-control-next"
          type="button"
          data-bs-target="#carouselExampleCaptions"
          data-bs-slide="next"
        >
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
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
