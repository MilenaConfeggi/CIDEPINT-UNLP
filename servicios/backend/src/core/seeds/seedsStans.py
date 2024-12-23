from models.presupuestos.STAN import STAN
from models.base import db
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from servicios.backend.src.core.services.servicioPresupuesto import crear_stan, crear_ensayo, crear_ensayo_stan
def seeds_stans():
    seed_stan()
    seed_ensayos()
    seed_ensayos_stans()

def seed_stan():
    stan_data = [
        {
            'numero': '582',
            'precio_dolares': 31,
            "precio_por_muestra": True,
            
        },
        {
            'numero': '583',
            'precio_dolares': 33,
            "precio_por_muestra": True,
        },
        {
            'numero': '878',
            'precio_dolares': 13,
            "precio_por_muestra": True,
        },
        {
            'numero': '592',
            'precio_dolares': 17,
            "precio_por_muestra": True,
        },
        {
            'numero': '593',
            'precio_dolares': 25,
            "precio_por_muestra": True,
        },
        {
            'numero': '575',
            'precio_dolares': 20,
            "precio_por_muestra": True,
        },
        {
            'numero': '577',
            'precio_dolares': 20,
            "precio_por_muestra": True,
        },
        {
            'numero': '6891',
            'precio_dolares': 44,
            "precio_por_muestra": True,
        },
        {
            'numero': '875',
            'precio_dolares': 19,
            "precio_por_muestra": True,
        },
        {
            'numero': '573',
            'precio_dolares': 14,
            "precio_por_muestra": True,
        },
        {
            'numero': '838',
            'precio_dolares': 20,
            "precio_por_muestra": True,
        },
        {
            'numero': '881',
            'precio_dolares': 20,
            "precio_por_muestra": True,
        },
        {
            'numero': '611',
            'precio_dolares': 14,
            "precio_por_muestra": True,
        },
        {
            'numero': '873',
            'precio_dolares': 18,
            "precio_por_muestra": True,
        },
        {
            'numero': '594',
            "precio_por_muestra": True,
        },
        {
            'numero': '603',
            'precio_dolares': 16,
            "precio_por_muestra": True,
        },
        {
            'numero': '604',
            'precio_dolares': 16,
            "precio_por_muestra": True,
        },
        {
            'numero': '4765',
            'precio_dolares': 20,
            "precio_por_muestra": True,
        },
        {
            'numero': '574',
            'precio_dolares': 13,
            "precio_por_muestra": True,
        },
        {
            'numero': '580',
            'precio_dolares': 14,
            "precio_por_muestra": True,
        },
        {
            'numero': '608',
            'precio_dolares': 16,
            "precio_por_muestra": True,
        },
        {
            'numero': '596',
            'precio_dolares': 12,
            "precio_por_muestra": True,
        },
        {
            'numero': '876',
            'precio_dolares': 12,
            "precio_por_muestra": True,
        },
        {
            'numero': '4671',
            "precio_por_muestra": True,
        },
        {
            'numero': '4668',
            'precio_dolares': 30,
            "precio_por_muestra": True,
        },
        {
            'numero': '4624',
            "precio_por_muestra": True,
        },
        {
            'numero': '4862',
            "precio_por_muestra": True,
        },
        {
            'numero': '1140',
            "precio_por_muestra": True,
        },
        {
            'numero': '571',
            'precio_dolares': 0.5,
            "precio_por_muestra": False,
        },
        {
            'numero': '570',
            'precio_dolares': 0.3,
            "precio_por_muestra": False,
        },
        {
            'numero': '569',
            'precio_dolares': 4,
            "precio_por_muestra": False,
        },
        {
            'numero': '4692',
            'precio_dolares': 0.5,
            "precio_por_muestra": False,
        },
        {
            'numero': '572',
            'precio_dolares': 2,
            "precio_por_muestra": False,
        },
        {
            'numero': '4670',
            'precio_dolares': 2,
            "precio_por_muestra": False,
        },
        {
            'numero': '1142',
            "precio_por_muestra": True,
        },
        {
            'numero': '607',
            'precio_dolares': 12,
            "precio_por_muestra": True,
        },
        {
            'numero': '605',
            "precio_por_muestra": True,
        },
        {
            'numero': '877',
            'precio_dolares': 17,
            "precio_por_muestra": True,
        },
        {
            'numero': '859',
            'precio_dolares': 30,
            "precio_por_muestra": True,
        },
        {
            'numero': '4713',
            'precio_dolares': 14,
            "precio_por_muestra": True,
        },
        {
            'numero': '4629',
            "precio_por_muestra": True,
        },
        {
            'numero': '4596',
            'precio_dolares': 17,
            "precio_por_muestra": True,
        },
        {
            'numero': '4768',
            "precio_por_muestra": False,
        },
        {
            'numero': '4672',
            'precio_dolares': 19,
            "precio_por_muestra": True,
        },
        {
            'numero': '4769',
            "precio_por_muestra": True,
        },
        {
            'numero': '613',
            'precio_dolares': 85,
            "precio_por_muestra": True,
        },
        {
            'numero': '4673',
            "precio_por_muestra": True,
        },
        {
            'numero': '6526',
            'precio_dolares': 100,
            "precio_por_muestra": True,
        },
        {
            'numero': '6527',
            'precio_dolares': 100,
            "precio_por_muestra": True,
        },
        {
            'numero': '6633',
            'precio_dolares': 12000,
            "precio_por_muestra": True,
        },
        {
            'numero': '4717',
            'precio_dolares': 29,
            "precio_por_muestra": True,
        },
        {
            'numero': '6694',
            'precio_dolares': 0.2,
            "precio_por_muestra": True,
        },
        {
            'numero': '616',
            'precio_dolares': 12,
            "precio_por_muestra": True,
        },
        {
            'numero': '590',
            'precio_dolares': 23,
            "precio_por_muestra": True,
        },
        {
            'numero': '589',
            'precio_dolares': 23,
            "precio_por_muestra": True,
        },
        {
            'numero': '880',
            'precio_dolares': 20,
            "precio_por_muestra": True,
        },
        {
            'numero': '595',
            "precio_por_muestra": True,
        },
        {
            'numero': '591',
            'precio_dolares': 37,
            "precio_por_muestra": True,
        },
        {
            'numero': '4677',
            "precio_por_muestra": True,
        },
        {
            'numero': '4883',
            "precio_por_muestra": False,
        },
        {
            'numero': '4863',
            "precio_por_muestra": False,
        },
        {
            'numero': '606',
            'precio_dolares': 18,
            "precio_por_muestra": True,
        },
        {
            'numero': '610',
            'precio_dolares': 25,
            "precio_por_muestra": True,
        },
        {
            'numero': '897',
            "precio_por_muestra": True,
        },
        {
            'numero': '884',
            'precio_dolares': 11,
            "precio_por_muestra": True,
        },
        {
            'numero': '831',
            'precio_dolares': 16,
            "precio_por_muestra": True,
        },
        {
            'numero': '832',
            'precio_dolares': 30,
            "precio_por_muestra": True,
        },
        {
            'numero': '576',
            'precio_dolares': 21,
            "precio_por_muestra": True,
        },
        {
            'numero': '599',
            'precio_dolares': 20,
            "precio_por_muestra": True,
        },
        {
            'numero': '4620',
            'precio_dolares': 22,
            "precio_por_muestra": True,
        },
        {
            'numero': '879',
            'precio_dolares': 21,
            "precio_por_muestra": True,
        },
        {
            'numero': '4864',
            "precio_por_muestra": True,
        },
        {
            'numero': '856',
            'precio_dolares': 25,
            "precio_por_muestra": True,
        },
        {
            'numero': '581',
            'precio_dolares': 58,
            "precio_por_muestra": True,
        },
        {
            'numero': '874',
            'precio_dolares': 17,
            "precio_por_muestra": True,
        },
        {
            'numero': '588',
            'precio_dolares': 14,
            "precio_por_muestra": True,
        },
        {
            'numero': '855',
            'precio_dolares': 28,
            "precio_por_muestra": True,
        },
        {
            'numero': '586',
            'precio_dolares': 14,
            "precio_por_muestra": True,
        },
        {
            'numero': '587',
            'precio_dolares': 15,
            "precio_por_muestra": True,
        },
        {
            'numero': '836',
            "precio_por_muestra": True,
        },
        {
            'numero': '868',
            'precio_dolares': 30,
            "precio_por_muestra": True,
        },
        {
            'numero': '602',
            'precio_dolares': 19,
            "precio_por_muestra": True,
        },
        {
            'numero': '834',
            'precio_dolares': 28,
            "precio_por_muestra": True,
        },
        {
            'numero': '4678',
            'precio_dolares': 30,
            "precio_por_muestra": True,
        },
        {
            'numero': '4693',
            'precio_dolares': 66,
            "precio_por_muestra": True,
        },
        {
            'numero': '4679',
            "precio_por_muestra": True,
        },
        {
            'numero': '601',
            "precio_por_muestra": True,
        },
        {
            'numero': '585',
            "precio_por_muestra": True,
        },
        {
            'numero': '615',
            'precio_dolares': 16,
            "precio_por_muestra": True,
        },
        {
            'numero': '4676',
            'precio_dolares': 26,
            "precio_por_muestra": True,
        },
        {
            'numero': '4675',
            'precio_dolares': 26,
            "precio_por_muestra": True,
        },
        {
            'numero': '871',
            'precio_dolares': 16,
            "precio_por_muestra": True,
        },
        {
            'numero': '4680',
            'precio_dolares': 51,
            "precio_por_muestra": True,
        },
        {
            'numero': '4681',
            "precio_por_muestra": True,
        },
        {
            'numero': '866',
            "precio_por_muestra": True,
        },
        {
            'numero': '579',
            'precio_pesos': 23900,
            'precio_dolares': 26,
            "precio_por_muestra": True,
        },
        {
            'numero': '858',
            'precio_dolares': 18,
            "precio_por_muestra": True,
        },
        {
            'numero': '612',
            'precio_pesos': 25100,
            'precio_dolares': 28,
            "precio_por_muestra": True,
        },
        {
            'numero': '5068',
            "precio_por_muestra": True,
        },
        {
            'numero': '5550',
            'precio_dolares': 15000,
            "precio_por_muestra": True,
        },

    ]

    for data in stan_data:
        crear_stan(data)

