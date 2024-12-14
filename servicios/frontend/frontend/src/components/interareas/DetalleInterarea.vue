<template>
    <div class="container my-5">
        <h1 class="text-center mb-4">Detalles de la Interárea</h1>
        <div v-if="interarea" class="card shadow-sm">
            <div class="card-body">
                <p class="fw-bold">
                    <span class="text-secondary">Nro Interarea:</span>
                    <span class="ms-2">{{ interarea.nro_interarea }}</span>
                </p>
                <p>
                    <span class="fw-bold text-secondary">Legajo/Investigación:</span>
                    <span class="ms-2">{{ interarea.legajo_id }}</span>
                </p>
                <p>
                    <span class="fw-bold text-secondary">Área Solicitante:</span>
                    <span class="ms-2">{{ interarea.muestra_id }}</span>
                </p>
                <p>
                    <span class="fw-bold text-secondary">Área Receptora:</span>
                    <span class="ms-2">{{ interarea.area_receptora }}</span>
                </p>
                <p>
                    <span class="fw-bold text-secondary">Fecha Solicitud:</span>
                    <span class="ms-2">{{ formatFecha(interarea.fecha_solicitud_no_firmada) }}</span>
                </p>
            </div>
        </div>
        <div v-else class="alert alert-warning text-center mt-4">
            No se ha encontrado la interárea.
        </div>
        <div class="text-center mt-4">
            <button CargarResultado class="btn btn-primary">Cargar Resultado</button>
            <button class="btn btn-secondary">Cargar solicitud firmada</button>
            <button class="btn btn-secondary">Descargar solicitud</button>
            <button class="btn btn-secondary">Ver resultados</button>
            <button @click="volverAlListado" class="btn btn-secondary">Volver al Listado</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router"; // Importa ambas funciones

const interarea = ref(null);

// Obtén las instancias de route y router
const route = useRoute();
const router = useRouter();

const fetchInterarea = async (id) => {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas/${id}`);
        if (!response.ok) {
            throw new Error("Error al obtener los detalles de la interárea");
        }
        interarea.value = await response.json();
    } catch (error) {
        console.error("Error al obtener la interárea:", error);
    }
};

onMounted(() => {
    const id = route.params.id;
    fetchInterarea(id);
});

const volverAlListado = () => {
    router.push({ name: "interareas" }); // Realiza la navegación al listado
};

const formatFecha = (fecha) => {
    if (!fecha) return "Sin fecha";
    const options = { year: "numeric", month: "long", day: "numeric" };
    return new Date(fecha).toLocaleDateString("es-ES", options);
};
</script>
