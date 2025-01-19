<template>
  <RouterLink to="/legajos" class="back-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24">
      <g fill="none">
        <path
          d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"
        />
        <path
          fill="black"
          d="M3.283 10.94a1.5 1.5 0 0 0 0 2.12l5.656 5.658a1.5 1.5 0 1 0 2.122-2.122L7.965 13.5H19.5a1.5 1.5 0 0 0 0-3H7.965l3.096-3.096a1.5 1.5 0 1 0-2.122-2.121z"
        />
      </g>
    </svg>
  </RouterLink>
  <div class="d-flex justify-content-center align-items-center">
    <form
      ref="form"
      @submit.prevent="handleSubmit"
      class="d-flex justify-content-center align-items-center row g-3 needs-validation"
      novalidate
      :class="{ 'was-validated': wasValidated }"
    >
      <h2 class="mb-3 col-md-7">Cancelar Legajo Nro.{{ legajoId }}</h2>
      <div class="mb-3">
        <label for="estado" class="form-label">Estado del proceso:</label>
        <input
          type="text"
          class="form-control"
          id="motivo"
          placeholder="Motivo"
          required
          v-model="form.estado"
        />
        <div class="invalid-feedback">Por favor, ingrese un estado.</div>
        <label for="motivo" class="form-label">Motivo de cancelación</label>
        <textarea
          class="form-control"
          id="motivo"
          placeholder="Escriba el motivo"
          required
          v-model="form.motivo"
        ></textarea>
        <div class="invalid-feedback">Por favor, ingrese un motivo válido.</div>
      </div>
      <div class="col-12 d-flex justify-content-center">
        <button type="submit" class="btn btn-danger" :disabled="isSubmitting">
          {{ isSubmitting ? 'Cancelando...' : 'Cancelar' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { useLegajosStore } from '../../stores/legajos'
import { useToast } from 'vue-toastification'

export default {
  setup() {
    const route = useRoute()
    const router = useRouter()
    const legajosStore = useLegajosStore()
    const toast = useToast()

    const legajoId = route.params.id

    return {
      legajoId,
      legajosStore,
      router,
      toast,
    }
  },
  data() {
    return {
      form: {
        motivo: '',
        estado: '',
      },
      wasValidated: false,
      isSubmitting: false,
    }
  },
  methods: {
    async handleSubmit() {
      const form = this.$refs.form

      if (!form.checkValidity()) {
        this.wasValidated = true
        return
      }

      this.wasValidated = false
      this.isSubmitting = true

      try {
        await this.legajosStore.cancelLegajo(this.legajoId, this.form.motivo, this.form.estado)
        this.toast.success('Legajo cancelado exitosamente')
        this.resetForm()
        setTimeout(() => {
          this.router.push('/legajos')
        }, 2000)
      } catch (error) {
        this.toast.error('Error al cancelar el legajo')
        console.error('Error al cancelar el legajo:', error)
      } finally {
        this.isSubmitting = false
      }
    },
    resetForm() {
      ;(this.form.motivo = ''), (this.form.estado = '')
      this.wasValidated = false
    },
  },
}
</script>
