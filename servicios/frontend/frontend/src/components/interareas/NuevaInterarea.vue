<template>
  <div class="container">
    <div class="card shadow">
      <div class="card-body">
        <h4 class="card-title text-center mb-4">Solicitar Interarea</h4>

        <div v-if="mensajeExito" class="alert alert-success">
          {{ mensajeExito }}
        </div>

        <form @submit.prevent="enviarFormulario">
          <div class="form-group">
            <label class="form-label fw-bold">Seleccionar tipo de interarea</label>
            <select v-model="form.tipo" class="form-select">
              <option disabled value="">Tipo</option>
              <option value="ABSORCIÓN ATÓMICA">ABSORCIÓN ATÓMICA</option>
              <option value="ANALISIS QUIMICO">ANALISIS QUIMICO</option>
              <option value="ANELPIRE-IMPEDANCIA">ANELPIRE – Medidas de Impedancia</option>
              <option value="ARENADO">ARENADO</option>
              <option value="Asist. Téc. ELECTRÓNICA">Asist. Téc. ELECTRÓNICA</option>
              <option value="ASTP-LINA">ATSP Y LINA</option>
              <option value="DSC">DSC</option>
              <option value="ESPECROFOTOMETRÍA UV visible">ESPECROFOTOMETRÍA UV visible</option>
              <option value="ESPECTROFOTOMETRIA_FTIR">FTIR</option>
              <option value="GENERAL">GENERAL</option>
              <option value="Molino Horizontal de Perlas de Alta Velocidad">Molino de Perlas Horizontal de Alta Velocidad</option>
              <option value="TGA">TGA</option>
            </select>
            <div v-if="errores.tipo" class="text-danger">{{ errores.tipo }}</div>
          </div>

          <div class="form-group">
            <div class="form-check">
              <input type="checkbox" v-model="form.investigacion" id="investigacion" class="form-check-input" />
              <label class="form-check-label fw-bold" for="investigacion">
                Investigación
              </label>
            </div>
          </div>

          <div class="form-group" v-if="!form.investigacion">
            <label class="form-label fw-bold">Seleccionar legajo</label>
            <select v-model="form.legajo" @change="filtrarMuestras" class="form-select">
              <option disabled value="">Legajos</option>
              <option v-for="legajo in legajos" :key="legajo.id" :value="legajo.id">
                {{ legajo.nro_legajo }}
              </option>
            </select>
            <div v-if="errores.legajo" class="text-danger">{{ errores.legajo }}</div>
          </div>

          <div class="form-group" v-if="form.investigacion">
            <label class="form-label fw-bold">Ingresar línea de investigación</label>
            <input v-model="form.lineaInvestigacion" type="text" class="form-control" placeholder="Línea de investigación" />
            <div v-if="errores.lineaInvestigacion" class="text-danger">{{ errores.lineaInvestigacion }}</div>
          </div>

          <div class="form-group">
            <label class="form-label fw-bold">Seleccionar área</label>
            <select v-model="form.area" class="form-select">
              <option disabled value="">Áreas</option>
              <option v-for="area in areas" :key="area.id" :value="area.id">
                {{ area.nombre }}
              </option>
            </select>
            <div v-if="errores.area" class="text-danger">{{ errores.area }}</div>
          </div>

          <div class="form-group">
            <div v-if="form.investigacion">
              <label class="form-label fw-bold">Ingresar identificación de muestras</label>
              <input v-model="form.muestra_investigacion" type="text" class="form-control" placeholder="Identificación de muestras" />
            </div>
            <div v-if="!form.investigacion">
              <label class="form-label fw-bold">Seleccionar identificación de muestras</label>
              <select v-model="form.muestra" class="form-select" :disabled="!form.legajo">
                <option disabled value="">Identificaciones</option>
                <option v-for="muestra in muestrasFiltradas" :key="muestra.id" :value="muestra.id">
                  {{ muestra.nro_muestra }}
                </option>
              </select>
            </div>
            <div v-if="errores.muestra" class="text-danger">{{ errores.muestra }}</div>
          </div>

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
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      legajos: [],
      areas: [],
      muestras: [],
      muestrasFiltradas: [], // Estado para almacenar las muestras filtradas
      errores: {}, // Estado para almacenar los mensajes de error
      mensajeExito: "", // Estado para almacenar el mensaje de éxito
      form: {
        legajo: "",
        lineaInvestigacion: "",
        area: "",
        muestra: "",
        muestra_investigacion: "",
        investigacion: false,
        identificacion: "",
        tipo: "",
        solicitante: ""
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
    filtrarMuestras() {
      if (this.form.legajo) {
        this.muestrasFiltradas = this.muestras.filter(muestra => muestra.legajo_id === this.form.legajo);
      } else {
        this.muestrasFiltradas = [];
      }
    },
    validarFormulario() {
      this.errores = {};

      if (!this.form.tipo) {
        this.errores.tipo = "El tipo de interarea es obligatorio.";
      }

      if (!this.form.area) {
        this.errores.area = "El área es obligatoria.";
      }

      if (!this.form.muestra && !this.form.investigacion) {
        this.errores.muestra = "La muestra es obligatoria.";
      } else if (this.form.muestra.length > 255) {
        this.errores.muestra = "La muestra no puede superar los 255 caracteres.";
      }

      if (!this.form.muestra_investigacion && this.form.investigacion) {
        this.errores.muestra = "La muestra es obligatoria.";
      } else if (this.form.muestra_investigacion.length > 255) {
        this.errores.muestra = "La muestra no puede superar los 255 caracteres.";
      }

      if (this.form.lineaInvestigacion.length > 255) {
        this.errores.lineaInvestigacion = "La línea de investigación no puede superar los 255 caracteres.";
      }

      if (this.form.investigacion && !this.form.lineaInvestigacion) {
        this.errores.lineaInvestigacion = "La línea de investigación es obligatoria.";
      } else if (!this.form.investigacion && !this.form.legajo) {
        this.errores.legajo = "El legajo es obligatorio.";
      }

      return Object.keys(this.errores).length === 0;
    },
    async enviarFormulario() {
      if (!this.validarFormulario()) {
        return;
      }

      const baseUrl = import.meta.env.VITE_API_URL;

      const datosFormulario = {
        legajo: this.form.legajo,
        lineaInvestigacion: this.form.lineaInvestigacion,
        area: this.form.area,
        muestra: this.form.muestra,
        investigacion: this.form.investigacion,
        tipo: this.form.tipo,
        solicitante: this.form.solicitante // aca deberia sacar el area de la sesion
      };

      try {
        const response = await fetch(`${baseUrl}/interareas/crear`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(datosFormulario),
        });

        if (!response.ok) {
          throw new Error("Error al enviar el formulario");
        }

        this.mensajeExito = "Se ha creado la interárea correctamente.";
        this.router.push({ name: "interareas" });
      } catch (error) {
        console.error("Error al enviar el formulario:", error);
        alert("Hubo un error al enviar el formulario.");
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>