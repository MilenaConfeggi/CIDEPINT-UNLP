<template>
    <div class="container my-5">
        <h1 class="text-center mb-4">Detalles de la Interárea</h1>
        <div v-if="interarea" class="card shadow-sm border-0">
            <div class="card-body">
                <p class="mb-3">
                    <span class="fw-bold text-secondary">Nro Interarea:</span>
                    <span class="ms-2">{{ interarea.nro_interarea }}</span>
                </p>
                <p class="mb-3">
                    <span v-if="!interarea.investigacion">
                        <span class="fw-bold text-secondary">Legajo:</span>
                        <span class="ms-2">{{ interarea.legajo.id }}</span>
                    </span>
                    <span v-else>
                        <span class="fw-bold text-secondary">Línea de Investigación:</span>
                        <span class="ms-2">{{ interarea.nro_investigacion }}</span>
                    </span>
                </p>
                <p class="mb-3">
                    <span class="fw-bold text-secondary">Área Solicitante:</span>
                    <span class="ms-2">{{ interarea.area_solicitante.nombre }}</span>
                </p>
                <p class="mb-3">
                    <span class="fw-bold text-secondary">Área Receptora:</span>
                    <span class="ms-2">{{ interarea.area_receptora.nombre }}</span>
                </p>
                <p class="mb-3">
                    <span class="fw-bold text-secondary">Fecha Solicitud:</span>
                    <span class="ms-2">{{ interarea.fecha_creacion }}</span>
                </p>
                <p v-if="mostrarResultado" class="mb-3">
                    <span class="fw-bold text-secondary">Resultado:</span>
                    <span class="ms-2">{{ interarea.resultados }}</span>
                </p>
            </div>
        </div>

        <div v-else class="alert alert-warning text-center mt-4">No se ha encontrado la interárea.</div>
      
        <div class="text-center mt-4">
            <button v-if="debeMostrarCargarResultado()" @click="toggleInputResultado" class="btn btn-success me-2">Cargar Resultado</button>
            <button v-if="debeMostrarSubirSolicitudFirmada() && tienePermisoCargarFirma" @click="toggleSubirSolicitudFirmada" class="btn btn-secondary me-2">Subir Solicitud Firmada</button>
            <button v-if="debeMostrarCargarSolicitudCompleta()" @click="toggleSubirSolicitudCompleta" class="btn btn-secondary me-2">Cargar Solicitud Completa</button>
            <button v-if="debeMostrarVerResultados()" @click="toggleResultado" class="btn btn-secondary me-2">Ver Resultados</button>
            <button @click="descargarInterarea" class="btn btn-secondary me-2">Descargar Solicitud</button>
            <button @click="volverAlListado" class="btn btn-secondary">Volver al Listado</button>
        </div>
      
        <div v-if="mensajeExito" class="alert alert-success mt-4 text-center">
            {{ mensajeExito }}
        </div>
      
        <div v-if="mostrarSubirSolicitud" class="mt-4 text-center">
            <input type="file" accept=".doc, .docx" @change="onFileChange" class="form-control w-50 mx-auto"/>
            <button @click="subirSolicitudFirmada" class="btn btn-success mt-3">Subir Solicitud</button>
            <div v-if="errorArchivo" class="text-danger mt-2">{{ errorArchivo }}</div>
        </div>
      
        <div v-if="mostrarSubirSolicitudCompleta" class="mt-4 text-center">
            <input type="file" accept=".doc, .docx" @change="onFileChange" class="form-control w-50 mx-auto"/>
            <button @click="subirSolicitudCompleta" class="btn btn-success mt-3">Subir Solicitud Completa</button>
            <div v-if="errorArchivo" class="text-danger mt-2">{{ errorArchivo }}</div>
        </div>
      
      <div v-if="mostrarInput" class="mt-4 text-center">
        <input type="text" class="form-control w-50 mx-auto" placeholder="Escribe el resultado aquí..." v-model="resultado"/>
        <button @click="guardarResultado" class="btn btn-success mt-3">Guardar Resultado</button>
        <div v-if="errorResultado" class="text-danger mt-2">{{ errorResultado }}</div>
      </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const interarea = ref(null);
const mostrarInput = ref(false);
const mostrarSubirSolicitud = ref(false);
const mostrarSubirSolicitudCompleta = ref(false);
const mostrarResultado = ref(false);
const resultado = ref("");
const archivo = ref(null);
const area = localStorage.getItem("area");
const errorArchivo = ref("");
const errorResultado = ref("");
const mensajeExito = ref("");
const permisos = JSON.parse(localStorage.getItem('permisos')) || [];

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
    } catch (error) {
        console.error("Error al descargar la solicitud:", error);
    }
};

const guardarResultado = async () => {
    errorResultado.value = "";
    if (!resultado.value) {
        errorResultado.value = "El campo de resultado está vacío.";
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

        mensajeExito.value = "Resultado guardado con éxito"; 
        resultado.value = ""; 
        mostrarInput.value = false;

        setTimeout(() => {
            mensajeExito.value = "";
        }, 3000);
    } catch (error) {
        console.error("Error al guardar el resultado:", error);
    }
};

