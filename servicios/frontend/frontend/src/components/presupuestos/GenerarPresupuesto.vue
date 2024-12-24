<template>
    <div>
      <h3>Selecciona los Stans</h3>
      <form @submit.prevent="enviarSeleccion">
        <div v-for="stan in stans" :key="stan.id">
          <input
            type="checkbox"
            :value="stan.id"
            v-model="seleccionados"
          />
          <label>{{ stan.numero }} Desc: {{ stan.descripcion }}</label>
          <div v-if="seleccionados.includes(stan.id)">
            
            <div v-if="stan.precio_por_muestra">
                Cantidad de muestras: 
            </div>
            <div v-else>
                Cantidad de horas:
            </div>
          <input
            v-model="cantidadSeleccionada[stan.id]"
            type="number"
            min="1"
            placeholder="Cantidad"
          />
        </div>
        </div>
        <h3>Selecciona un medio de pago</h3>
        <select v-model="medioDePagoSeleccionado">
          <option value="" disabled>Elige un medio de pago</option>
          <option v-for="medio in mediosDePago" :key="medio.id" :value="medio.id">
          {{ medio.medio_de_pago }}
          </option>
        </select>
        <br>
        <button type="submit">Aceptar</button>
      </form>
        <div v-if="fetchError" class="alert alert-danger mb-4" role="alert">
          {{ fetchError }}
        </div>
        <div v-if="submitError" class="alert alert-danger mb-4" role="alert">
          {{ submitError }}
        </div>
        <div v-if="successMessage" class="alert alert-success mb-4" role="alert">
          {{ successMessage }}
        </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { useAuthStore } from '@/stores/auth';
  
  const stans = ref([]);
  const selectedStan = ref(null);
  const authStore = useAuthStore();
  const seleccionados = ref([]);
  const cantidadSeleccionada = ref({});

  const mediosDePago = ref([]);
  const medioDePagoSeleccionado = ref("")

  const route = useRoute();
  const idLegajo = route.params.id_legajo;

  const fetchError = ref(null);
  const submitError = ref(null);
  const successMessage = ref(null);
  
  
  const fetchStans = async () => {
    try {
      const token = authStore.getToken();
      const response = await fetch(`${import.meta.env.VITE_API_URL}/presupuestos/stans`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
      });
  
      if (!response.ok) {
        throw new Error("Error al obtener los usuarios");
      }
  
      stans.value = await response.json();
    } catch (error) {
      console.error("Error al obtener los stans:", error);
    }
  };
  const fetchMediosDePago = async () => {
    try {
      const token = authStore.getToken();
      const response = await fetch(`${import.meta.env.VITE_API_URL}/presupuestos/medios_de_pago`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
      });
  
      if (!response.ok) {
        throw new Error("Error al obtener los medios de pago");
      }
  
      mediosDePago.value = await response.json();
    } catch (error) {
      console.error("Error al obtener los medios de pago:", error);
    }
  };
  const highlightRow = (id) => {
    selectedStan.value = id;
  };

  const enviarSeleccion = async () => {
    // Crear un arreglo con los datos a enviar: id y cantidad

    submitError.value = null; // Limpia errores previos
    successMessage.value = null; // Limpia mensajes previos

    // Validar que se haya seleccionado al menos un stan
    if (seleccionados.value.length === 0) {
      submitError.value = 'Debes seleccionar al menos un stan.';
      return;
    }

    // Validar que se haya seleccionado un método de pago
    if (!medioDePagoSeleccionado.value) {
      submitError.value = 'Debes seleccionar un método de pago.';
      return;
    }

    // Crear un arreglo con los datos a enviar: id y cantidad
    const datosSeleccionados = seleccionados.value.map((id) => ({
      id,
      cantidad: cantidadSeleccionada.value[id] || 0, // Usar 0 si no se ingresó cantidad
    }));

    // Validar que todas las cantidades sean mayores a 0
    const cantidadesInvalidas = datosSeleccionados.some(
      (item) => item.cantidad <= 0
    );
    if (cantidadesInvalidas) {
      submitError.value = 'Todos los stans seleccionados deben tener una cantidad mayor a 0.';
      return;
    }

    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/presupuestos/crear/${idLegajo}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            seleccionados: datosSeleccionados,
            medioDePago: medioDePagoSeleccionado.value,
            legajo: 33,
        }),
        });
        console.log("Datos enviados:", {
        seleccionados: datosSeleccionados,
        medioDePago: medioDePagoSeleccionado.value,
        legajo: 1,
        });
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.message || 'Error al generar el certificado');
        }
  
        successMessage.value = result.message;
    } catch (err) {
      submitError.value = err.message || 'Error desconocido';
    }
  };
  
  onMounted(() => {
    fetchStans();
    fetchMediosDePago();
  });
  </script>
  
  <style scoped>
  form {
    margin-top: 1rem;
  }
  div {
    margin-bottom: 0.5rem;
  }
  button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  button:hover {
    background-color: #0056b3;
  }
  </style>