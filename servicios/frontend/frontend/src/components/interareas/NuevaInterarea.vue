<template>
    <div class="container">
        <div class="card shadow">
            <div class="card-body">
                <h4 class="card-title text-center mb-4">Solicitar Interarea</h4>
        
                <form @submit.prevent="enviarFormulario">
                    <!-- Checkbox para seleccionar si es investigación -->
                    <div class="form-group">
                        <div class="form-check">
                            <input type="checkbox" v-model="form.investigacion" id="investigacion" class="form-check-input"/>
                            <label class="form-check-label fw-bold" for="investigacion">
                                Investigación
                            </label>
                        </div>
                    </div>
        
                    <!-- Selección de legajo o línea de investigación (condicional) -->
                    <div class="form-group">
                        <div v-if="!form.investigacion">
                            <label class="form-label fw-bold">Seleccionar legajo</label>
                            <select v-model="form.legajo" class="form-select">
                                <option disabled value="">Legajos</option>
                                <option v-for="legajo in legajos" :key="legajo.id" :value="legajo.id">
                                    {{ legajo.id }}
                                </option>
                            </select>
                        </div>
                        <div v-if="form.investigacion">
                            <label class="form-label fw-bold"> Ingresar línea de investigación</label>
                            <input v-model="form.lineaInvestigacion" type="text" class="form-control" placeholder="Línea de investigación" />
                        </div>
                    </div>
        
                    <!-- Selección de área -->
                    <div class="form-group">
                        <label class="form-label fw-bold">Seleccionar área</label>
                        <select v-model="form.area" class="form-select">
                            <option disabled value="">Áreas</option>
                            <option v-for="area in areas" :key="area.id" :value="area.id">
                            {{ area.nombre }}
                            </option>
                        </select>
                    </div>
        
                    <!-- Material a ensayar -->
                    <div class="form-group">
                        <label class="form-label fw-bold">Material a ensayar</label>
                        <input v-model="form.material" type="text" class="form-control" placeholder="Ingresar material a ensayar"/>
                    </div>
        
                    <!-- Selección de identificación de muestras -->
                    <div class="form-group">
                        <label class="form-label fw-bold">Seleccionar identificación de muestras</label>
                        <select v-model="form.muestra" class="form-select">
                            <option disabled value="">Identificaciones</option>
                            <option v-for="muestra in muestras" :key="muestra.id" :value="muestra.id">
                            {{ muestra.id }}
                            </option>
                        </select>
                    </div>
        
                    <!-- Botón de envío -->
                    <div class="text-center">
                        <button type="submit" class="btn btn-primary btn-lg w-50">
                            Enviar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        legajos: [],
        areas: [],
        muestras: [],
        form: {
          legajo: "",
          lineaInvestigacion: "",
          area: "",
          material: "",
          muestra: "",
          investigacion: false, // Nuevo campo para el checkbox
        },
      };
    },
    methods: {
      async fetchData() {
        try {
          const baseUrl = import.meta.env.VITE_API_URL;
          const [legajosRes, areasRes, muestrasRes] = await Promise.all([
            fetch(`${baseUrl}/api/legajos/all`),
            fetch(`${baseUrl}/api/area/`),
            fetch(`${baseUrl}/muestras/`),
          ]);
  
          this.legajos = await legajosRes.json();
          this.areas = await areasRes.json();
          this.muestras = await muestrasRes.json();
        } catch (error) {
          console.error("Error al cargar los datos:", error);
        }
      },
      enviarFormulario() {
        console.log("todavia no hace nada jeje");
      },
    },
    mounted() {
      this.fetchData();
    },
  };
</script>
  
  