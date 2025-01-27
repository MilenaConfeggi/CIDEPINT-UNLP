<template>
    <div class="statistics container mt-4">
        <h1 class="text-center mb-4">Estadísticas</h1>

        <div class="card mb-4 p-3">
            <h2 class="card-title text-center mb-3">Filtrar Ensayos</h2>
            <div class="row g-2">
                <div class="col-md-4">
                    <label for="startDate" class="form-label">Fecha de inicio:</label>
                    <input type="date" id="startDate" class="form-control" v-model="startDate" />
                </div>
                <div class="col-md-4">
                    <label for="endDate" class="form-label">Fecha de fin:</label>
                    <input type="date" id="endDate" class="form-control" v-model="endDate" />
                </div>
                <div class="col-md-4 d-flex align-items-end">
                    <button class="btn btn-primary w-100" @click="fetchEnsayos">Filtrar</button>
                </div>
            </div>
            <div v-if="error" class="text-danger mt-2">{{ error }}</div>
        </div>

        <div class="card mb-4 p-3">
            <h2 class="card-title text-center mb-3">Estadísticas de Ensayos</h2>
            <apexchart type="bar" :options="ensayosOptions" :series="ensayosSeries" />
        </div>

        <div class="card mb-4 p-3">
            <h2 class="card-title text-center mb-3">Estadísticas de Clientes</h2>
            <apexchart type="bar" :options="conformidadOptions" :series="conformidadSeries" />
        </div>

        <div class="card mb-4 p-3">
            <h2 class="card-title text-center mb-3">Estadísticas de Legajos</h2>
            <apexchart type="pie" :options="legajosOptions" :series="legajosSeries" />
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import VueApexCharts from 'vue3-apexcharts';
import { useAuthStore } from '@/stores/auth';
  
export default {
    name: 'Statistics',
    components: {
        apexchart: VueApexCharts,
    },
    data() {
        return {
            startDate: null,
            endDate: null,
            error: "",
            apiData: {
                conformidad: [],
                ensayos: [],
                legajos: [],
            },
            conformidadSeries: [],
            conformidadOptions: {},
            ensayosSeries: [],
            ensayosOptions: {},
            legajosSeries: [],
            legajosOptions: {},
        };
    },
    methods: {
        async fetchApiData() {
            try {
                const authStore = useAuthStore();
                const token = authStore.getToken();
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/estadisticas`,{
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                }
                );
                this.apiData = response.data;
                this.prepareChartData();
            } catch (error) {
                console.error('Hubo un problema al obtener los datos:', error);
            }
        },
        generateRandomColor() {
            const randomColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
            return randomColor;
        },
        prepareChartData() {
            this.conformidadSeries = [{
                    name: 'Cantidad',
                    data: this.apiData.conformidad.map((item) => item.cantidad),
                },
            ];
            this.conformidadOptions = {
                chart: {
                    type: 'bar',
                    toolbar: { show: false },
                },
                xaxis: {
                    categories: this.apiData.conformidad.map((item) => `Estrella ${item.categoria}`),
                },
                title: {
                    text: 'Conformidad por puntuación',
                    align: 'center',
                },
            };
  
            this.legajosSeries = this.apiData.legajos.map((item) => item.cantidad);
            this.legajosOptions = {
                chart: {
                    type: 'pie',
                },
                labels: this.apiData.legajos.map((item) => item.estado),
                title: {
                    text: 'Cantidad de legajos por estado',
                    align: 'center',
                },
            };
        },
        async fetchEnsayos() {
            try {
                if (!this.startDate || !this.endDate) {
                    this.error = 'Se deben seleccionar ambas fechas para filtrar los ensayos';
                    return;
                } else {
                    if (this.startDate > this.endDate) {
                        this.error = 'La fecha de inicio no puede ser mayor a la fecha de fin';
                        return;
                    } else {
                        this.error = "";
                    }
                }
                
                const formData = new FormData();
                formData.append('startDate', this.startDate);
                formData.append('endDate', this.endDate);

                const authStore = useAuthStore();
                const token = authStore.getToken();

                const response = await axios.post(`${import.meta.env.VITE_API_URL}/estadisticas/ensayos`, formData,{
                    headers: {
                    "Authorization": `Bearer ${token}`,
                    },
                }
                );

                this.apiData.ensayos = response.data;
    
                const totalEnsayos = this.apiData.ensayos.reduce((sum, item) => sum + item.cantidad, 0);
                const ensayosPorcentaje = this.apiData.ensayos.map((ensayo) => (ensayo.cantidad / totalEnsayos) * 100);
    
                this.ensayosSeries = [{
                        name: 'Porcentaje de Ensayos',
                        data: ensayosPorcentaje.map((porcentaje) => parseFloat(porcentaje.toFixed(2))),
                    },
                ];
    
                const colors = this.apiData.ensayos.map(() => this.generateRandomColor());
                this.ensayosOptions = {
                    chart: {
                        type: 'bar',
                        toolbar: { show: false },
                    },
                    xaxis: {
                        categories: this.apiData.ensayos.map((ensayo) => ensayo.nombre),
                    },
                    title: {
                        text: 'Porcentaje de ensayos más solicitados',
                        align: 'center',
                    },
                    plotOptions: {
                        bar: {
                            horizontal: true,
                        },
                    },
                    dataLabels: {
                        enabled: true,
                        formatter: (val) => `${val.toFixed(2)}%`,
                    },
                    colors,
                };
            } catch (error) {
                console.error('Hubo un problema al obtener los datos:', error);
            }
        },
    },
    mounted() {
        this.fetchApiData();
    },
  };
</script>
  
<style scoped>
.statistics {
    max-width: 800px;
    margin: 0 auto;
}
  
.card {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #fff;
}
  
.card-title {
    font-size: 1.5rem;
    color: #333;
}
  
.card h2 {
    margin-bottom: 1rem;
}
  
.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
}
  
.btn-primary:hover {
    background-color: #0056b3;
    border-color: #004085;
}
</style>