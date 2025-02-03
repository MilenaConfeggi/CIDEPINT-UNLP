<script setup>
import 'survey-core/defaultV2.min.css'
import { Model } from 'survey-core'
import { SurveyComponent } from 'survey-vue3-ui'
import { onMounted } from 'vue'
import axios from 'axios'
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useRouter } from 'vue-router'
const route = useRoute()
const router = useRouter()

const surveyId = route.query.id

const survey = new Model({
  locale: 'es',
  logoPosition: 'right',
  pages: [
    {
      name: 'page1',
      elements: [
        {
          type: 'multipletext',
          name: 'clientData',
          title: 'Datos del cliente(*)',
          description: '(*) La empresa puede reservarse el derecho de contestar de forma anonima',
          items: [
            {
              name: 'nombreCliente',
              title: 'Nombre de su empresa',
            },
            {
              name: 'Seccion',
              title: {
                es: 'Sección/División/ Departamento',
              },
            },
            {
              name: 'fecha',
              inputType: 'date',
              title: 'Fecha',
            },
          ],
        },
        {
          type: 'comment',
          name: 'como_conocio_cidepint',
          title: 'Como tomo conociemiento sobre el CIDEPINT?',
          isRequired: true,
        },
        {
          type: 'rating',
          name: 'calificacion_general',
          title: 'Calificacion general',
          isRequired: true,
          rateType: 'stars',
          minRateDescription: 'Malo',
          maxRateDescription: 'Excelente',
        },
        {
          type: 'matrix',
          name: 'temas',
          title: 'Temas',
          isRequired: true,
          columns: [
            {
              value: 'excelente',
              text: 'Excelente',
            },
            {
              value: 'muy_bueno',
              text: 'Muy Bueno',
            },
            {
              value: 'bueno',
              text: 'Bueno',
            },
            {
              value: 'regular',
              text: 'Regular',
            },
            {
              value: 'malo',
              text: 'Malo',
            },
          ],
          rows: [
            {
              value: 'atencion_admin',
              text: 'Atención administrativa',
            },
            {
              value: 'servicio_ofrecido',
              text: 'Servicio ofrecido por el Laboratorio',
            },
            {
              value: 'resultado_ensayo',
              text: 'Resultado del ensayo solicitado',
            },
            {
              value: 'asesoramiento',
              text: 'Asesoramiento brindado',
            },
            {
              value: 'cumplimiento',
              text: 'Cumplimiento de plazos',
            },
            {
              value: 'precio_servicio',
              text: 'Precio del servicio',
            },
            {
              value: 'sistema_de_pago',
              text: 'Sistema de pago',
            },
          ],
          isAllRowRequired: true,
        },
        {
          type: 'comment',
          name: 'otros',
          title: 'Otros aspectos que considere de relevancia',
        },
      ],
    },
  ],
  cookieName: surveyId,
})

var errorMessage = ref('')
var surveyCompleted = ref(false)

survey.onComplete.add(function (sender, options) {
  // Display the "Saving..." message (pass a string value to display a custom message)
  options.showSaveInProgress();
  const xhr = new XMLHttpRequest();
  xhr.open("POST", `${import.meta.env.VITE_API_URL}/api/encuestas/complete?id=${surveyId}`);
  xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
  xhr.onload = xhr.onerror = function () {
    if (xhr.status == 200) {
      // Display the "Success" message (pass a string value to display a custom message)
      options.showSaveSuccess();
      // Alternatively, you can clear all messages:
      // options.clearSaveMessages();
    } else {
      // Display the "Error" message (pass a string value to display a custom message)
      options.showSaveError();
    }
  };
  xhr.send(JSON.stringify(sender.data));
});

onMounted(() => {

  if (!surveyId) {
    router.push('/notFound')
    return
  }

  // Validar el enlace con el backend
  axios
    .get(`${import.meta.env.VITE_API_URL}/api/encuestas/?id=${surveyId}`)
    .then((response) => {
      if (response.data.completed) {
        surveyCompleted.value = true
      } else {
        this.initializeSurvey()
      }
    })
    .catch((e) => {
      if (e.status === 404) {
        router.push('/notFound')
        return
      }
      errorMessage.value = 'El enlace no es válido o ya ha sido usado.'
    })
})
</script>

<template>
  <SurveyComponent v-if="!surveyCompleted" :survey="survey" />
  <div v-else class="d-flex justify-content-center align-items-center p-3 mb-2 bg-secondary-subtle">
    <h1 calss="text-center">Gracias por completar la encuesta.</h1>
  </div>
</template>
