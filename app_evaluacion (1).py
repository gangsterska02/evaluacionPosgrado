"""
Evaluación de Psicología — Versión Streamlit
Convertido desde programa_marzo2026.py (Tkinter)
"""

import streamlit as st
import pandas as pd
import random
import io
import re
from pathlib import Path

# ─────────────────────────────────────────────
# PALETA DE COLORES
# ─────────────────────────────────────────────
BG_PRINCIPAL = "#f0f8ff"   # Blanco Azulado
BG_ACENTO    = "#dbe9f6"   # Azul Claro
FG_TITULO    = "#1e90ff"   # Azul Intenso
BG_BOTON     = "#ff6347"   # Rojo Tomate
FG_TEXTO     = "#333333"   # Gris Oscuro

# ─────────────────────────────────────────────
# BANCO DE PREGUNTAS
# ─────────────────────────────────────────────
PREGUNTAS_BASE = [
    {
        "pregunta": "De los siguientes eventos históricos, elige aquel que fue crítico en la emergencia del conductismo.",
        "opciones": ["Teoría de la evolución de Darwin", "Creación de la cámara de condicionamiento operante", "Segunda guerra mundial", "Derrumbamiento del muro de Berlín"],
        "correcta_text": "Teoría de la evolución de Darwin",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "En 1906 se publicó un libro que estableció los principios básicos de la acción refleja, incluyendo el concepto de sinapsis. ¿Cuál es el título de esa obra?",
        "opciones": ["Los reflejos condicionales de Iván Pávlov", "La acción integrativa del sistema nervioso de Charles Sherrington.", "La conducta de los organismos de B.F. Skinner.", "Principios de Psicología de Keller y Schoenfeld."],
        "correcta_text": "La acción integrativa del sistema nervioso de Charles Sherrington.",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": 'Thomas Hobbes sostenía que "todo lo que existe es materia; todo lo que ocurre es movimiento". ¿Qué postura filosófica representa esta afirmación, la cual anticipa el rechazo conductista de lo mental como sustancia independiente del cuerpo?',
        "opciones": ["Materialismo", "Idealismo subjetivo", "Dualismo interaccionista", "Paralelismo psicofísico"],
        "correcta_text": "Materialismo",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "George Berkeley negó la existencia de la sustancia material y afirmó que la única realidad verdadera es la mente. ¿Qué postura filosófica defendía Berkeley y que es contraria a la del conductismo?",
        "opciones": ["Idealismo subjetivo", "Materialismo", "Dualismo interaccionista", "Realismo ingenuo"],
        "correcta_text": "Idealismo subjetivo",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "Se refiere a la intensidad mínima de un estímulo para que pueda provocar una respuesta",
        "opciones": ["Umbral", "Latencia", "Tasa de respuesta", "Intensidad"],
        "correcta_text": "Umbral",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "Es el estímulo cuya presencia señala que la respuesta no será reforzada",
        "opciones": ["Estímulo delta", "Estímulo discriminativo", "Estímulo condicional", "Estímulo de extinción"],
        "correcta_text": "Estímulo delta",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "En un procedimiento de condicionamiento operante, es el estímulo que señala de manera consistente que una respuesta específica será seguida por una consecuencia reforzante",
        "opciones": ["Estímulo discriminativo", "Estímulo delta", "Estímulo incondicionado", "Reforzador"],
        "correcta_text": "Estímulo discriminativo",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "El siguiente esquema es ejemplo del responder típico de un organismo al estar expuesto a un programa de reforzamiento denominado:",
        "opciones": ["Intervalo fijo", "Reforzamiento operante", "Intervalo variable", "Razón fija"],
        "correcta_text": "Intervalo fijo",
        "imagen_path": "images/grafico_intervalo_fijo.png",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "En un estudio clásico, la respuesta de miedo de un niño fue condicionada ante una rata blanca. Posteriormente, el niño manifestó reacciones similares frente a otros estímulos, como un conejo, un abrigo de piel y una máscara. La figura siguiente presenta la intensidad de la respuesta emocional ante diversos estímulos, ordenados según su grado de semejanza con la rata blanca. ¿Cuál de las siguientes opciones describe con mayor precisión la relación entre las propiedades de los estímulos y el patrón de respuesta observado?",
        "opciones": [
            "La similitud entre los estímulos determina la generalización de la respuesta, produciendo un gradiente decreciente.",
            "La respuesta se mantiene constante, independientemente de las diferencias entre los estímulos.",
            "La ausencia del estímulo aversivo elimina la respuesta de manera uniforme ante todos los estímulos.",
            "La intensidad del estímulo aversivo explica por sí sola la variación en la respuesta.",
        ],
        "correcta_text": "La similitud entre los estímulos determina la generalización de la respuesta, produciendo un gradiente decreciente.",
        "imagen_path": "images/gradiente_generalizacion.png",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "El siguiente esquema es un ejemplo de un procedimiento de condicionamiento clásico denominado:",
        "opciones": ['Condicionamiento "huella"', 'Condicionamiento "para atrás"', 'Condicionamiento "simultáneo"', "Condicionamiento pavloviano"],
        "correcta_text": 'Condicionamiento "huella"',
        "imagen_path": "images/esquema_huella.png",
        "categoria": "Análisis conceptual de fenómenos psicológicos",
    },
    {
        "pregunta": "Es la unidad de análisis en la teoría del condicionamiento operante",
        "opciones": ["Triple relación de contingencia", "estímulo–organismo–respuesta (E–O–R)", "Tasa de respuesta", "Contingencias de reforzamiento"],
        "correcta_text": "Triple relación de contingencia",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": "Una rata es colocada en una cámara de condicionamiento operante. Cuando una luz se enciende, las respuestas de presión de la palanca son seguidas por la entrega de alimento. En ausencia de la luz, las presiones de palanca no producen ninguna consecuencia. El investigador busca analizar el comportamiento de la rata en función de estas condiciones. ¿Cuál de las siguientes opciones delimita correctamente la unidad de análisis pertinente para estudiar el fenómeno descrito?",
        "opciones": [
            "La relación entre la presencia de la luz, la presión de la palanca y la entrega de alimento",
            "La frecuencia total de respuestas de presión de palanca durante la sesión",
            "La presión de la palanca como conducta del organismo",
            "El nivel de privación de alimento de la rata antes del experimento",
        ],
        "correcta_text": "La relación entre la presencia de la luz, la presión de la palanca y la entrega de alimento",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": "En los procedimientos de condicionamiento operante que utilizan laberintos, de las siguientes opciones ¿cuál suele ser una de las principales variables dependientes?",
        "opciones": ["Tiempo de recorrido", "Reforzadores", "Tasa de respuesta", "Programa de reforzamiento"],
        "correcta_text": "Tiempo de recorrido",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": "En un aula escolar, se te solicita registrar la conducta de los alumnos de levantarse de su asiento mientras la profesora imparte la clase. ¿cuál de estos registros consideras más apropiado para registrar la conducta de todos los alumnos?",
        "opciones": ["Registro Pla check", "Registro acumulativo", "Registro anecdótico", "Registro frecuencia"],
        "correcta_text": "Registro Pla check",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": "En un estudio experimental, se entrena a palomas para picar una tecla bajo distintos programas de reforzamiento. El investigador desea analizar cómo cambia la tasa de respuesta a lo largo de la sesión para identificar patrones característicos de cada programa. ¿Cuál de los siguientes registros es más adecuado para obtener datos que permitan satisfacer el objetivo escrito?",
        "opciones": [
            "Registro acumulativo continuo de respuestas",
            "Muestreo por intervalos de tiempo fijo",
            "Registro anecdótico de eventos relevantes",
            "Registro de latencia de la primera respuesta",
        ],
        "correcta_text": "Registro acumulativo continuo de respuestas",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": "Cómo se denomina el procedimiento mediante el cual un organismo aprende una respuesta específica que y que consiste en el reforzamiento diferencial de aproximaciones sucesivas",
        "opciones": ["Moldeamiento", "Modelamiento", "Privación", "Reforzamiento"],
        "correcta_text": "Moldeamiento",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": "Dinsmoor y Lawson (1956) realizaron el siguiente experimento: Objetivo: Evaluar el efecto de la intensidad y el intervalo de tiempo que pospone un choque eléctrico sobre la latencia de la presión del operando de ratas en un programa de escape. Con base en la figura que se te presenta, elige la opción que mejor describa los resultados.",
        "opciones": [
            "A mayor intensidad y mayor tiempo sin choque eléctrico, menor latencia.",
            "A mayor tiempo, mayor latencia.",
            "Tiempo sin respuesta con choque eléctrico.",
            "Mayor tiempo, menor latencia del choque eléctrico.",
        ],
        "correcta_text": "A mayor intensidad y mayor tiempo sin choque eléctrico, menor latencia.",
        "imagen_path": "images/grafico_dinsmoor.png",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": "En el estudio Soares et al. (2025), se evaluó el efecto de la disminución en la magnitud del reforzamiento sobre la variabilidad conductual. En la Figura 4 se presenta el índice de variabilidad de los sujetos bajo diferentes condiciones de magnitud del reforzador. Con base en los datos mostrados en la figura, selecciona la opción que describe correctamente el efecto de la disminución de la magnitud del reforzamiento sobre la variabilidad conductual.",
        "opciones": [
            "La disminución de la magnitud del reforzamiento se asocia con un incremento en la variabilidad conductual.",
            "La variabilidad conductual disminuye conforme se reduce la magnitud del reforzamiento.",
            "La variabilidad conductual se mantiene constante independientemente de la magnitud del reforzamiento.",
            "La variabilidad conductual es mayor únicamente cuando la magnitud del reforzamiento es alta.",
        ],
        "correcta_text": "La disminución de la magnitud del reforzamiento se asocia con un incremento en la variabilidad conductual.",
        "imagen_path": "images/grafica_latencia.png",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": (
            "Briggs y Riccio (2007) estaban interesados en analizar si la extinción de una respuesta se veía afectada "
            "por la amnesia retrograda producida por eventos traumáticos. Para ello hicieron un estudio con seis grupos "
            "de ratas. Un primer grupo, denominado no ext, fue expuesto a situación en la que se condicionó la respuesta "
            "de evitación de ratas a trasladarse de una recámara blanca a otra de color negro en la que recibían descargas "
            "eléctricas. Un segundo grupo (ext) paso por la misma situación, pero tuvo una fase posterior en las que se les "
            "expuso en la sección en la que antes habían recibido choques eléctricos sin que estos se presentarán, es decir "
            "se extinguió su respuesta de evitación. Un tercer grupo (ext/hypo) paso por fase del grupo no ext, y una fase "
            "adicional en la que se les introdujo en agua fría hasta reducir considerablemente su temperatura corporal, y "
            "luego se introdujo de nuevo en la caja de vaivén, y se registró el tiempo que tardaban en introducirse en la "
            "cámara negra. Tres grupos más, denominados 30, 33 y 37 pasaron por las mismas condiciones que el grupo "
            "ext/hypo pero, antes de ser reintroducidas a la caja de vaivén se les permitió llegar a los 30, 33 y 37 "
            "grados centígrados (respectivamente) y posteriormente se registró su comportamiento. Los datos recopilados "
            "se presentan en la siguiente figura, en la que se observa en el eje de las ordenadas el tiempo que tardaban "
            "en trasladarse de la sección blanca a la sección negra. Las barras de la abscisa son cada de uno de los "
            "grupos observados. Con base en los datos, elige aquella opción que represente un hallazgo reportado por los autores."
        ),
        "opciones": [
            "A) La amnesia inducida por hipotermia interfiere con la recuperación de la extinción, y su efecto depende del estado fisiológico (temperatura corporal) en la reexposición.",
            "La extinción elimina permanentemente la memoria del condicionamiento de evitación, independientemente del estado fisiológico del organismo.",
            "La hipotermia incrementa de forma lineal la respuesta de evitación en todos los grupos experimentales sin interacción con la extinción.",
            "El aprendizaje de evitación solo ocurre en ausencia de extinción y no puede recuperarse tras manipulación fisiológica posterior.",
        ],
        "correcta_text": "A) La amnesia inducida por hipotermia interfiere con la recuperación de la extinción, y su efecto depende del estado fisiológico (temperatura corporal) en la reexposición.",
        "imagen_path": "images/briggs.png",
        "categoria": "Análisis metodológico de hechos psicológicos",
    },
    {
        "pregunta": (
            "Antonio es un estudiante de Psicología que, tras haber tenido experiencias previas en las que las ratas de "
            "laboratorio se asociaron con sobresaltos intensos y situaciones desagradables durante prácticas (por ejemplo, "
            "movimientos bruscos de los animales y manipulación inesperada que le generaban una fuerte respuesta de miedo), "
            "desarrolla una reacción de temor al ver o estar cerca de ellas. Esta reacción incluye conductas de evitación "
            "como retirarse del lugar, cerrar los ojos o desviar la mirada. Para ayudarlo, su profesor lo expone de manera "
            "gradual y repetida a la presencia de ratas en un contexto controlado, en el que ahora las ratas no realizan "
            "movimientos bruscos ni ocurren situaciones desagradables. Antonio no puede evitar el estímulo, pero tampoco "
            "ocurre el evento aversivo que antes estaba asociado a las ratas. Con el paso de las sesiones, las respuestas "
            "de miedo de Antonio disminuyen hasta prácticamente desaparecer. ¿Qué principio del aprendizaje explica este "
            "cambio en la conducta de Antonio?"
        ),
        "opciones": ["Extinción", "Evitación condicional", "Generalización", "Reforzamiento"],
        "correcta_text": "Extinción",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            'Adriana es una gerente bancaria de 45 años que hace ocho meses fue diagnosticada con diabetes. A partir del '
            'diagnóstico ha tenido tres crisis de salud asociadas a desajustes en su glucosa en sangre. Cuando Adriana se '
            'encuentra en su rutina diaria y aparece la experiencia de antojo o deseo de consumir bebidas azucaradas, '
            'continúa consumiendo refresco de cola, rechaza la dieta prescrita argumentando que "no le sabe bien" y no toma '
            'el medicamento indicado por el médico. Como resultado inmediato, experimenta sensación de agrado al consumir el '
            'refresco y alimentos que prefiere, y además mantiene la creencia de que su condición puede controlarse sin '
            'medicamentos debido a la experiencia de su madre. Con base en lo anterior, determina cuál es la dimensión '
            'psicológica del caso.'
        ),
        "opciones": [
            "La interacción entre la experiencia de antojo, la respuesta de consumo de refresco y la sensación de agrado inmediata que mantiene la conducta.",
            "Las recomendaciones médicas como antecedentes instruccionales que organizan el cumplimiento o incumplimiento del tratamiento.",
            "C) La experiencia de antojo como evento antecedente que dispara la conducta de consumo.",
            "D) La sensación de agrado inmediata como consecuencia que mantiene la conducta de consumo.",
        ],
        "correcta_text": "La interacción entre la experiencia de antojo, la respuesta de consumo de refresco y la sensación de agrado inmediata que mantiene la conducta.",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            'Luis es un estudiante universitario de 20 años que ha comenzado a reprobar varias materias. Refiere que cuando '
            'intenta estudiar, suele posponer la actividad revisando redes sociales o viendo videos en su celular. Aunque '
            'menciona sentirse preocupado por su desempeño académico, también comenta que "necesita relajarse un poco antes '
            'de empezar", lo que suele prolongarse durante varias horas. Luis reconoce que esta situación le ha generado '
            'conflictos familiares y académicos, pero le resulta difícil iniciar sus actividades escolares. Con base en lo '
            'anterior, determina cuál es la dimensión psicológica sobre la cual debe basarse el análisis psicológico.'
        ),
        "opciones": [
            "conducta de evitación de demandas académicas mantenido por consecuencias de alivio inmediato.",
            "Déficit en habilidades de autorregulación cognitiva asociado a baja planificación.",
            "Sesgo motivacional hacia reforzadores de alta inmediatez frente a metas de largo plazo.",
            "Alteración en la percepción de autoeficacia académica ante tareas evaluativas.",
        ],
        "correcta_text": "conducta de evitación de demandas académicas mantenido por consecuencias de alivio inmediato.",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            "El dueño de una compañía de ventas te contrata para intervenir con un gerente de producto que, aunque cumple "
            "consistentemente con sus objetivos de ventas y desempeño, mantiene conflictos frecuentes con sus subordinados "
            "debido a que utiliza regaños, descalificaciones e insultos como forma habitual de comunicación. El objetivo de "
            "la intervención es reducir la frecuencia de estas conductas verbales aversivas sin afectar su nivel de desempeño "
            "laboral. Al entrevistarte con el gerente, ¿cuál de las siguientes preguntas consideras que te permitiría "
            "identificar la dimensión psicológica del problema?"
        ),
        "opciones": [
            "1. ¿Qué situaciones ocurren en su jornada laboral en las que tiende a reaccionar con regaños o descalificaciones hacia sus subordinados, y qué cambia en su entorno inmediato después de hacerlo?",
            "B) ¿Cómo interpreta usted el desempeño de sus subordinados y qué ideas tiene sobre la manera en que deberían responder a sus instrucciones dentro del equipo de trabajo?",
            "C) ¿Qué aspectos de su formación profesional y experiencia previa considera que han influido en su estilo de comunicación actual con su equipo de trabajo?",
            "D) ¿Qué cambios organizacionales, como metas de ventas o presión por resultados, han modificado la forma en que usted supervisa y evalúa el desempeño de su equipo?",
        ],
        "correcta_text": "1. ¿Qué situaciones ocurren en su jornada laboral en las que tiende a reaccionar con regaños o descalificaciones hacia sus subordinados, y qué cambia en su entorno inmediato después de hacerlo?",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            "Antonio es un niño de ocho años que acude a una escuela pública. Su profesora lo define como un niño "
            "inteligente y amable, pero que constantemente se distrae con sus compañeritos, lo que le impide terminar en "
            "tiempo y forma con las actividades que se le solicitan. Con el propósito de analizar las principales variables "
            "que afectan el termino de sus actividades, elige aquel registro que pueda proporcionar la información más apropiada."
        ),
        "opciones": ["Registro de bloque temporal.", "Registro anecdótico", "Registro pla chek", "Registro acumulativo"],
        "correcta_text": "Registro de bloque temporal.",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            "Carmen es una estudiante de medicina que, en situaciones de nerviosismo, presenta una conducta repetitiva de "
            "rascado en el brazo, la cual le ha ocasionado lesiones visibles en la piel. Ha identificado que esta conducta "
            "ocurre con mayor intensidad durante la temporada de exámenes, particularmente ante la incertidumbre sobre su "
            "desempeño académico. Además, señala que el rascado tiende a ocurrir de manera continua o intermitente a lo "
            "largo de periodos prolongados, lo que dificulta delimitar con claridad el inicio y el final de cada episodio. "
            "Dado este contexto: ¿Qué parámetro de registro conductual sería el más adecuado para evaluar esta conducta y "
            "por qué, considerando las características de ocurrencia descritas?"
        ),
        "opciones": [
            "a) Duración de la conducta, para cuantificar el tiempo total en que Carmen permanece rascándose.",
            "b) Frecuencia de respuestas, para estimar cuántas veces ocurre la conducta en un periodo determinado.",
            "c) Latencia de la respuesta, para identificar el tiempo que tarda en aparecer la conducta tras un estímulo.",
            "d) Intervalos de muestreo, para estimar la ocurrencia de la conducta en periodos previamente definidos.",
        ],
        "correcta_text": "a) Duración de la conducta, para cuantificar el tiempo total en que Carmen permanece rascándose.",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            "En un estudio experimental con 12 estudiantes universitarios con IMC en rango normopeso, se evaluó la "
            "regulación social de la conducta alimentaria mediante un diseño intrasujeto con cuatro fases (A, B, C y A'). "
            "En la fase A los participantes comían solos; en la fase B lo hacían con un modelo que consumía 113 g de "
            "alimentos poco calóricos en 1200 segundos; en la fase C con un modelo que consumía 133 g de alimentos "
            "calóricos en el mismo tiempo; y en la fase A' nuevamente solos. Se registró la cantidad de alimento ingerido, "
            "la frecuencia de elección de alimentos calóricos y la duración del consumo. Los resultados mostraron que la "
            "cantidad ingerida disminuyó en B (Mdn = 119.5 g) respecto a A (131 g) y aumentó en C (145 g), con diferencias "
            "significativas entre fases (χ²(3) = 12.67, p = .005). No hubo diferencias significativas en el tipo de "
            "alimento (p = .470). Los participantes con mayor consumo inicial mostraron mayor ajuste a las condiciones. "
            "Con base en esta información, ¿cuál es el análisis más adecuado de las variables implicadas?"
        ),
        "opciones": [
            "VI: consumo del modelo; VD: cantidad ingerida; moduladora: consumo inicial.",
            "VI: hambre; VD: cantidad ingerida.",
            "VI: tipo de alimento; VD: consumo.",
            "VI: tiempo de sesión; VD: consumo.",
        ],
        "correcta_text": "VI: consumo del modelo; VD: cantidad ingerida; moduladora: consumo inicial.",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            "Armando es un peleador de muay thai que está por disputar un campeonato. En combates previos, cuando su "
            "oponente emite insultos dirigidos a su persona o a su familia, Armando incrementa abruptamente la frecuencia "
            "de ataques desorganizados, descuida la guardia y abandona la estrategia previamente acordada con su equipo, "
            "lo que lo expone a contraataques. Su próximo rival ha comenzado a utilizar sistemáticamente este tipo de "
            "provocaciones, por lo que se espera que estas ocurran durante la pelea. Aunque Armando identifica que estos "
            "estímulos le generan enojo intenso, su principal preocupación es que esta situación interfiera con su "
            "desempeño táctico. Considerando que la intervención debe orientarse a modificar las condiciones asociadas a "
            "la problemática, ¿cuál de los siguientes objetivos es el más adecuado para guiar el diseño del procedimiento?"
        ),
        "opciones": [
            "a) Establecer que, ante la presencia de provocaciones verbales del oponente, Armando mantenga la secuencia táctica entrenada (guardia, distancia y combinación) en la mayoría de los intercambios durante el combate.",
            "b) Entrenar a Armando para reducir la intensidad de su reacción ante los insultos mediante exposición progresiva a situaciones de provocación.",
            "c) Lograr que Armando incremente la consistencia en la ejecución de combinaciones ofensivas durante la pelea.",
            "d) Desarrollar en Armando la capacidad de ignorar los estímulos irrelevantes emitidos por el oponente durante el combate.",
        ],
        "correcta_text": "a) Establecer que, ante la presencia de provocaciones verbales del oponente, Armando mantenga la secuencia táctica entrenada (guardia, distancia y combinación) en la mayoría de los intercambios durante el combate.",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            "Carla trabaja en atención al cliente y reporta altos niveles de estrés laboral. Ante situaciones de presión, "
            "especialmente cuando interactúa con clientes conflictivos, tiende a evitar el contacto directo y delega la "
            "atención a sus compañeros. Esta conducta ha reducido momentáneamente su malestar, pero ha comenzado a generar "
            "problemas en su desempeño laboral y conflictos con su equipo. Para evaluar el progreso de una intervención "
            "dirigida a modificar esta problemática, ¿cuál de los siguientes indicadores es el más adecuado?"
        ),
        "opciones": [
            "a) Número de veces que Carla delega la atención de clientes conflictivos a sus compañeros por turno.",
            "b) Nivel de estrés percibido por Carla al final de la jornada laboral.",
            "c) Grado de satisfacción de Carla con su desempeño laboral.",
            "d) Opinión de sus compañeros sobre la actitud de Carla en el trabajo.",
        ],
        "correcta_text": "a) Número de veces que Carla delega la atención de clientes conflictivos a sus compañeros por turno.",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            "Diego es un estudiante de preparatoria que presenta dificultades para participar en clase. Aunque domina los "
            "contenidos, evita levantar la mano por miedo a equivocarse y ser juzgado por sus compañeros. Como consecuencia, "
            "su participación es baja y esto ha comenzado a afectar su calificación final. Se ha identificado que la conducta "
            "de evitación se mantiene porque reduce momentáneamente el malestar asociado a la evaluación social. Con base en "
            "esta situación, ¿cuál de los siguientes procedimientos es el más adecuado para intervenir el problema?"
        ),
        "opciones": [
            "a) Exponer gradualmente a Diego a situaciones de participación en clase, iniciando con contextos de baja exigencia y aumentando progresivamente la dificultad, reforzando sus intentos de participación.",
            "b) Proporcionar información a Diego sobre la importancia de participar en clase para mejorar su rendimiento académico.",
            "c) Solicitar a los compañeros que eviten emitir juicios negativos cuando Diego participe en clase.",
            "d) Pedir a Diego que intente participar más frecuentemente durante las clases.",
        ],
        "correcta_text": "a) Exponer gradualmente a Diego a situaciones de participación en clase, iniciando con contextos de baja exigencia y aumentando progresivamente la dificultad, reforzando sus intentos de participación.",
        "categoria": "Intervención psicológica de problemas sociales",
    },
    {
        "pregunta": (
            "Imagina que eres un psicólogo que trabaja en el ámbito educativo y recibes una solicitud para intervenir en "
            "la conducta de un niño que se levanta de su lugar de manera frecuente durante la clase. El objetivo es "
            "modificar las condiciones bajo las cuales esta conducta ocurre, de modo que el niño permanezca en su lugar "
            "y sólo se levante cuando la profesora lo indique. Con base en esta situación, ¿cuál es el principio "
            "psicológico más adecuado para orientar la intervención?"
        ),
        "opciones": ["Control de estímulos", "Reforzamiento positivo", "Castigo positivo", "Extinción"],
        "correcta_text": "Control de estímulos",
        "categoria": "Intervención psicológica de problemas sociales",
    },
]

