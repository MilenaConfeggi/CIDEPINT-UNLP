<template>
  <div class="modal-backdrop" v-if="isOpen" role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <div class="modal-content" v-if="!showGenerarPresupuesto && !showGenerarPresupuestoPesos">
      <div class="modal-header">
        <h2 id="modal-title" class="modal-title">Detalles del Presupuesto</h2>
        <button class="close-button" @click="closeModal" aria-label="Cerrar modal">×</button>
      </div>
      <div class="modal-body">
                <!-- Sección de Presupuestos -->
        <div v-if="presupuestos.length > 0" class="presupuestos-section">
          <h3>Presupuestos</h3>
          <ul>
            <li v-for="archivo in presupuestos" :key="archivo">
              <a href="#" @click.prevent="abrirArchivo(archivo, 'presupuestos')">{{ archivo }}</a>
            </li>
          </ul>
        </div>

        <!-- Sección de Presupuestos Firmados -->
        <div v-if="presupuestosFirmados.length > 0" class="presupuestos-firmados-section">
          <h3>Presupuestos Firmados</h3>
          <ul>
            <li v-for="archivo in presupuestosFirmados" :key="archivo">
              <a href="#" @click.prevent="abrirArchivo(archivo, 'presupuestos_firmados')">{{ archivo }}</a>
            </li>
          </ul>
        </div>
      </div>
        <div class="action-section">
          <button
            v-if="hasPermission('generar_presupuesto')"
            class="btn btn-primary"
            @click="generarPresupuestoDolares"
          >
            Generar Presupuesto en Dólares
          </button>
          <button
            v-if="hasPermission('generar_presupuesto')"
            class="btn btn-primary"
            @click="generarPresupuestoPesos"
          >
            Generar Presupuesto en Pesos
          </button>
          <label
            v-if="hasPermission('cargar_presupuesto_firmado')"
            class="btn btn-success"
          >
            Subir Presupuesto Firmado
            <input
              type="file"
              accept="application/pdf"
              @change="subirPresupuestoFirmado"
              hidden
            />
          </label>
        </div>
        </div>

    <!-- Renderiza el componente GenerarPresupuesto -->
    <GenerarPresupuesto v-if="showGenerarPresupuesto" :legajoId="legajoId" @close="closeGenerarPresupuesto" />

    <!-- Renderiza el componente GenerarPresupuestoPesos -->
    <GenerarPresupuestoPesos v-if="showGenerarPresupuestoPesos" :legajoId="legajoId" @close="closeGenerarPresupuestoPesos" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { usePresupuestoStore } from '../../stores/presupuesto';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  isOpen: Boolean,
  legajoId: Number,
  hasPermission: Function,
});

const emit = defineEmits(['close']);
const presupuestoStore = usePresupuestoStore();
const toast = useToast();

const presupuestos = ref([]);
const presupuestosFirmados = ref([]);

const showGenerarPresupuesto = ref(false);
const showGenerarPresupuestoPesos = ref(false);

const closeModal = () => {
  emit('close');
};

const generarPresupuestoDolares = () => {
  router.push({ name: 'generar_presupuesto', params: { id_legajo: props.legajoId } });
};

const generarPresupuestoPesos = () => {
  router.push({ name: 'generar_presupuesto_en_pesos', params: { id_legajo: props.legajoId } });
};

const closeGenerarPresupuesto = () => {
  showGenerarPresupuesto.value = false;
};

const closeGenerarPresupuestoPesos = () => {
  showGenerarPresupuestoPesos.value = false;
};

const verPresupuesto = async () => {
  try {
    await presupuestoStore.verPresupuesto(props.legajoId);
  } catch (error) {
    console.error('Error al ver presupuesto:', error);
    toast.error('Error al ver presupuesto.');
  }
};

const subirPresupuestoFirmado = async (event) => {
  const file = event.target.files[0];
  if (file && file.type === 'application/pdf') {
    try {
      await presupuestoStore.uploadPresupuestoFirmado(event, null, props.legajoId);
      toast.success('Presupuesto firmado subido correctamente.');
      cargarPresupuestosFirmados(); // Recargar la lista de presupuestos firmados
    } catch (error) {
      console.error('Error al subir presupuesto firmado:', error);
      toast.error('Error al subir presupuesto firmado.');
    }
  } else {
    toast.warning('Por favor selecciona un archivo PDF.');
  }
};

const cargarPresupuestos = async () => {
  presupuestos.value = await presupuestoStore.fetchPresupuestos(props.legajoId);
};

const cargarPresupuestosFirmados = async () => {
  presupuestosFirmados.value = await presupuestoStore.fetchPresupuestosFirmados(props.legajoId);
};

const abrirArchivo = (archivo, tipo) => {
  const baseUrl = `${import.meta.env.VITE_API_URL}/presupuestos/ver_documento/${props.legajoId}`;
  const url = `${baseUrl}/${archivo}`;
  window.open(url, '_blank');
};

// Watch para cargar los datos cuando el modal se abre
watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      cargarPresupuestos();
      cargarPresupuestosFirmados();
    }
  }
);

onMounted(() => {
  // Carga inicial si el modal ya está abierto al montar el componente
  if (props.isOpen) {
    cargarPresupuestos();
    cargarPresupuestosFirmados();
  }
});
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background: #ffffff;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  max-height: 80%; /* Limita la altura máxima del modal */
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.close-button:hover {
  color: #000;
}

.modal-body {
  margin-top: 20px;
  overflow-y: auto; /* Habilita el scroll vertical */
  max-height: calc(100% - 60px); /* Ajusta la altura máxima del cuerpo del modal */
  padding-right: 10px; /* Espacio para evitar que el scroll tape el contenido */
}

.action-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-success {
  background-color: #28a745;
  color: #fff;
  border: none;
}

.btn-success:hover {
  background-color: #218838;
}
</style>