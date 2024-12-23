<template>
  <div class="container mt-4">
    <hr class="line">
    <h1 class="text-center mb-4">Listado de Interáreas</h1>
    <hr class="line">
    <div class="table-responsive mt-4">
      <table class="table table-hover table-bordered">
        <thead class="thead-dark">
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
          <tr v-for="interarea in interareas" :key="interarea.id" @click="highlightRow(interarea.id)" :class="{ 'table-active': selectedInterarea === interarea.id }">
            <td class="text-center">{{ interarea.nro_interarea }}</td>
            <td>
              <span v-if="!interarea.investigacion">Legajo {{ interarea.legajo.id }}</span>
              <span v-else>Linea {{ interarea.nro_investigacion }}</span>
            </td>
            <td>{{ interarea.area_solicitante.nombre }}</td>
            <td>{{ interarea.area_receptora.nombre }}</td>
            <td class="text-center">{{ interarea.fecha_creacion }}</td>
            <td class="text-center">
              <button @click.stop="showInfo(interarea)" class="btn btn-primary btn-sm me-2">Ver interárea</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const interareas = ref([]);
const router = useRouter();
const area = localStorage.getItem("area");

const fetchInterareas = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas`);
    if (!response.ok) {
      throw new Error("Error al obtener las interáreas");
    }
    const data = await response.json(); 
    if (area !== "null") {
      interareas.value = data.filter((interarea) => 
          interarea.area_solicitante.id === parseInt(area) || 
          interarea.area_receptora.id === parseInt(area)
      );
    } else {
      interareas.value = data; 
    }
  } catch (error) {
    console.error("Error al obtener las interáreas:", error);
  }
};

const showInfo = (interarea) => {
  router.push({ name: "InterareaDetalle", params: { id: interarea.id } });
};

onMounted(async () => {
  fetchInterareas(); 
});

</script>

<style scoped>
.table {
  width: 100%;
  margin: auto;
  border-collapse: collapse;
}

.table th, .table td {
  text-align: center;
  vertical-align: middle;
  padding: 10px;
}

.table-hover tbody tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}

.table-active {
  background-color: #d1ecf1;
}

.thead-dark th {
  background-color: #343a40;
  color: white;
}

.line {
  border: 0;
  height: 1px;
  background: #333;
  background-image: linear-gradient(to right, #ccc, #333, #ccc);
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