# ─────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
    <style>
        /* Fondo general */
        .stApp {{
            background-color: {BG_PRINCIPAL};
        }}

        /* Títulos principales */
        h1, h2, h3 {{
            color: {FG_TITULO} !important;
        }}

        /* Párrafos y texto general */
        p, label, .stMarkdown {{
            color: {FG_TEXTO};
        }}

        /* Botones principales — Rojo Tomate */
        div.stButton > button {{
            background-color: {BG_BOTON} !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.8rem !important;
            font-size: 1rem !important;
            font-weight: bold !important;
            transition: background-color 0.2s ease;
        }}
        div.stButton > button:hover {{
            background-color: #ff8c73 !important;
            color: white !important;
        }}

        /* Download button — mantener coherencia */
        div.stDownloadButton > button {{
            background-color: {FG_TITULO} !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.8rem !important;
            font-size: 1rem !important;
            font-weight: bold !important;
        }}
        div.stDownloadButton > button:hover {{
            background-color: #4da6ff !important;
            color: white !important;
        }}

        /* Tarjeta / contenedor de pregunta */
        .card {{
            background-color: {BG_ACENTO};
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            border: 1px solid #c5d8ef;
        }}

        /* Radio buttons */
        .stRadio > div {{
            background-color: {BG_ACENTO};
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }}

        /* Inputs */
        .stTextInput > div > input,
        .stNumberInput > div > input {{
            border: 1.5px solid #a0bfd8 !important;
            border-radius: 6px !important;
            background-color: white !important;
        }}

        /* Progress bar */
        .stProgress > div > div > div {{
            background-color: {FG_TITULO} !important;
        }}

        /* Ocultar el menú hamburguesa y footer de Streamlit */
        #MainMenu, footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# INICIALIZACIÓN DE SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        # bienvenida | consentimiento | posgrado | demograficos | autoevaluacion | preguntas | resultados
        "pagina": "bienvenida",
        "data": {},
        "answers": [],
        "questions": [],
        "current_question": 0,
        "correct_answers": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def ir_a(pagina: str):
    st.session_state.pagina = pagina


