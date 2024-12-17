<template>
  <div class="table-responsive mt-4">
    <table class="table table-striped table-hover table-bordered">
      <thead class="table-light">
        <tr>
          <th scope="col" class="text-center">Nro</th>
          <th scope="col">Legajo/Linea de Investigación</th>
          <th scope="col">Área Solicitante</th>
          <th scope="col">Área Receptora</th>
          <th scope="col" class="text-center">Fecha Solicitud</th>
          <th scope="col" class="text-center">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="interareas.length === 0">
          <td colspan="6" class="text-center">No hay solicitudes de interáreas disponibles.</td>
        </tr>
        <tr v-for="interarea in interareas" :key="interarea.id">
          <td class="text-center">{{ interarea.nro_interarea }}</td>
          <td>
            <span v-if="interarea.investigacion">Legajo {{ interarea.legajo_id }}</span>
            <span v-else>Linea {{ interarea.legajo_id }}</span>
          </td>
          <td>{{ interarea.muestra_id }}</td>
          <td>{{ interarea.area_receptora || "Sin área asignada" }}</td>
          <td class="text-center">{{ formatFecha(interarea.fecha_solicitud_no_firmada) }}</td>
          <td class="text-center">
            <button @click="showInfo(interarea)" class="btn btn-primary btn-sm me-2">Ver interárea</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
  
<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router"; // Importar useRouter

const interareas = ref([]);
const router = useRouter();

const fetchInterareas = async () => {
try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas`);
    if (!response.ok) {
    throw new Error("Error al obtener las interáreas");
    }
    interareas.value = await response.json();
} catch (error) {
    console.error("Error al obtener las interáreas:", error);
}
};

const formatFecha = (fecha) => {
if (!fecha) return "Sin fecha";
const options = { year: "numeric", month: "long", day: "numeric" };
return new Date(fecha).toLocaleDateString("es-ES", options);
};

const showInfo = (interarea) => {
    router.push({ name: "InterareaDetalle", params: { id: interarea.id } });
};

onMounted(() => {
fetchInterareas();
});
</script>
  