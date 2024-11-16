<template>
  <form @submit.prevent="submitForm" enctype="multipart/form-data">
    <div>
      <label for="archivo">Archivo:</label>
      <input type="file" id="archivo" @change="handleFileUpload" required />
    </div>
    <button type="submit">Enviar</button>
  </form>
</template>

<script>
export default {
props: {
  legajoId: {
    type: Number,
    required: true
  }
},
data() {
  return {
    formData: new FormData(),
  };
},
methods: {
  handleFileUpload(event) {
    const file = event.target.files[0];
    this.formData.append('archivo', file);
  },
  async submitForm() {
    try {
      const response = await fetch(`http://127.0.0.1:5000/mails/subir_mail/${this.legajoId}`, {
        method: 'POST',
        body: this.formData,
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