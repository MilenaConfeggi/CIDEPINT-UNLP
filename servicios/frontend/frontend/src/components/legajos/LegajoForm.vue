<template>
  <RouterLink to="/legajos" class="back-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24">
      <g fill="none">
        <path
          d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z" />
        <path fill="black"
          d="M3.283 10.94a1.5 1.5 0 0 0 0 2.12l5.656 5.658a1.5 1.5 0 1 0 2.122-2.122L7.965 13.5H19.5a1.5 1.5 0 0 0 0-3H7.965l3.096-3.096a1.5 1.5 0 1 0-2.122-2.121z" />
      </g>
    </svg>
  </RouterLink>
  <h2 class="mb-3 text-center mb-5">Crear legajo</h2>
  <form ref="formRef" @submit.prevent="validateForm" class="row g-3 needs-validation" novalidate
    :class="{ 'was-validated': wasValidated }">
    <div class="col-md-6">
      <label for="nombreCliente" class="form-label">Nombre del cliente</label>
      <input type="text" class="form-control" id="nombreCliente" required v-model="form.nombreCliente"
        placeholder="Ingresar nombre del cliente." />
      <div class="invalid-feedback">Por favor, ingrese nombre del cliente.</div>
    </div>
    <div class="col-md-6">
      <label for="cuit" class="form-label">CUIT</label>
      <input type="number" class="form-control" id="cuit" required v-model="form.cuit" placeholder="Ingresar CUIT." />
      <div class="invalid-feedback">Por favor, ingrese CUIT.</div>
    </div>
    <div class="col-md-6">
      <label for="email" class="form-label">Email</label>
      <input type="email" class="form-control" id="email" required v-model="form.email" placeholder="Ingresar email." />
      <div class="invalid-feedback">Por favor, ingrese un email valido.</div>
    </div>
    <div class="col-md-6">
      <label for="telefono" class="form-label">Teléfono</label>
      <input type="text" class="form-control" id="telefono" placeholder="+54 (9) 221 " v-model="form.telefono"
        required />
      <div class="invalid-feedback">Por favor, ingrese un teléfono.</div>
    </div>
    <div class="col-md-6">
      <label for="contacto" class="form-label">Contacto</label>
      <input type="text" class="form-control" id="contacto" v-model="form.contacto" required
        placeholder="Ingresar contacto." />
      <div class="invalid-feedback">Por favor, ingrese un contacto.</div>
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
      <input type="text" class="form-control" id="calle" v-model="form.calle" required placeholder="Ingresar calle." />
      <div class="invalid-feedback">Por favor, ingrese calle.</div>
    </div>
    <div class="col-md-6">
      <label for="numero" class="form-label">Número</label>
      <input type="text" class="form-control" id="calle" v-model="form.numero" required
        placeholder="Ingresar número." />
      <div class="invalid-feedback">Por favor, ingrese número.</div>
    </div>
    <div class="col-md-6">
      <label for="piso" class="form-label">Piso</label>
      <input type="text" class="form-control" id="piso" v-model="form.piso" placeholder="Ingresar piso." />
    </div>
    <div class="col-md-6">
      <label for="depto" class="form-label">Departamento</label>
      <input type="text" class="form-control" id="depto" v-model="form.depto" placeholder="Ingresar departamento." />
    </div>
    <div class="col-md-6">
      <label for="cp" class="form-label">Código postal</label>
      <input type="text" class="form-control" id="cp" v-model="form.codigo_postal" required
        placeholder="Ingresar código postal." />
      <div class="invalid-feedback">Por favor, ingrese código postal.</div>
    </div>
    <div class="col-md-2">
      <label for="localidad" class="form-label">Localidad</label>
      <input type="text" class="form-control" id="localidad" v-model="form.localidad" required
        placeholder="Ingresar localidad." />
      <div class="invalid-feedback">Por favor, ingrese una localidad.</div>
    </div>
    <div class="col-md-3 mt-4">
      <div class="form-check">
        <input class="form-check-input" type="checkbox" id="es_juridico" v-model="form.es_juridico" />
        <label class="form-check-label" for="es_juridico"> No requiere presupuesto </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="checkbox" id="necesita_facturacion" v-model="form.necesita_facturacion" />
        <label class="form-check-label" for="necesita_facturacion"> Necesita facturación </label>
      </div>
    </div>
    <div class="mb-3">
      <label for="objetivo" class="form-label">Objetivo del OT</label>
      <textarea class="form-control" id="objetivo" placeholder="Ingresar objetivo." required
        v-model="form.objetivo"></textarea>
      <div class="invalid-feedback">Por favor, ingrese un objetivo para el legajo.</div>
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
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

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
    const router = useRouter()

    return {
      areas,
      loading,
      error,
      toast,
      router
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
      const form = this.$refs.formRef
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
          const authStore = useAuthStore();
          const token = authStore.getToken();
          const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/api/legajos/add`,
            data,  
            {      
              headers: {
                Authorization: `Bearer ${token}`
              }
            }
          )
          console.log(response)
          this.toast.success('Formulario enviado correctamente')
          this.wasValidated = false
          this.resetForm()
          setTimeout(() => {
            this.router.push('/legajos')
          }, 1500)
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
