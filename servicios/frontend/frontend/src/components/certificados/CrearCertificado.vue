<template>
  <div class="container mt-4">
    <hr class="line">
    <h1 class="text-center mb-4">Generar Certificado</h1>
    <hr class="line">
    <form @submit.prevent="submitForm" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 form-container">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Seleccionar Empleado:</label>
        <select v-model="selectedEmpleado" @change="agregarEmpleado" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
          <option value="" disabled selected>Seleccione un empleado</option>
          <option v-for="empleado in empleados" :key="empleado.id" :value="empleado">{{ empleado.nombre }} {{ empleado.apellido }}</option>
        </select>
      </div>
      <div v-for="(empleado, index) in empleadosSeleccionados" :key="index" class="mb-4 card">
        <div class="card-header">
          <label class="block text-gray-700 text-sm font-bold mb-2">{{ empleado.nombre }} {{ empleado.apellido }}</label>
          <button type="button" @click="eliminarEmpleado(index)" class="delete-button">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
        <div class="card-body">
          <div class="mb-2">
            <label class="block text-gray-700 text-sm font-bold mb-2">Función:</label>
            <select v-model="empleado.funcion" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
              <option value="Responsable del equipo">Responsable del equipo</option>
              <option value="Integrante del equipo">Integrante del equipo</option>
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-700 text-sm font-bold mb-2">Porcentaje de Participación:</label>
            <input type="number" v-model="empleado.participacion" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" step="0.01" min="0" required>
          </div>
        </div>
      </div>
      <div class="mb-4">
        <label for="descripcion" class="block text-gray-700 text-sm font-bold mb-2">Descripción de la actividad tecnológica:</label>
        <textarea id="descripcion" v-model="descripcion" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 descripcion-input" rows="4"></textarea>
      </div>
      <div v-if="fetchError" class="alert alert-danger mb-4" role="alert">
        {{ fetchError }}
      </div>
      <div v-if="submitError" class="alert alert-danger mb-4" role="alert">
        {{ submitError }}
      </div>
      <div v-if="successMessage" class="alert alert-success mb-4" role="alert">
        {{ successMessage }}
      </div>
      <div class="flex items-center justify-between" v-if="!fetchError">
        <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Generar Certificado</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

const toast = useToast();
const router = useRouter();
const route = useRoute();
const idLegajo = route.params.id_legajo;

const empleados = ref([]);
const empleadosSeleccionados = ref([]);
const selectedEmpleado = ref(null);
const descripcion = ref('');
const fetchError = ref(null);
const submitError = ref(null);
const successMessage = ref(null);

const fetchEmpleados = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/usuarios/todos`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    const result = await response.json();
    if (response.status !== 200) {
      throw new Error(result.message || 'Error al obtener los empleados');
    }
    empleados.value = result.map(empleado => ({
      id: empleado.id,
      nombre: empleado.nombre,
      apellido: empleado.apellido,
    }));
  } catch (err) {
    fetchError.value = err.message || 'Error desconocido';
  }
};

const fetchDescripcion = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/certificado/chequear_descripcion_existente/${idLegajo}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });

    const result = await response.json();
    console.log('Descripción recibida:', result);

    if (response.status !== 200) {
      throw new Error('Error al obtener la descripción');
    }

    descripcion.value = result || '';
    console.log('Descripción actualizada:', descripcion.value);
  } catch {
    descripcion.value = '';
    console.log('No se pudo obtener la descripción, el campo queda vacío.');
  }
};

const agregarEmpleado = () => {
  if (selectedEmpleado.value && !empleadosSeleccionados.value.some(e => e.id === selectedEmpleado.value.id)) {
    empleadosSeleccionados.value.push({
      ...selectedEmpleado.value,
      nombre: selectedEmpleado.value.nombre,
      apellido: selectedEmpleado.value.apellido,
      funcion: 'Integrante del equipo',
      participacion: 0,
    });
    selectedEmpleado.value = null;
  }
};

const eliminarEmpleado = (index) => {
  empleadosSeleccionados.value.splice(index, 1);
};

const submitForm = async () => {
  submitError.value = null;
  successMessage.value = null;

  if (!descripcion.value.trim()) {
    submitError.value = 'La descripción no puede estar vacía';
    return;
  }

  const sumaParticipacion = empleadosSeleccionados.value.reduce((total, empleado) => {
    return total + parseFloat(empleado.participacion || 0);
  }, 0);

  if (sumaParticipacion !== 100) {
    submitError.value = 'La suma de las participaciones debe ser igual a 100';
    return;
  }

  const data = {
    empleados: empleadosSeleccionados.value,
    descripcion: descripcion.value,
  };

  console.log('Datos enviados:', data);

  try {
    toast.info('Generando certificado...');
    const response = await fetch(`${import.meta.env.VITE_API_URL}/certificado/crear/${idLegajo}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    console.log('Respuesta del servidor:', result);

    if (response.status !== 200) {
      throw new Error(result.message || 'Error al generar el certificado');
    }
    toast.success('Certificado generado correctamente');
    successMessage.value = result.message;
    setTimeout(() => {
      router.push(`/legajos/${idLegajo}`);
    }, 1500);
  } catch (err) {
    toast.error('Error al generar el certificado');
    submitError.value = err.message || 'Error desconocido';
  }
};

onMounted(() => {
  fetchEmpleados();
  fetchDescripcion();
});
</script>

<style scoped>
.line {
  border: 0;
  height: 1px;
  background: #333;
  background-image: linear-gradient(to right, #ccc, #333, #ccc);
}

.form-container {
  max-height: 600px; 
  overflow-y: auto;
}

.descripcion-input {
  width: 100%; /* Ajusta el ancho al 100% del contenedor */
}

button {
  background-color: #28a745; 
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #218838; 
}

.delete-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #dc3545;
  font-size: 1.5rem;
  padding: 0;
}

.delete-button:hover {
  background-color: #ffdada;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-body {
  padding: 8px 0;
}

.alert {
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}
</style>