<template>
  <div>
    <h3>Selecciona los Stans</h3>
    <form @submit.prevent="enviarSeleccion">
      <div class="checkbox-grid">
        <div v-for="stan in stans" :key="stan.id" class="checkbox-item">
          <input
            type="checkbox"
            :value="stan.id"
            v-model="seleccionados"
            id="stan-{{ stan.id }}"
            class="styled-checkbox"
          />
          <label :for="'stan-' + stan.id">
            {{ stan.numero }} - {{ stan.descripcion }}
          </label>
          <div v-if="seleccionados.includes(stan.id)" class="quantity-input">
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
      </div>

      <div class="file-upload">
        <label for="archivo">Subir PDF de presupuesto (opcional):</label>
        <input type="file" id="archivo" @change="handleFileUpload" accept="application/pdf" />
      </div>

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
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'vue-toastification';

const stans = ref([]);
const selectedStan = ref(null);
const authStore = useAuthStore();
const seleccionados = ref([]);
const cantidadSeleccionada = ref({});
const archivo = ref(null);

const route = useRoute();
const router = useRouter();
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

    if (response.status !== 200) {
      throw new Error("Error al obtener los usuarios");
    }

    stans.value = await response.json();
  } catch (error) {
    console.error("Error al obtener los stans:", error);
  }
};

const handleFileUpload = (event) => {
  archivo.value = event.target.files[0];
};

const enviarSeleccion = async () => {
  submitError.value = null; // Limpia errores previos
  successMessage.value = null; // Limpia mensajes previos

  // Validar que se haya seleccionado al menos un stan
  if (seleccionados.value.length === 0) {
    submitError.value = 'Debes seleccionar al menos un stan.';
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

  const token = authStore.getToken();
  const toast = useToast();

  try {
    if (archivo.value) {
      // Subir el PDF
      const formData = new FormData();
      formData.append('archivo', archivo.value);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/presupuestos/subir_presupuesto/${idLegajo}`, {
        method: 'POST',
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData,
      });

      const result = await response.json();
      if (response.status !== 200) {
        throw new Error(result.message || 'Error al subir el presupuesto');
      }

      toast.success(result.message);
      setTimeout(() => {
        router.push({ path: `/legajos/${idLegajo}` });
      }, 1500); // 1500 milisegundos = 1,5 segundos
    } else {
      // Generar el presupuesto automáticamente
      toast.info("Generando presupuesto...");
      const response = await fetch(`${import.meta.env.VITE_API_URL}/presupuestos/crear/${idLegajo}`, {
        method: 'POST',
        headers: {
          "Authorization": `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          seleccionados: datosSeleccionados,
          legajo: idLegajo,
        }),
      });

      const result = await response.json();
      if (response.status !== 200) {
        toast.error(result.message);
      } else {
        toast.success(result.message);
        setTimeout(() => {
          router.push({ path: `/legajos/${idLegajo}` });
        }, 1500); // 1500 milisegundos = 1,5 segundos
      }
    }
  } catch (err) {
    toast.error(err.message);
  }
};

onMounted(() => {
  fetchStans();
});
</script>

<style scoped>
.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* Acomoda 4 elementos por fila */
  gap: 0.5rem; /* Espaciado reducido */
  margin-top: 1rem;
}

.checkbox-item {
  display: flex;
  align-items: center; /* Alinea checkbox y texto horizontalmente */
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
  gap: 0.5rem; /* Espaciado entre checkbox y texto */
}

.custom-checkbox {
  width: 1.5rem; /* Tamaño más grande */
  height: 1.5rem;
  accent-color: #00c8ff; /* Color celeste */
  cursor: pointer;
}

.checkbox-item label {
  font-size: 0.9rem; /* Tamaño más pequeño para el texto */
  line-height: 1.2;
}

.checkbox-item:hover {
  background-color: #e6f7ff; /* Fondo celeste claro al pasar el mouse */
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

input[type="checkbox"].styled-checkbox {
  width: 15px;
  height: 15px;
  accent-color: #007bff; /* Color azul */
  cursor: pointer;
}

.file-upload {
  margin-top: 1rem;
}
</style>