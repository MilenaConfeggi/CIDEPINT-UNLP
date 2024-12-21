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
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  
  const stans = ref([]);
  const selectedStan = ref(null);
  const authStore = useAuthStore();
  const seleccionados = ref([]);
  const cantidadSeleccionada = ref({});

  const mediosDePago = ref([]);
  const medioDePagoSeleccionado = ref("")
  
  
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
    const datosSeleccionados = seleccionados.value.map(id => ({
        id,
        cantidad: cantidadSeleccionada.value[id] || 0, // Usar 0 si no se ingresó cantidad
    }));

    try {
        const respuesta = await fetch(`${import.meta.env.VITE_API_URL}/presupuestos/crear`, {
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
        const datos = await respuesta.json();
        console.log('Respuesta del backend:', datos);
    } catch (error) {
        console.error('Error al enviar la selección:', error);
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