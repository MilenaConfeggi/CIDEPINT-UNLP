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
          <tr v-if="paginatedInterareas.length === 0">
            <td colspan="6" class="text-center">No hay solicitudes de interáreas disponibles.</td>
          </tr>
          <tr v-for="interarea in paginatedInterareas" :key="interarea.id" @click="highlightRow(interarea.id)" :class="{ 'table-active': selectedInterarea === interarea.id }">
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
    <nav aria-label="Paginación" class="mt-3">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="changePage(currentPage - 1)" :disabled="currentPage === 1">Anterior</button>
        </li>
        <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
          <button class="page-link" @click="changePage(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">Siguiente</button>
        </li>
      </ul>
    </nav>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const interareas = ref([]);
const currentPage = ref(1); 
const itemsPerPage = ref(8); 
const router = useRouter();
const area = localStorage.getItem("area");

const paginatedInterareas = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return interareas.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(interareas.value.length / itemsPerPage.value));

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

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
  await fetchInterareas();
});
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.page-item {
  list-style: none;
}

.page-link {
  display: inline-block;
  padding: 8px 12px;
  margin: 0 5px;
  border: 1px solid #007bff;
  border-radius: 4px;
  color: #007bff;
  background-color: white; 
  text-decoration: none;
  transition: all 0.3s ease;
}

.page-link:hover {
  background-color: #007bff;
  color: white;
}

.page-item.active .page-link {
  background-color: #0056b3;
  color: white;
  border-color: #0056b3;
}

.page-item.disabled .page-link {
  color: #ccc;
  cursor: not-allowed;
  background-color: #f8f9fa;
  border-color: #ddd;
}

.page-item.previous .page-link,
.page-item.next .page-link {
  padding: 8px 16px;
  font-weight: bold;
}

</style>