def seed_ensayos():
    ensayos_data = [
        #STAN 582
        {
            'nombre': ' abrasión húmeda'
        },
        {
            'nombre': 'lavabilidad'
        },
        {
            'nombre': 'resistencia al incremento del brillo'
        },
        #STAN 583
        {
            'nombre': 'Abrasión Taber'
        },
        {
            'nombre': 'resistencia al desgaste'
        },
        #STAN 878
        {
            'nombre': 'absorción de agua'
        },
        {
            'nombre': 'absorción capilar de agua'
        },
        #STAN 592
        {
            'nombre': 'adhesión por técnica al corte'
        },
        #STAN 593
        {
            'nombre': 'adhesión por tracción'
        },
        #STAN 575
        {
            'nombre': 'aplicabilidad'
        },
        #STAN 577
        {
            'nombre': 'brillo'
        },
        #STAN 6891
        {
            'nombre': 'caracterización básica de pinturas mediante ensayos normalizados'
        },
        #STAN 875
        {
            'nombre': 'carga de despegue y pérdida de cohesión'
        },
        #STAN 573
        {
            'nombre': 'color (observación visual)'
        },
        #STAN 838
        {
            'nombre': 'color sistema CIELAB '
        },
        {
            'nombre': 'luminancia'
        },
        #STAN 881
        {
            'nombre': 'Contenido de material ligante (vehículo)'
        },
        {
            'nombre': 'esferas incorporadas'
        },
        #STAN 611
        {
            'nombre': 'densidad'
        },
        {
            'nombre': 'ph'
        },
        {
            'nombre': 'peso específico'
        },
        #STAN 873
        {
            'nombre': 'deslizamiento por calentamiento a 60°C'
        },
        {
            'nombre': 'aplastamiento'
        },
        {
            'nombre': 'fluidez'
        },
        #STAN 594
        {
            'nombre': 'determinación de dureza con aparatos de tipo péndulo'
        },
        #STAN 603
        {
            'nombre': 'determinación de esferas no defectuosas para incorporar'
        },
        #STAN 604
        {
            'nombre': 'determinación de esferas no defectuosas para sembrar'
        },
        #STAN 4765
        {
            'nombre': 'determinación de la masa de esferas de vidrio presentes en un recubrimiento termoplástico'
        },
        #STAN 574
        {
            'nombre': 'dilución'
        },
        #STAN 580
        {
            'nombre': 'doblado'
        },
        {
            'nombre': 'flexibilidad'
        },
        {
            'nombre': 'elasticidad'
        },
        #STAN 608
        {
            'nombre': 'dureza al lápiz'
        },
        #STAN 596
        {
            'nombre': 'dureza Buchholz'
        },
        #STAN 876
        {
            'nombre': 'dureza Shore A'
        },
        #STAN 4671
        {
            'nombre': 'dureza Sward Rocker'
        },
        #STAN 4668
        {
            'nombre': 'ensayo de doblado de pinturas de demarcación vial a diferentes temperaturas'
        },
        #STAN 4624
        {
            'nombre': 'ensayo de penetración'
        },
        #STAN 4862
        {
            'nombre': 'ensayo de prohesión en cámara Q-FOG '
        },
        #STAN 1140
        {
            'nombre': 'ensayos de control de calidad de pinturas en laboratorio para calificación según especificaciones CIDEPINT-YPF'
        },
        #STAN 571
        {
            'nombre': 'envejecimiento acelerado en ambiente corrosivo, NIEBLA SALINA'
        },
        #STAN 570
        {
            'nombre': 'envejecimiento acelerado en CÁMARA 100% HUMEDAD RELATIVA'
        },
        #STAN 569
        {
            'nombre': 'envejecimiento acelerado en CÁMARA DE ARCO DE XENON'
        },
        #STAN 4692
        {
            'nombre': 'envejecimiento acelerado en CÁMARA DE HUMEDAD QCT'
        },
        #STAN 572
        {
            'nombre': 'envejecimiento acelerado en CÁMARA DE UV, tubos UVA '
        },
        #STAN 4670
        {
            'nombre': 'envejecimiento acelerado en CÁMARA DE UV, tubos UVB'
        },
        #STAN 1142
        {
            'nombre': 'especificación'
        },
        #STAN 607
        {
            'nombre': 'espesor de película seca'
        },
        #STAN 605
        {
            'nombre': 'espesor sin producir chorreo'
        },
        #STAN 877
        {
            'nombre': 'estabilidad, color y aspecto de material termoplástico'
        },
        #STAN 859
        {
            'nombre': 'estabilidad en el envase'
        },
        #STAN 4713
        {
            'nombre': 'evaluación de la estabilidad en el envase de una pintura de demarcación vial'
        },
        #STAN 4629
        {
            'nombre': 'evaluación de la pérdida de peso por ataque químico con solución de ácido clorhídrico'
        },
        #STAN 4596
        {
            'nombre': 'evaluación de la presencia de tratamiento de hidrofugación en microesferas de vidrio'
        },
        #STAN 4768
        {
            'nombre': 'evaluación de la resistencia de la película de pintura a la inmersión en agua caliente'
        },
        #STAN 4672
        {
            'nombre': 'evaluación de la resistencia de la película de pintura a la inmersión en diversas sustancias'
        },
        #STAN 4769
        {
            'nombre': 'evaluación de la resistencia de la película de pintura a la inmersión en un medio específico y a temperatura definida'
        },
        #STAN 613
        {
            'nombre': 'evaluación de oxodegradación de polietileno'
        },
        #STAN 4673
        {
            'nombre': 'evaluación del comportamiento al doblado de probeta pintada tratada térmicamente'
        },
        #STAN 6526
        {
            'nombre': 'evaluación del desempeño de recubrimientos para pizarras blancas de base MDF'
        },
        #STAN 6527
        {
            'nombre': 'evaluación del desempeño de un recubrimiento epoxi para protección anticorrosiva de hornos del proceso de la industria del petróleo y gas'
        },
        #STAN 6633
        {
            'nombre': 'evaluación del desempeño de recubrimientos automotrices según norma B72_0200'
        },
        #STAN 4717
        {
            'nombre': 'evaluación del poder cubritivo de pinturas de demarcación vial por medición de color'
        },
        #STAN 6694
        {
            'nombre': 'foto'
        },
        #STAN 616
        {
            'nombre': 'grado de dispersión'
        },
        {
            'nombre': 'molienda'
        },
        #STAN 590
        {
            'nombre': 'granulometría de esferas para incorporar'
        },
        #STAN 589
        {
            'nombre': 'granulometría de esferas para sembrado'
        },
        #STAN 880
        {
            'nombre': 'granulometría del material libre de ligante'
        },
        #STAN 595
        {
            'nombre': 'homogeneidad'
        },
        #STAN 591
        {
            'nombre': 'índice de refracción'
        },
        #STAN 4677
        {
            'nombre': 'inspección de obra para evaluación del estado de estructuras edilicias/industriales'
        },
        #STAN 4883
        {
            'nombre': 'intemperismo natural (Terraza) con spray, incluye arrugado, ampollado, cuarteado, agrietado, desprendimiento de película, tizado y cambios de color y brillo visuales'
        },
        #STAN 4863
        {
            'nombre': 'intemperismo natural (Terraza), incluye arrugado, ampollado, cuarteado, agrietado, desprendimiento de película, tizado y cambios de color y brillo visuales'
        },
        #STAN 606
        {
            'nombre': 'materias no volátiles en peso'
        },
        #STAN 610
        {
            'nombre': 'materias no volátiles en volumen'
        },
        #STAN 897
        {
            'nombre': 'método de determinación de espesores por corte en cuña (PIG) y medida óptica'
        },
        #STAN 884
        {
            'nombre': 'olor'
        },
        #STAN 831
        {
            'nombre': 'permeabilidad al agua'
        },
        {
            'nombre': 'tensión superficial Dunoi'
        },
        #STAN 832
        {
            'nombre': 'permeabilidad al vapor de agua'
        },
        #STAN 576
        {
            'nombre': 'poder cubritivo'
        },
        #STAN 599
        {
            'nombre': 'porosidad Holiday'
        },
        #STAN 4620
        {
            'nombre': 'preparación y pintado de probetas'
        },
        #STAN 879
        {
            'nombre': 'punto de ablandamiento'
        },
        {
            'nombre': 'resistencia a la temperatura'
        },
        #STAN 4864
        {
            'nombre': 'rayado'
        },
        #STAN 856
        {
            'nombre': 'residuo sobre tamiz'
        },
        #STAN 581
        {
            'nombre': 'resistencia a la abrasión tubular'
        },
        #STAN 874
        {
            'nombre': 'resistencia a la baja temperatura'
        },
        #STAN 588
        {
            'nombre': 'resistencia a la inmersión en aceite'
        },
        #STAN 855
        {
            'nombre': 'resistencia a la inmersión en aceite con temperatura'
        },
        #STAN 586
        {
            'nombre': 'resistencia a la inmersión en agua'
        },
        {
            'nombre': 'agua destilada'
        },
        #STAN 587
        {
            'nombre': 'resistencia a la inmersión en gasoil'
        },
        #STAN 836
        {
            'nombre': 'resistencia a la tracción y alargamiento de rotura'
        },
        #STAN 868
        {
            'nombre': 'resistencia al amarillamiento y oscurecimiento'
        },
        #STAN 602
        {
            'nombre': 'resistencia al calor (mufla)'
        },
        #STAN 834
        {
            'nombre': 'resistencia al impacto'
        },
        #STAN 4678
        {
            'nombre': 'resistencia de pinturas de demarcación vial en contacto con diferentes productos'
        },
        #STAN 4693
        {
            'nombre': 'resistencia de una pintura de demarcación vial al manchado por asfalto'
        },
        #STAN 4679
        {
            'nombre': 'retención de partículas gruesas sobre tamiz'
        },
        #STAN 601
        {
            'nombre': 'rugosidad superficial'
        },
        #STAN 585
        {
            'nombre': 'sangrado'
        },
        #STAN 615
        {
            'nombre': 'tiempo de secado'
        },
        #STAN 4676
        {
            'nombre': 'tiempo de secado “No pick-up time”'
        },
        #STAN 4675
        {
            'nombre': 'tiempo de secado “No pick-up time” a dilución máxima'
        },
        #STAN 871
        {
            'nombre': 'uniformidad y asentamiento'
        },
        #STAN 4680
        {
            'nombre': 'variación de la viscosidad y sedimentación de una pintura de demarcación vial luego de someterla a envejecimiento forzado'
        },
        #STAN 4681
        {
            'nombre': 'verificación de las dimensiones de las tachas plásticas utilizadas en señalización vial'
        },
        #STAN 866
        {
            'nombre': 'vida útil'
        },
        #STAN 579
        {
            'nombre': 'viscosidad Brookfield'
        },
        #STAN 858
        {
            'nombre': 'viscosidad IRAM o Ford'
        },
        #STAN 612
        {
            'nombre': 'viscosidad Stormer'
        },
        #STAN 5068
        {
            'nombre': 'evaluación de desempeño de recubrimientos especiales'
        },
        #STAN 5550
        {
            'nombre': 'evaluación y/o diagnóstico del deterioro de recubrimientos'
        },

    ]

    for data in ensayos_data:
        crear_ensayo(data['nombre'])

