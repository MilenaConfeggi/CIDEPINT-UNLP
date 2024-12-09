<template>
  <main>
    <div class="d-flex flex-column justify-content-center align-items-center">

      <img alt="cidepint logo" class="logo d-flex justify-content-center" src="/CIDEPINT_full_logo.png" width="400em" height="100em" > 
      
      <p class="text-center">
        Bienvenido a la aplicación de gestión de legajos de la Universidad Nacional de La Plata.
      </p>
    </div>
    <div class="row row-cols-3 row-cols-md-3 g-4">
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
        <div class="card">
          <img src="/muestras.png" class="card-img-top" alt="muestras" />
          <div class="card-body">
            <h5 class="card-title">Muestras</h5>
            <p class="card-text">
              Aqui se encuentran las muestras identificadas, que se utilizan para generar los
              informes.
            </p>
            <RouterLink to="/muestras/1" class="btn btn-primary">Ver Muestras</RouterLink>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <img src="/informe.png" class="card-img-top" alt="informes" />
          <div class="card-body">
            <h5 class="card-title">Informes</h5>
            <p class="card-text">
              Aqui se encuentran los informes de los clientes, que se generan a partir de las
              muestras identificadas.
            </p>
            <RouterLink to="/informes/1" class="btn btn-primary">Ver Informes</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