def _limpiar_prefijo(texto: str) -> str:
    """Elimina prefijos tipo a), A), 1), 1. que algunas opciones ya traen."""
    return re.sub(r"^\s*([0-9]+[.)]\s*|[a-dA-D][.)]\s*)", "", texto).strip()


def preparar_preguntas():
    """Limpia prefijos, baraja opciones y baraja el orden de preguntas."""
    preguntas = []
    for q in PREGUNTAS_BASE:
        item = dict(q)
        opciones_limpias = [_limpiar_prefijo(o) for o in item["opciones"]]
        correct_clean    = _limpiar_prefijo(item["correcta_text"])
        random.shuffle(opciones_limpias)
        item["opciones"]      = opciones_limpias
        item["correcta_text"] = correct_clean
        item["correcta_idx"]  = opciones_limpias.index(correct_clean)
        preguntas.append(item)
    random.shuffle(preguntas)
    return preguntas


def construir_excel() -> bytes:
    """Construye el archivo Excel de resultados y lo devuelve como bytes."""
    result_data = dict(st.session_state.data)
    for idx, ans in enumerate(st.session_state.answers, start=1):
        result_data[f"Pregunta {idx}"] = ans["Pregunta"]
        result_data[f"Respuesta {idx}"] = ans["Respuesta Seleccionada"]
        result_data[f"Correcta {idx}"] = ans["Respuesta Correcta Texto"]
        result_data[f"Resultado {idx}"] = ans["Resultado"]

    df = pd.DataFrame([result_data])
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buf.getvalue()


