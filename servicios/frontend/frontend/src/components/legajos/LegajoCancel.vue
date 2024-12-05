<template>
  <div class="d-flex justify-content-center align-items-center">
    <form
      ref="form"
      @submit.prevent="handleSubmit"
      class="d-flex justify-content-center align-items-center row g-3 needs-validation"
      novalidate
      :class="{ 'was-validated': wasValidated }"
    >
      <h2 class="mb-3 col-md-6">Cancelar Legajo</h2>
      <div class="mb-3">
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

export default {
  setup() {
    const route = useRoute()
    const router = useRouter()
    const legajosStore = useLegajosStore()

    const legajoId = route.params.id

    return {
      legajoId,
      legajosStore,
      router,
    }
  },
  data() {
    return {
      form: {
        motivo: '',
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
        await this.legajosStore.cancelLegajo(this.legajoId, this.form.motivo)
        alert('Legajo cancelado exitosamente')
        this.resetForm()
        this.router.push('/legajos')
      } catch (error) {
        console.error('Error al cancelar el legajo:', error)
        alert('Ocurrió un error al cancelar el legajo. Inténtelo nuevamente.')
      } finally {
        this.isSubmitting = false
      }
    },
    resetForm() {
      this.form.motivo = ''
      this.wasValidated = false
    },
  },
}
</script>