def seed_ensayos_stans():
    ensayos_stans_data = [
        # STAN 582
        {'ensayo_id': 1, 'stan_id': 1},
        {'ensayo_id': 2, 'stan_id': 1},
        {'ensayo_id': 3, 'stan_id': 1},
        # STAN 583
        {'ensayo_id': 4, 'stan_id': 2},
        {'ensayo_id': 5, 'stan_id': 2},
        # STAN 878
        {'ensayo_id': 6, 'stan_id': 3},
        {'ensayo_id': 7, 'stan_id': 3},
        # STAN 592
        {'ensayo_id': 8, 'stan_id': 4},
        # STAN 593
        {'ensayo_id': 9, 'stan_id': 5},
        # STAN 575
        {'ensayo_id': 10, 'stan_id': 6},
        # STAN 577
        {'ensayo_id': 11, 'stan_id': 7},
        # STAN 6891
        {'ensayo_id': 12, 'stan_id': 8},
        # STAN 875
        {'ensayo_id': 13, 'stan_id': 9},
        # STAN 573
        {'ensayo_id': 14, 'stan_id': 10},
        # STAN 838
        {'ensayo_id': 15, 'stan_id': 11},
        {'ensayo_id': 16, 'stan_id': 11},
        # STAN 881
        {'ensayo_id': 17, 'stan_id': 12},
        {'ensayo_id': 18, 'stan_id': 12},
        # STAN 611
        {'ensayo_id': 19, 'stan_id': 13},
        {'ensayo_id': 20, 'stan_id': 13},
        {'ensayo_id': 21, 'stan_id': 13},
        # STAN 873
        {'ensayo_id': 22, 'stan_id': 14},
        {'ensayo_id': 23, 'stan_id': 14},
        {'ensayo_id': 24, 'stan_id': 14},
        # STAN 594
        {'ensayo_id': 25, 'stan_id': 15},
        # STAN 603
        {'ensayo_id': 26, 'stan_id': 16},
        # STAN 604
        {'ensayo_id': 27, 'stan_id': 17},
        # STAN 4765
        {'ensayo_id': 28, 'stan_id': 18},
        # STAN 574
        {'ensayo_id': 29, 'stan_id': 19},
        # STAN 580
        {'ensayo_id': 30, 'stan_id': 20},
        {'ensayo_id': 31, 'stan_id': 20},
        {'ensayo_id': 32, 'stan_id': 20},
        # STAN 608
        {'ensayo_id': 33, 'stan_id': 21},
        # STAN 596
        {'ensayo_id': 34, 'stan_id': 22},
        # STAN 876
        {'ensayo_id': 35, 'stan_id': 23},
        # STAN 4671
        {'ensayo_id': 36, 'stan_id': 24},
        # STAN 4668
        {'ensayo_id': 37, 'stan_id': 25},
        # STAN 4624
        {'ensayo_id': 38, 'stan_id': 26},
        # STAN 4862
        {'ensayo_id': 39, 'stan_id': 27},
        # STAN 1140
        {'ensayo_id': 40, 'stan_id': 28},
        # STAN 571
        {'ensayo_id': 41, 'stan_id': 29},
        # STAN 570
        {'ensayo_id': 42, 'stan_id': 30},
        # STAN 569
        {'ensayo_id': 43, 'stan_id': 31},
        # STAN 4692
        {'ensayo_id': 44, 'stan_id': 32},
        # STAN 572
        {'ensayo_id': 45, 'stan_id': 33},
        # STAN 4670
        {'ensayo_id': 46, 'stan_id': 34},
        # STAN 1142
        {'ensayo_id': 47, 'stan_id': 35},
        # STAN 607
        {'ensayo_id': 48, 'stan_id': 36},
        # STAN 605
        {'ensayo_id': 49, 'stan_id': 37},
        # STAN 877
        {'ensayo_id': 50, 'stan_id': 38},
        # STAN 859
        {'ensayo_id': 51, 'stan_id': 39},
        # STAN 4713
        {'ensayo_id': 52, 'stan_id': 40},
        # STAN 4629
        {'ensayo_id': 53, 'stan_id': 41},
        # STAN 4596
        {'ensayo_id': 54, 'stan_id': 42},
        # STAN 4768
        {'ensayo_id': 55, 'stan_id': 43},
        # STAN 4672
        {'ensayo_id': 56, 'stan_id': 44},
        # STAN 4769
        {'ensayo_id': 57, 'stan_id': 45},
        # STAN 613
        {'ensayo_id': 58, 'stan_id': 46},
        # STAN 4673
        {'ensayo_id': 59, 'stan_id': 47},
        # STAN 6526
        {'ensayo_id': 60, 'stan_id': 48},
        # STAN 6527
        {'ensayo_id': 61, 'stan_id': 49},
        # STAN 6633
        {'ensayo_id': 62, 'stan_id': 50},
        # STAN 4717
        {'ensayo_id': 63, 'stan_id': 51},
        # STAN 6694
        {'ensayo_id': 64, 'stan_id': 52},
        # STAN 616
        {'ensayo_id': 65, 'stan_id': 53},
        {'ensayo_id': 66, 'stan_id': 53},
        # STAN 590
        {'ensayo_id': 67, 'stan_id': 54},
        # STAN 589
        {'ensayo_id': 68, 'stan_id': 55},
        # STAN 880
        {'ensayo_id': 69, 'stan_id': 56},
        # STAN 595
        {'ensayo_id': 70, 'stan_id': 57},
        # STAN 591
        {'ensayo_id': 71, 'stan_id': 58},
        # STAN 4677
        {'ensayo_id': 72, 'stan_id': 59},
        # STAN 4883
        {'ensayo_id': 73, 'stan_id': 60},
        # STAN 4863
        {'ensayo_id': 74, 'stan_id': 61},
        # STAN 606
        {'ensayo_id': 75, 'stan_id': 62},
        # STAN 610
        {'ensayo_id': 76, 'stan_id': 63},
        # STAN 897
        {'ensayo_id': 77, 'stan_id': 64},
        # STAN 884
        {'ensayo_id': 78, 'stan_id': 65},
        # STAN 831
        {'ensayo_id': 79, 'stan_id': 66},
        {'ensayo_id': 80, 'stan_id': 66},
        # STAN 832
        {'ensayo_id': 81, 'stan_id': 67},
        # STAN 576
        {'ensayo_id': 82, 'stan_id': 68},
        # STAN 599
        {'ensayo_id': 83, 'stan_id': 69},
        # STAN 4620
        {'ensayo_id': 84, 'stan_id': 70},
        # STAN 879
        {'ensayo_id': 85, 'stan_id': 71},
        {'ensayo_id': 86, 'stan_id': 71},
        # STAN 4864
        {'ensayo_id': 87, 'stan_id': 72},
        # STAN 856
        {'ensayo_id': 88, 'stan_id': 73},
        # STAN 581
        {'ensayo_id': 89, 'stan_id': 74},
        # STAN 874
        {'ensayo_id': 90, 'stan_id': 75},
        # STAN 588
        {'ensayo_id': 91, 'stan_id': 76},
        # STAN 855
        {'ensayo_id': 92, 'stan_id': 77},
        # STAN 586
        {'ensayo_id': 93, 'stan_id': 78},
        {'ensayo_id': 94, 'stan_id': 78},
        # STAN 587
        {'ensayo_id': 95, 'stan_id': 79},
        # STAN 836
        {'ensayo_id': 96, 'stan_id': 80},
        # STAN 868
        {'ensayo_id': 97, 'stan_id': 81},
        # STAN 602
        {'ensayo_id': 98, 'stan_id': 82},
        # STAN 834
        {'ensayo_id': 99, 'stan_id': 83},
        # STAN 4678
        {'ensayo_id': 100, 'stan_id': 84},
        # STAN 4693
        {'ensayo_id': 101, 'stan_id': 85},
        # STAN 4679
        {'ensayo_id': 102, 'stan_id': 86},
        # STAN 601
        {'ensayo_id': 103, 'stan_id': 87},
        # STAN 585
        {'ensayo_id': 104, 'stan_id': 88},
        # STAN 615
        {'ensayo_id': 105, 'stan_id': 89},
        # STAN 4676
        {'ensayo_id': 106, 'stan_id': 90},
        # STAN 4675
        {'ensayo_id': 107, 'stan_id': 91},
        # STAN 871
        {'ensayo_id': 108, 'stan_id': 92},
        # STAN 4680
        {'ensayo_id': 109, 'stan_id': 93},
        # STAN 4681
        {'ensayo_id': 110, 'stan_id': 94},
        # STAN 866
        {'ensayo_id': 111, 'stan_id': 95},
        # STAN 579
        {'ensayo_id': 112, 'stan_id': 96},
        # STAN 858
        {'ensayo_id': 113, 'stan_id': 97},
        # STAN 612
        {'ensayo_id': 114, 'stan_id': 98},
        # STAN 5068
        {'ensayo_id': 115, 'stan_id': 99},
        # STAN 5550
        {'ensayo_id': 116, 'stan_id': 100},
    ]

    for data in ensayos_stans_data:
        crear_ensayo_stan(data['ensayo_id'], data['stan_id'])