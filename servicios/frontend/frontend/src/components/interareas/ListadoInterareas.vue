<template>
<div className="table-responsive">
    <table className="table table-bordered table-hover">
    <thead className="table-light">
        <tr>
        <th scope="col">Nro</th>
        <th scope="col">Legajo/Linea de Investigación</th>
        <th scope="col">Área Solicitante</th>
        <th scope="col">Área receptora</th>
        <th scope="col">Fecha solicitud</th>
        <th scope="col">Acciones</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="interarea in interareas" :key="interarea.id">
            <td>{{ interarea.nro_interarea }}</td>
            <td v-if="interarea.investigacion">Legajo {{ interarea.legajo_id }}</td>
            <td v-else>Linea {{ interarea.legajo_id }}</td>
            <td>{{ interarea.muestra_id }}</td>
            <td> ? </td>
            <td>{{ interarea.fecha_solicitud_no_firmada }}</td>
            <td>
                <button>a</button>
            </td>
        </tr>
    </tbody>
    </table>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const interareas = ref([]);

const emitInterareas = () => {
    emit('interareasFetched', interareas.value);
};

const fetchInterareas = async () => {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas`);
        if (!response.ok) {
            throw new Error('Error al obtener las interareas');
        }
        interareas.value = await response.json();
        emitInterareas();
    } catch (error) {
        console.error('Error al obtener las interareas:', error);
    }
};

onMounted(() => {
    fetchInterareas();
});
</script>