<template>
    <div class="container mt-4">
        <div class="card">
        <div class="card-body">
            <h4 class="card-title text-center">Solicitar Interarea</h4>

            <form>
            <!-- Selección de legajo o línea de investigación -->
            <div class="mb-3 row">
                <label class="col-md-4 col-form-label">Seleccionar legajo o ingresar línea de investigación</label>
                <div class="col-md-3">
                
                </div>
                <div class="col-md-5">
                <input
                    
                    type="text"
                    class="form-control"
                    placeholder="Ingresar línea de investigación"
                />
                </div>
            </div>

            <!-- Selección de área -->
            <div class="mb-3">
                <label class="form-label">Seleccionar área</label>
                
            </div>

            <!-- Material a ensayar -->
            <div class="mb-3">
                <label class="form-label">Material a ensayar</label>
                <input
                type="text"
                class="form-control"
                placeholder="Ingresar material a ensayar"
                />
            </div>

            <!-- Selección de identificación de muestras -->
            <div class="mb-3">
                <label class="form-label">Seleccionar identificación de muestras</label>
            </div>

            <!-- Botón de envío -->
            <div class="text-center">
                <button type="submit" class="btn btn-primary">
                Enviar
                </button>
            </div>
            </form>
        </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'NuevaInterarea',
};
</script>