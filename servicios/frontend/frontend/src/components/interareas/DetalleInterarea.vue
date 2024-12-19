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
                    <span class="ms-2">{{ formatFecha(interarea.fecha_creacion) }}</span>
                </p>
                <p v-if="mostrarResultado">
                    <span class="fw-bold text-secondary">Resultado:</span>
                    <span class="ms-2">{{ interarea.resultados }}</span>
                </p>
            </div>
        </div>
        <div v-else class="alert alert-warning text-center mt-4">
            No se ha encontrado la interárea.
        </div>

        <div class="text-center mt-4">
            <button v-if="interarea && interarea.estadoInterarea_id == 2" @click="toggleInputResultado" class="btn btn-primary">Cargar Resultado</button>
            <button v-if="interarea && interarea.estadoInterarea_id == 1" class="btn btn-secondary" @click="mostrarSubirSolicitud = !mostrarSubirSolicitud">Subir Solicitud Firmada</button>
            <button v-if="interarea && interarea.estadoInterarea_id == null" class="btn btn-secondary" @click="mostrarSubirSolicitudCompleta = !mostrarSubirSolicitudCompleta">Cargar solicitud completa</button>
            <button @click="descargarInterarea" class="btn btn-secondary">Descargar solicitud</button>
            <button v-if="interarea && interarea.estadoInterarea_id == 3" @click="toggleResultado" class="btn btn-secondary">Ver resultados</button>
            <button @click="volverAlListado" class="btn btn-secondary">Volver al Listado</button>
        </div>

        <!-- Input para subir solicitud firmada -->
        <div v-if="mostrarSubirSolicitud" class="mt-4 text-center">
            <input 
                type="file" 
                accept=".doc, .docx"
                @change="onFileChange" 
                class="form-control w-50 mx-auto"
            />
            <button @click="subirSolicitudFirmada" class="btn btn-success mt-3">Subir Solicitud</button>
        </div>

        <!-- Input para subir solicitud completa -->
        <div v-if="mostrarSubirSolicitudCompleta" class="mt-4 text-center">
            <input 
                type="file" 
                accept=".doc, .docx" 
                @change="onFileChangeCompleta" 
                class="form-control w-50 mx-auto"
            />
            <button @click="subirSolicitudCompleta" class="btn btn-success mt-3">Subir Solicitud Completa</button>
        </div>

        <!-- Input de texto libre que aparece al presionar "Cargar Resultado" -->
        <div v-if="mostrarInput" class="mt-4 text-center">
            <input 
                type="text" 
                class="form-control w-50 mx-auto" 
                placeholder="Escribe el resultado aquí..." 
                v-model="resultado"
            />
            <button @click="guardarResultado" class="btn btn-success mt-3">Guardar Resultado</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const interarea = ref(null);
const mostrarInput = ref(false); // Controla si el input de resultado se muestra o no
const mostrarSubirSolicitud = ref(false); // Controla si el input de subida de solicitud se muestra o no
const mostrarSubirSolicitudCompleta = ref(false); // Controla si el input de subida de solicitud completa se muestra o no
const mostrarResultado = ref(false); // Controla si el resultado se muestra o no
const resultado = ref(""); // Almacena el texto ingresado como resultado
const archivo = ref(null); // Almacena el archivo seleccionado
const archivoCompleto = ref(null); // Almacena el archivo de solicitud completa seleccionado

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

const fetchDescargarSolicitud = async (nombreSolicitud) => {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas/descargar/${nombreSolicitud}`);
        if (!response.ok) {
            throw new Error("Error al descargar la solicitud");
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = nombreSolicitud;
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error("Error al descargar la solicitud:", error);
    }
};

onMounted(() => {
    const id = route.params.id;
    fetchInterarea(id);
});

const volverAlListado = () => {
    router.push({ name: "interareas" });
};

const descargarInterarea = () => {
    fetchDescargarSolicitud(interarea.value.nombre_archivo);
};

const formatFecha = (fecha) => {
    if (!fecha) return "Sin fecha";
    const options = { year: "numeric", month: "long", day: "numeric" };
    return new Date(fecha).toLocaleDateString("es-ES", options);
};

// Funciones para manejar el input de resultado
const toggleInputResultado = () => {
    mostrarInput.value = !mostrarInput.value;
};

const guardarResultado = async () => {
    if (!resultado.value) {
        alert("El campo de resultado está vacío.");
        return;
    }
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas/guardar_resultado/${interarea.value.id}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nro_interarea: interarea.value.nro_interarea,
                resultado: resultado.value,
            }),
        });

        if (!response.ok) {
            throw new Error("Error al guardar el resultado");
        }

        alert("Resultado guardado con éxito");
        resultado.value = ""; // Limpiar el campo
        mostrarInput.value = false; // Ocultar el input después de guardar
    } catch (error) {
        console.error("Error al guardar el resultado:", error);
        alert("Hubo un error al guardar el resultado.");
    }
};

// Funciones para manejar el archivo de solicitud firmada
const onFileChange = (event) => {
    const files = event.target.files;
    if (files && files[0]) {
        archivo.value = files[0];
    }
};

const subirSolicitudFirmada = async () => {
    if (!archivo.value) {
        alert("Por favor selecciona un archivo antes de subir.");
        return;
    }

    const formData = new FormData();
    formData.append("archivo", archivo.value);
    formData.append("id", interarea.value.id);

    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas/cargar_archivo_firmado/${interarea.value.id}`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Error al subir la solicitud firmada");
        }

        alert("Solicitud firmada subida con éxito");
        archivo.value = null; // Limpiar el archivo
        mostrarSubirSolicitud.value = false; // Ocultar el formulario
    } catch (error) {
        console.error("Error al subir la solicitud firmada:", error);
        alert("Hubo un error al subir la solicitud firmada.");
    }
};

// Funciones para manejar el archivo de solicitud completa
const onFileChangeCompleta = (event) => {
    const files = event.target.files;
    if (files && files[0]) {
        archivoCompleto.value = files[0];
    }
};

const subirSolicitudCompleta = async () => {
    if (!archivoCompleto.value) {
        alert("Por favor selecciona un archivo antes de subir.");
        return;
    }

    const formData = new FormData();
    formData.append("archivo", archivoCompleto.value);
    formData.append("id", interarea.value.id);

    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas/cargar_archivo_completo/${interarea.value.id}`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Error al subir la solicitud completa");
        }

        alert("Solicitud completa subida con éxito");
        archivoCompleto.value = null; // Limpiar el archivo
        mostrarSubirSolicitudCompleta.value = false; // Ocultar el formulario
    } catch (error) {
        console.error("Error al subir la solicitud completa:", error);
        alert("Hubo un error al subir la solicitud completa.");
    }
};

// Función para manejar la visualización del resultado
const toggleResultado = () => {
    mostrarResultado.value = !mostrarResultado.value;
};
</script>

<style scoped>
.container {
    max-width: 800px;
}
</style>