def construir_csv() -> bytes:
    """Construye el archivo CSV de resultados y lo devuelve como bytes."""
    result_data = dict(st.session_state.data)
    for idx, ans in enumerate(st.session_state.answers, start=1):
        result_data[f"Pregunta {idx}"] = ans["Pregunta"]
        result_data[f"Respuesta {idx}"] = ans["Respuesta Seleccionada"]
        result_data[f"Correcta {idx}"] = ans["Respuesta Correcta Texto"]
        result_data[f"Resultado {idx}"] = ans["Resultado"]

    df = pd.DataFrame([result_data])
    return df.to_csv(index=False).encode("utf-8")


# ─────────────────────────────────────────────
# VISTAS
# ─────────────────────────────────────────────

def vista_bienvenida():
    st.markdown("<h1 style='text-align:center;'>¡Bienvenido/a! 👋</h1>", unsafe_allow_html=True)

    # Logo opcional
    try:
        st.image("images/image.png", width=180)
    except Exception:
        try:
            st.image("image.png", width=180)
        except Exception:
            pass

    st.markdown(f"""
    <div class="card">
        <p style="font-size:1.1rem; text-align:justify; color:{FG_TEXTO};">
            Muchas gracias por tu participación. Nos gustaría que nos ayudaras a contestar algunas
            preguntas sobre tu formación psicológica. Te pedimos que contestes con honestidad,
            sin consultar fuentes externas. Asimismo, si tienes alguna duda, pregunta al investigador
            porque una vez iniciada la evaluación no podrás hacerlo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Entendido ✅"):
            ir_a("consentimiento")
            st.rerun()


def vista_consentimiento():
    st.markdown(
        f"<h1 style='text-align:center; color:{FG_TITULO};'>Consentimiento Informado</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<div style='background:{BG_ACENTO}; border-radius:12px; padding:1.4rem 1.6rem;
        border:1px solid #c5d8ef; margin-bottom:1rem;'>
        <p style='color:{FG_TEXTO}; font-size:1rem; margin-bottom:0.8rem;'>
        Al hacer clic en <b>"Aceptar"</b> e ingresar tu nombre, declaras que comprendes
        y aceptas lo siguiente:</p>
        <ol style='color:{FG_TEXTO}; font-size:1rem; line-height:1.7; padding-left:1.3rem;'>
          <li><b>Sin efecto en tu calificación:</b> Esta evaluación no afectará tu calificación
          en ninguna materia. Los resultados son solo para fines internos del programa.</li>
          <li><b>Confidencialidad:</b> Tus respuestas y tu nombre se mantendrán confidenciales.
          Los datos se analizarán de forma anonimizada y no se compartirán tus datos personales
          con terceros sin tu autorización.</li>
          <li><b>Uso voluntario:</b> Tu participación es completamente voluntaria. Puedes cerrar
          la evaluación en cualquier momento sin ninguna consecuencia.</li>
        </ol>
        </div>""",
        unsafe_allow_html=True,
    )

    with st.form("form_consentimiento"):
        nombre_cons = st.text_input("Escribe tu nombre para aceptar:")
        col1, col2 = st.columns(2)
        with col1:
            aceptar = st.form_submit_button("✅ Aceptar y continuar", use_container_width=True)
        with col2:
            rechazar = st.form_submit_button("❌ No deseo participar", use_container_width=True)

    if aceptar:
        if not nombre_cons.strip():
            st.error("Por favor escribe tu nombre para aceptar el consentimiento.")
        else:
            st.session_state.data["Nombre Consentimiento"] = nombre_cons.strip()
            ir_a("posgrado")
            st.rerun()
    if rechazar:
        st.warning("Gracias por tu tiempo. Puedes cerrar esta pestaña.")
        st.stop()


