<template>
  <form
    @submit.prevent="validateForm"
    class="row g-3 needs-validation"
    novalidate
    :class="{ 'was-validated': wasValidated }"
  >
    <div class="col-md-6">
      <label for="nombreCliente" class="form-label">Nombre del cliente</label>
      <input
        type="text"
        class="form-control"
        id="nombreCliente"
        required
        v-model="form.nombreCliente"
      />
      <div class="invalid-feedback">Por favor, introduzca un nombre del cliente.</div>
    </div>
    <div class="col-md-6">
      <label for="cuit" class="form-label">CUIT</label>
      <input type="number" class="form-control" id="cuit" required v-model="form.cuit" />
      <div class="invalid-feedback">Por favor, introduzca un CUIT.</div>
    </div>
    <div class="col-md-6">
      <label for="email" class="form-label">Mail</label>
      <input type="email" class="form-control" id="email" required v-model="form.email" />
      <div class="invalid-feedback">Por favor, introduzca un email valido.</div>
    </div>
    <div class="col-md-6">
      <label for="telefono" class="form-label">Telefono</label>
      <input
        type="text"
        class="form-control"
        id="telefono"
        placeholder="+54 (9) 221 "
        v-model="form.telefono"
        required
      />
    </div>
    <div class="col-md-6">
      <label for="contacto" class="form-label">Contacto</label>
      <input type="text" class="form-control" id="contacto" v-model="form.contacto" required />
      <div class="invalid-feedback">Por favor, introduzca un contacto.</div>
    </div>
    <div class="col-md-6">
      <label for="area" class="form-label">Area</label>
      <select class="form-select" id="area" v-model="form.area" required>
        <option selected value="">Seleccione el area...</option>
        <option v-for="area in areas" :key="area.id" :value="area.id">
          {{ area.nombre }}
        </option>
      </select>
      <div class="invalid-feedback">Por favor, seleccione un área.</div>
    </div>
    <div class="col-md-6">
      <label for="calle" class="form-label">Calle</label>
      <input type="text" class="form-control" id="calle" v-model="form.calle" required />
    </div>
    <div class="col-md-6">
      <label for="numero" class="form-label">Numero</label>
      <input type="text" class="form-control" id="calle" v-model="form.numero" required />
    </div>
    <div class="col-md-6">
      <label for="piso" class="form-label">Piso</label>
      <input type="text" class="form-control" id="piso" v-model="form.piso" />
    </div>
    <div class="col-md-6">
      <label for="depto" class="form-label">Departamento</label>
      <input type="text" class="form-control" id="depto" v-model="form.depto" />
    </div>
    <div class="col-md-6">
      <label for="cp" class="form-label">Codigo postal</label>
      <input type="text" class="form-control" id="cp" v-model="form.codigo_postal" required />
    </div>
    <div class="col-md-2">
      <label for="localidad" class="form-label">Localidad</label>
      <input type="text" class="form-control" id="localidad" v-model="form.localidad" required />
    </div>
    <div class="col-md-3 mt-4">
      <div class="form-check">
        <input
          class="form-check-input"
          type="checkbox"
          id="es_juridico"
          v-model="form.es_juridico"
        />
        <label class="form-check-label" for="es_juridico"> No requiere presupuesto </label>
      </div>
      <div class="form-check">
        <input
          class="form-check-input"
          type="checkbox"
          id="necesita_facturacion"
          v-model="form.necesita_facturacion"
        />
        <label class="form-check-label" for="necesita_facturacion"> Necesita facturación </label>
      </div>
    </div>
    <div class="mb-3">
      <label for="objetivo" class="form-label">Objetivo del OT</label>
      <textarea
        class="form-control"
        id="objetivo"
        placeholder="Objetivo"
        required
        v-model="form.objetivo"
      ></textarea>
      <div class="invalid-feedback">Por favor ingrese un objetivo para el legajo.</div>
    </div>
    <div class="col-12 d-flex justify-content-center">
      <button type="submit" class="btn btn-primary">Crear legajo</button>
    </div>
  </form>
</template>
<script>
import axios from 'axios'
import { useAreasStore } from '../../stores/areas'
import { storeToRefs } from 'pinia'
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      form: {
        email: '',
        cuit: '',
        telefono: '',
        contacto: '',
        calle: '',
        numero: '',
        localidad: '',
        codigo_postal: '',
        piso: '',
        depto: '',
        objetivo: '',
        es_juridico: false,
        necesita_facturacion: false,
        nombreCliente: '',
        area: '',
      },
      wasValidated: false,
    }
  },

  setup() {
    const areasStore = useAreasStore();
    const { areas, loading, error } = storeToRefs(areasStore);
    const toast = useToast();

    return {
      areas,
      loading,
      error,
      toast,
    };
  },
  async mounted() {
    const areasStore = useAreasStore();
    await areasStore.getAreas();
  },
  methods: {
    async loadAreas() {
      try {
        const areasStore = useAreasStore()
        await areasStore.getAreas()
      } catch (error) {
        console.error('Error cargando áreas:', error)
        this.toast.error('Hubo un error cargando las áreas. Intente de nuevo más tarde.')
      }
    },
    async validateForm() {
      const form = this.$el
      if (form.checkValidity()) {
        const cliente = {
          email: this.form.email,
          cuit: this.form.cuit,
          telefono: this.form.telefono,
          celular: this.form.telefono,
          direccion: this.form.direccion,
          contacto: this.form.contacto,
          calle: this.form.calle,
          numero: this.form.numero,
          localidad: this.form.localidad,
          codigo_postal: this.form.codigo_postal,
          piso: this.form.piso,
          depto: this.form.depto,
          nombre: this.form.nombreCliente,
        }
        const legajo = {
          objetivo: this.form.objetivo,
          es_juridico: this.form.es_juridico,
          necesita_facturacion: this.form.necesita_facturacion,
          fecha_entrada: new Date().toISOString().replace('T', ' ').replace('Z', ''),
          area_id: this.form.area,
        }
        const data = {
          legajo: legajo,
          cliente: cliente,
        }
        try {
          const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/legajos/add`, data)
          console.log(response)
          this.toast.success('Formulario enviado correctamente')
          this.wasValidated = false
          this.resetForm()
        } catch (error) {
          this.toast.error('Error al enviar el formulario')
          console.log(error)
        }
      } else {
        this.wasValidated = true
      }
    },
    resetForm() {
      this.form.email = ''
      this.form.cuit = ''
      this.form.telefono = ''
      this.form.contacto = ''
      this.form.calle = ''
      this.form.numero = ''
      this.form.localidad = ''
      this.form.codigo_postal = ''
      this.form.piso = ''
      this.form.depto = ''
      this.form.objetivo = ''
      this.form.es_juridico = false
      this.form.necesita_facturacion = false
      this.form.area = ''
    },
  },
}
</script>
