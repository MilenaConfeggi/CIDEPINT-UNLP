<template>
    <form @submit.prevent="submitForm">
      <div>
        <label for="nombre_archivo">Nombre del Archivo:</label>
        <input type="text" id="nombre_archivo" v-model="formData.nombre_archivo" required />
      </div>
      <button type="submit">Enviar</button>
    </form>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        nombre_archivo: '',
      },
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('http://127.0.0.1:5000/mails/subir_mail/1', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData),
        });

        if (!response.ok) {
          throw new Error('Error al enviar los datos');
        }

        const data = await response.json();
        console.log('Respuesta del servidor:', data);
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>