def vista_posgrado():
    st.markdown(
        f"<h1 style='text-align:center; color:{FG_TITULO};'>Datos de Formación</h1>",
        unsafe_allow_html=True,
    )

    with st.form("form_posgrado_inicial"):
        es_posgrado = st.radio(
            "¿Eres estudiante de posgrado?",
            options=["No", "Sí"],
            horizontal=True,
            index=None,
        )
        siguiente = st.form_submit_button("Siguiente ▶️")

    if siguiente:
        if es_posgrado is None:
            st.error("Por favor selecciona una opción.")
            st.stop()
        if es_posgrado == "No":
            st.session_state.data["Posgrado"] = "No"
            ir_a("demograficos")
            st.rerun()
        else:
            st.session_state.data["Posgrado"] = "Sí"
            ir_a("datos_posgrado")
            st.rerun()


def vista_datos_posgrado():
    st.markdown(
        f"<h1 style='text-align:center; color:{FG_TITULO};'>Datos de Posgrado</h1>",
        unsafe_allow_html=True,
    )

    with st.form("form_datos_posgrado"):
        nivel = st.selectbox(
            "a) Nivel de posgrado:",
            options=["", "Maestría", "Doctorado"],
        )
        semestre_pos = st.text_input("b) Semestre:")
        campo        = st.text_input("c) Campo de conocimiento:")
        sede         = st.text_input("d) Sede en que llevas a cabo el posgrado:")

        # e) Solo aplica si doctorado
        st.markdown(
            f"<p style='color:{FG_TEXTO}; font-size:0.9rem; margin:0.5rem 0 0.2rem;'>"
            "e) Si es doctorado, ¿fue…? (deja en blanco si es maestría)</p>",
            unsafe_allow_html=True,
        )
        tipo_doctorado = st.selectbox(
            "Tipo de ingreso al doctorado:",
            options=["No aplica", "Directo", "Maestría previa"],
            label_visibility="collapsed",
        )

        curso_ingreso = st.radio(
            "f) ¿Tomaste curso para entrar al posgrado?",
            options=["Sí", "No"],
            horizontal=True,
            index=None,
        )
        tiempo_titulacion = st.text_input(
            "g) ¿Cuánto tiempo pasó entre que te titulaste y entraste al posgrado?"
        )
        grupo_inv = st.radio(
            "h) ¿Perteneces a un grupo de investigación?",
            options=["Sí", "No"],
            horizontal=True,
            index=None,
        )
        tiempo_grupo = st.selectbox(
            "i) Si perteneces a un grupo de investigación, ¿cuánto tiempo llevas colaborando?",
            options=[
                "No aplica",
                "Menos de un año",
                "Más de un año",
                "Más de dos años",
                "Más de tres años",
            ],
        )
        da_clases = st.radio(
            "j) ¿Actualmente das clases?",
            options=["Sí", "No"],
            horizontal=True,
            index=None,
        )
        asignatura   = st.text_input("k) Si das clases, ¿de qué asignatura?")
        tiempo_clases = st.text_input(
            "l) Si das clases, ¿cuánto tiempo lo has hecho (en meses)?"
        )

        submitted = st.form_submit_button("Siguiente ▶️")

    if submitted:
        errores = []
        if not nivel:
            errores.append("Selecciona el nivel de posgrado (a).")
        if curso_ingreso is None:
            errores.append("Responde si tomaste curso de ingreso (f).")
        if grupo_inv is None:
            errores.append("Responde si perteneces a un grupo de investigación (h).")
        if da_clases is None:
            errores.append("Responde si actualmente das clases (j).")
        if errores:
            for e in errores:
                st.error(e)
        else:
            st.session_state.data.update({
                "Nivel de posgrado":        nivel,
                "Semestre posgrado":        semestre_pos,
                "Campo de conocimiento":    campo,
                "Sede posgrado":            sede,
                "Tipo ingreso doctorado":   tipo_doctorado,
                "Curso ingreso posgrado":   curso_ingreso,
                "Tiempo entre titulación e ingreso": tiempo_titulacion,
                "Grupo de investigación":   grupo_inv,
                "Tiempo en grupo inv.":     tiempo_grupo,
                "Da clases":                da_clases,
                "Asignatura que imparte":   asignatura,
                "Tiempo dando clases (meses)": tiempo_clases,
            })
            ir_a("demograficos")
            st.rerun()