const subirSolicitudFirmada = async () => {
    if (!archivo.value) {
        errorArchivo.value = "Por favor selecciona un archivo antes de subir.";
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

        mensajeExito.value = "Archivo cargado con éxito"; 
        resultado.value = ""; 
        mostrarInput.value = false;

        setTimeout(() => {
            mensajeExito.value = "";
        }, 3000);

        archivo.value = null; 
        mostrarSubirSolicitud.value = false; 
    } catch (error) {
        console.error("Error al subir la solicitud firmada:", error);
    }
};

const subirSolicitudCompleta = async () => {
    if (!archivo.value) {
        errorArchivo.value = "Por favor selecciona un archivo antes de subir.";
        return;
    }

    const formData = new FormData();
    formData.append("archivo", archivo.value);
    formData.append("id", interarea.value.id);

    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/interareas/cargar_archivo_completo/${interarea.value.id}`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Error al subir la solicitud completa");
        }

        mensajeExito.value = "Archivo cargado con éxito"; 
        resultado.value = ""; 
        mostrarInput.value = false;

        setTimeout(() => {
            mensajeExito.value = "";
        }, 3000);

        archivo.value = null; 
        mostrarSubirSolicitudCompleta.value = false;
    } catch (error) {
        console.error("Error al subir la solicitud completa:", error);
    }
};

const debeMostrarCargarResultado = () => {
    return interarea.value && (interarea.value.estadoInterarea_id == 2 && interarea.value.area_receptora.id === parseInt(area));
};

const debeMostrarSubirSolicitudFirmada = () => {
    return interarea.value && interarea.value.estadoInterarea_id == 1;
};

const debeMostrarCargarSolicitudCompleta = () => {
    return interarea.value && interarea.value.estadoInterarea_id == null;
};

const debeMostrarVerResultados = () => {
    return interarea.value && interarea.value.estadoInterarea_id == 3;
};

const toggleInputResultado = () => {
    mostrarInput.value = !mostrarInput.value;
};

const onFileChange = (event) => {
    const files = event.target.files;
    errorArchivo.value = "";
    if (files && files[0]) {
        const file = files[0];
        const fileType = file.name.split('.').pop().toLowerCase();
        if (fileType !== 'doc' && fileType !== 'docx') {
            errorArchivo.value = "El archivo debe ser de tipo .doc o .docx.";
            archivo.value = null;
        } else {
            archivo.value = file;
        }
    }
};


const toggleResultado = () => {
    mostrarResultado.value = !mostrarResultado.value;
};

const volverAlListado = () => {
    router.push({ name: "interareas" });
};

const descargarInterarea = () => {
    fetchDescargarSolicitud(interarea.value.nombre_archivo);
};

const toggleSubirSolicitudFirmada = () => {
    mostrarSubirSolicitud.value = !mostrarSubirSolicitud.value;
};

const toggleSubirSolicitudCompleta = () => {
    mostrarSubirSolicitudCompleta.value = !mostrarSubirSolicitudCompleta.value;
};

const tienePermisoCargarFirma = computed(() => {
  return permisos.includes('cargar_interarea_firmada');
});

onMounted(() => {
    const id = route.params.id;
    fetchInterarea(id);
});
</script>

<style scoped>
h1 {
    font-weight: bold;
}

.card {
    border-radius: 10px;
    background: linear-gradient(145deg, #ffffff, #f3f3f3);
}

.card-body {
    font-size: 1rem;
    line-height: 1.6;
}

.card-body span.fw-bold {
    color: #343a40;
}

.btn-primary {
    background-color: #4a90e2;
    border-color: #4a90e2;
}

.btn-primary:hover {
    background-color: #357abd;
    border-color: #357abd;
}

.btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
}

.btn-secondary:hover {
    background-color: #5a6268;
    border-color: #5a6268;
}

.alert {
    border-radius: 8px;
}

.form-control {
    border-radius: 5px;
}

.form-control:focus {
    box-shadow: 0 0 5px rgba(74, 144, 226, 0.5);
    border-color: #4a90e2;
}

.container {
    max-width: 800px;
}

.mt-3 button {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border-color: #c3e6cb;
}

.alert-warning {
    background-color: #fff3cd;
    color: #856404;
    border-color: #ffeeba;
}

input[type="file"] {
    padding: 10px;
    border: 2px dashed #ddd;
    background-color: #f9f9f9;
    border-radius: 10px;
    outline: none;
    transition: border-color 0.3s ease-in-out;
}

input[type="file"]:hover {
    border-color: #4a90e2;
}

input[type="text"] {
    border: 2px solid #ddd;
    padding: 10px;
}

input[type="text"]:focus {
    border-color: #4a90e2;
    box-shadow: 0 0 5px rgba(74, 144, 226, 0.5);
}
</style>