def vista_demograficos():
    st.markdown(
        f"<h1 style='text-align:center; color:{FG_TITULO};'>Datos Demográficos</h1>",
        unsafe_allow_html=True,
    )
    with st.form("form_demograficos"):
        semestre = st.text_input("Semestre:")
        edad     = st.text_input("Edad:")
        correo   = st.text_input("Correo electrónico:")
        submitted = st.form_submit_button("Siguiente ▶️")
        if submitted:
            st.session_state.data.update({
                "Semestre": semestre,
                "Edad":     edad,
                "Correo":   correo,
            })
            ir_a("autoevaluacion")
            st.rerun()


def vista_autoevaluacion():
    st.markdown("<h1 style='text-align:center;'>Autoevaluación (1-10)</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <p style="color:{FG_TEXTO};">
            Te pedimos que a continuación califiques tus habilidades o conocimientos adquiridos
            sobre la tradición conductual, cognitivo conductual e interconductual del <b>1</b> al <b>10</b>,
            en el que <b>1</b> es muy malos y <b>10</b> es excelente.
        </p>
    </div>
    """, unsafe_allow_html=True)

    secciones  = ["Teórico", "Metodológico", "Aplicado"]
    tradiciones = ["Conductual", "Cognitivo Conductual", "Interconductual"]
    campos = [(f"{s} - {t}") for s in secciones for t in tradiciones]

    with st.form("form_autoevaluacion"):
        valores = {}
        for campo in campos:
            valores[campo] = st.number_input(
                campo,
                min_value=1, max_value=10, step=1, value=5,
                key=f"auto_{campo}"
            )

        submitted = st.form_submit_button("Siguiente ▶️")
        if submitted:
            st.session_state.data.update(valores)
            st.session_state.questions      = preparar_preguntas()
            st.session_state.current_question = 0
            st.session_state.correct_answers  = 0
            st.session_state.answers          = []
            ir_a("preguntas")
            st.rerun()


def vista_preguntas():
    idx   = st.session_state.current_question
    total = len(st.session_state.questions)

    if idx >= total:
        # Guardar resumen y pasar a resultados
        n = total
        c = st.session_state.correct_answers
        st.session_state.data.update({
            "Respuestas Correctas": c,
            "Num Preguntas":        n,
            "Promedio (%)":         f"{(c/n*100):.2f}" if n > 0 else "0.00",
        })
        ir_a("resultados")
        st.rerun()
        return

    q = st.session_state.questions[idx]

    # Barra de progreso
    progreso = idx / total
    st.progress(progreso, text=f"Pregunta {idx + 1} de {total}")

    # ── Categoría ──────────────────────────────────────────────────────────
    categoria = q.get("categoria", "")
    st.markdown(
        f"<p style='color:{FG_TITULO}; font-style:italic; font-size:0.88rem; margin:0 0 4px 0;'>"
        f"📂 {categoria}</p>",
        unsafe_allow_html=True,
    )

    # ── Enunciado: dividido en párrafos, NUNCA truncado por HTML ───────────
    # Se busca el punto justo antes de la pregunta directa para separar en 2 párrafos.
    texto = q["pregunta"]
    # Patrones que suelen marcar el inicio de la pregunta directa
    separadores = [
        "¿Cuál", "¿Qué", "¿Cuá", "Con base en", "Selecciona", "Elige",
        "De acuerdo", "Determina", "Dado este", "Considerando",
    ]
    parrafos = [texto]
    for sep in separadores:
        idx_sep = texto.find(sep)
        if idx_sep > 80:   # sólo separar si el contexto previo es sustancial
            parrafos = [texto[:idx_sep].strip(), texto[idx_sep:].strip()]
            break

    # Renderizar cada párrafo como bloque independiente dentro de una tarjeta
    parrafos_html = "".join(
        f"<p style='color:{FG_TEXTO}; font-size:1.02rem; font-weight:600; "
        f"margin:0 0 0.7rem 0; line-height:1.55;'>{p}</p>"
        for p in parrafos if p
    )
    st.markdown(
        f"<div style='background:{BG_ACENTO}; border-radius:12px; "
        f"padding:1.2rem 1.4rem; border:1px solid #c5d8ef; margin-bottom:0.8rem;'>"
        f"{parrafos_html}</div>",
        unsafe_allow_html=True,
    )

    # ── Imagen (ruta absoluta via pathlib, funciona en Streamlit Cloud) ────
    if "imagen_path" in q:
        nombre_img = q["imagen_path"].replace("images/", "").replace("images\\", "")
        ruta_abs   = Path(__file__).parent / "images" / nombre_img
        if ruta_abs.exists():
            st.image(str(ruta_abs), use_container_width=True)
        else:
            st.warning(
                f"Imagen **{nombre_img}** no encontrada. "
                "Asegúrate de que esté en la carpeta `images/` de tu repositorio."
            )

    # Opciones: numeración limpia 1) 2) 3) 4) — sin doble prefijo
    numeros = ["1)", "2)", "3)", "4)", "5)"]
    opciones_display = [f"{numeros[i]} {opt}" for i, opt in enumerate(q["opciones"])]
    seleccion = st.radio(
        "Selecciona una opción:",
        options=opciones_display,
        key=f"q_{idx}",
        index=None,
    )

    if st.button("Siguiente ▶️"):
        if seleccion is None:
            st.warning("Por favor selecciona una opción antes de continuar.")
        else:
            sel_idx = opciones_display.index(seleccion)        # base-0
            respuesta_texto = q["opciones"][sel_idx]
            es_correcta     = sel_idx == q["correcta_idx"]    # comparación base-0 directa

            st.session_state.answers.append({
                "Pregunta":                q["pregunta"],
                "Respuesta Seleccionada":  respuesta_texto,
                "Respuesta Correcta Texto": q["correcta_text"],
                "Resultado":               "Correcta" if es_correcta else "Incorrecta",
                "Categoria":               q.get("categoria", "N/A"),
            })

            if es_correcta:
                st.session_state.correct_answers += 1

            st.session_state.current_question += 1
            st.rerun()


def vista_resultados():
    n = st.session_state.data.get("Num Preguntas", 0)
    c = st.session_state.data.get("Respuestas Correctas", 0)
    pct = st.session_state.data.get("Promedio (%)", "0.00")

    st.markdown("<h1 style='text-align:center;'>¡Evaluación Finalizada! 🎉</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h2 style="color:{FG_TITULO};">{c} / {n} correctas</h2>
        <h3 style="color:{FG_TEXTO};">Puntaje: {pct}%</h3>
        <p style="color:{FG_TEXTO}; margin-top:1rem;">
            Tus respuestas han sido registradas. Agradecemos tu participación.<br>
            Por favor llama al investigador para continuar.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📥 Descargar Resultados")
    col1, col2 = st.columns(2)

    with col1:
        excel_bytes = construir_excel()
        st.download_button(
            label="⬇️ Descargar Excel (.xlsx)",
            data=excel_bytes,
            file_name="resultado_evaluacion_conductual.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with col2:
        csv_bytes = construir_csv()
        st.download_button(
            label="⬇️ Descargar CSV (.csv)",
            data=csv_bytes,
            file_name="resultado_evaluacion_conductual.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Tabla resumen de respuestas
    if st.session_state.answers:
        st.markdown("### 📋 Resumen de Respuestas")
        df_resumen = pd.DataFrame(st.session_state.answers)[
            ["Categoria", "Pregunta", "Respuesta Seleccionada", "Respuesta Correcta Texto", "Resultado"]
        ]
        df_resumen.index = range(1, len(df_resumen) + 1)
        st.dataframe(df_resumen, use_container_width=True)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Evaluación de Psicología",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    inject_css()
    init_state()

    pagina = st.session_state.pagina

    if pagina == "bienvenida":
        vista_bienvenida()
    elif pagina == "consentimiento":
        vista_consentimiento()
    elif pagina == "posgrado":
        vista_posgrado()
    elif pagina == "datos_posgrado":
        vista_datos_posgrado()
    elif pagina == "demograficos":
        vista_demograficos()
    elif pagina == "autoevaluacion":
        vista_autoevaluacion()
    elif pagina == "preguntas":
        vista_preguntas()
    elif pagina == "resultados":
        vista_resultados()
    else:
        ir_a("bienvenida")
        st.rerun()


if __name__ == "__main__":
    main()
