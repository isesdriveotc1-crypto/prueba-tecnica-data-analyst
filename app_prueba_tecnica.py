import streamlit as st
import json
import os
from datetime import datetime
st.set_page_config(page_title="Prueba Técnica Data Analyst", page_icon="📊", layout="centered")

# --- CUSTOM CSS FOR STYLING ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #FFFFFF !important;
    }
    
    /* Forzar color blanco en los textos de markdown y labels, sin afectar botones */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, label p, label div {
        color: #FFFFFF !important;
    }

    .question-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        border-left: 5px solid #00E676;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    .question-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }
    
    /* Ajuste para TODOS los botones (incluyendo el Form Submit) */
    button {
        background-color: #00E676 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s;
    }
    button p, button div, button span {
        color: #000000 !important; /* Forzar color oscuro en textos internos del botón */
        font-weight: 800 !important;
    }
    button:hover {
        background-color: #00C853 !important;
        transform: scale(1.02);
    }
    button:hover p, button:hover div, button:hover span {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Prueba Técnica: Senior Data Analyst")
st.write("Bienvenido al entorno de evaluación. Por favor, responde las siguientes 10 preguntas. Al finalizar, el sistema calculará tu puntuación y nivel.")

# --- QUESTIONS DATABASE ---
questions = [
    {
        "id": 1,
        "question": "¿Cuál es la principal diferencia entre usar CTEs (Common Table Expressions) y subconsultas en SQL?",
        "options": [
            "Los CTEs mejoran principalmente la legibilidad y permiten recursividad, mientras que el optimizador suele tratar a ambos de forma similar en consultas simples.",
            "Un CTE solo puede ser llamado una vez dentro de la consulta principal, lo que reduce el consumo de CPU.",
            "Las subconsultas en el WHERE impiden que el motor de base de datos utilice índices preexistentes.",
            "Los CTEs siempre se materializan en disco, mientras que las subconsultas siempre se ejecutan en memoria."
        ],
        "answer": "Los CTEs mejoran principalmente la legibilidad y permiten recursividad, mientras que el optimizador suele tratar a ambos de forma similar en consultas simples.",
        "concept": "SQL"
    },
    {
        "id": 2,
        "question": "Se requiere calcular el 'Total Sales Year-to-Date (YTD)' en Power BI utilizando DAX, pero el año fiscal de la empresa termina en Junio. ¿Qué función o combinación es la más adecuada?",
        "options": [
            "TOTALYTD([Total Sales], 'Date'[Date], \"06-30\")",
            "CALCULATE([Total Sales], DATESYTD('Date'[Date]))",
            "SAMEPERIODLASTYEAR(TOTALYTD([Total Sales], 'Date'[Date]))",
            "SUMX(FILTER('Sales', 'Sales'[Month] <= 6), [Total Sales])"
        ],
        "answer": "TOTALYTD([Total Sales], 'Date'[Date], \"06-30\")",
        "concept": "DAX"
    },
    {
        "id": 3,
        "question": "En Python (Pandas), tienes un DataFrame con millones de registros y necesitas aplicar una lógica compleja de limpieza que depende de múltiples columnas. ¿Cuál es el método más eficiente en términos de rendimiento?",
        "options": [
            "Utilizar funciones vectorizadas de NumPy o el método df.apply() con axis=1.",
            "Convertir el DataFrame a una lista de diccionarios y procesarlo.",
            "Iterar con un bucle 'for' usando df.iterrows().",
            "Usar df.groupby() en todas las columnas para reducir el tamaño antes de limpiar."
        ],
        "answer": "Utilizar funciones vectorizadas de NumPy o el método df.apply() con axis=1.",
        "concept": "Python/Pandas"
    },
    {
        "id": 4,
        "question": "El perfil menciona el uso de Power Automate. ¿Cuál es el disparador (trigger) más eficiente para actualizar un reporte de Power BI solo cuando un archivo Excel específico llega a una carpeta de SharePoint?",
        "options": [
            "Trigger: 'When a HTTP request is received' desde Power BI.",
            "Trigger: 'Recurrence' cada 5 minutos con una condición de búsqueda de archivo.",
            "Programar el flujo para que se ejecute cada hora y revise si hay archivos nuevos.",
            "Trigger: 'When a file is created (properties only)' en SharePoint seguido de la acción 'Refresh a Power BI dataset'."
        ],
        "answer": "Trigger: 'When a file is created (properties only)' en SharePoint seguido de la acción 'Refresh a Power BI dataset'.",
        "concept": "Power Automate"
    },
    {
        "id": 5,
        "question": "Al diseñar un modelo de datos en Power BI para el área de Operaciones, ¿por qué es preferible un 'Esquema de Estrella' (Star Schema) sobre un 'Esquema de Copo de Nieve' (Snowflake)?",
        "options": [
            "Porque Power BI no permite más de dos niveles de jerarquía en las dimensiones de un Snowflake.",
            "Porque reduce la cantidad de uniones (joins) necesarias, mejorando el rendimiento de las medidas DAX y la facilidad de uso para el usuario final.",
            "Porque el esquema de estrella ocupa mucho menos espacio en disco.",
            "Porque el esquema de estrella elimina la necesidad de usar una tabla de Calendario (DimDate)."
        ],
        "answer": "Porque reduce la cantidad de uniones (joins) necesarias, mejorando el rendimiento de las medidas DAX y la facilidad de uso para el usuario final.",
        "concept": "Data Modeling"
    },
    {
        "id": 6,
        "question": "Estás analizando la correlación entre dos variables operativas en Python. Si el coeficiente de correlación de Pearson es 0.85, pero el gráfico de dispersión muestra una relación curva (parabólica), ¿qué conclusión es correcta?",
        "options": [
            "Un valor de 0.85 indica que el 85% de los datos son idénticos en ambas variables.",
            "Pearson puede estar sobreestimando la relación lineal; se debería considerar una transformación de variables o un coeficiente de Spearman.",
            "La correlación de Pearson es el indicador definitivo de que existe una relación lineal fuerte.",
            "No existe ninguna relación entre las variables si el gráfico no es una línea recta perfecta."
        ],
        "answer": "Pearson puede estar sobreestimando la relación lineal; se debería considerar una transformación de variables o un coeficiente de Spearman.",
        "concept": "Statistics/Python"
    },
    {
        "id": 7,
        "question": "Se te pide crear un dashboard para la Gerencia de Operaciones. ¿Cuál es la mejor práctica de 'Data Storytelling' para presentar un hallazgo crítico sobre la caída de la productividad?",
        "options": [
            "Utilizar gráficos 3D y colores brillantes para captar la atención de los directivos de inmediato.",
            "Presentar los datos en orden cronológico inverso, sin importar dónde esté el hallazgo crítico.",
            "Usar un gráfico que resalte claramente la anomalía, acompañado de una narrativa breve que explique la causa y una recomendación de acción.",
            "Incluir todas las tablas de datos posibles para que la gerencia pueda investigar por su cuenta."
        ],
        "answer": "Usar un gráfico que resalte claramente la anomalía, acompañado de una narrativa breve que explique la causa y una recomendación de acción.",
        "concept": "Data Storytelling"
    },
    {
        "id": 8,
        "question": "En SQL, necesitas encontrar los clientes que realizaron compras en el mes actual pero que no compraron nada en el mes anterior. ¿Cuál es la técnica más eficiente?",
        "options": [
            "Un INNER JOIN entre los dos meses y luego filtrar los nulos manualmente en Excel.",
            "Usar un GROUP BY y filtrar aquellos que tengan una cuenta de meses igual a 1.",
            "Un FULL OUTER JOIN entre la tabla de este mes y la del mes pasado.",
            "Un SELECT de los clientes actuales con una cláusula EXCEPT (o MINUS) que reste los clientes del mes pasado."
        ],
        "answer": "Un SELECT de los clientes actuales con una cláusula EXCEPT (o MINUS) que reste los clientes del mes pasado.",
        "concept": "SQL"
    },
    {
        "id": 9,
        "question": "Al trabajar con Modelado en Microsoft Fabric, ¿cuál es la ventaja clave de utilizar el modo 'Direct Lake' en comparación con 'Import' o 'DirectQuery'?",
        "options": [
            "Direct Lake requiere que los datos se dupliquen en la memoria de Power BI cada vez que hay una consulta.",
            "Direct Lake es el único modo que permite usar Python dentro de los reportes de Power BI.",
            "Permite analizar volúmenes masivos de datos directamente desde OneLake sin necesidad de importarlos, manteniendo el rendimiento de alta velocidad.",
            "Solo funciona si los datos están almacenados en archivos CSV locales."
        ],
        "answer": "Permite analizar volúmenes masivos de datos directamente desde OneLake sin necesidad de importarlos, manteniendo el rendimiento de alta velocidad.",
        "concept": "Microsoft Fabric"
    },
    {
        "id": 10,
        "question": "Como facilitador de cultura 'Data-Driven', un equipo se queja de que los datos del dashboard 'no coinciden con sus archivos manuales'. ¿Cuál debe ser tu primera acción como Senior Analyst?",
        "options": [
            "Cambiar los datos del dashboard para que coincidan con los archivos manuales sin investigar más.",
            "Realizar un ejercicio de 'Lineage' y conciliación de datos para identificar la fuente de la discrepancia y explicar las reglas de negocio aplicadas.",
            "Ignorar la queja, asumiendo que el proceso automatizado siempre es el correcto.",
            "Pedirle al equipo que deje de usar sus archivos manuales inmediatamente por orden de la gerencia."
        ],
        "answer": "Realizar un ejercicio de 'Lineage' y conciliación de datos para identificar la fuente de la discrepancia y explicar las reglas de negocio aplicadas.",
        "concept": "Data Culture/Analysis"
    }
]

def initialize_session_state():
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "candidate_name" not in st.session_state:
        st.session_state.candidate_name = ""
    if "show_confirm" not in st.session_state:
        st.session_state.show_confirm = False

initialize_session_state()

# --- MAIN APP ---
if not st.session_state.submitted:
    
    st.session_state.candidate_name = st.text_input("Nombre del Candidato:", placeholder="Ingresa tu nombre completo")
    st.markdown("---")

    with st.form("test_form"):
        for q in questions:
            st.markdown(f'<div class="question-box"><h4>Pregunta {q["id"]} de 10</h4><p>{q["question"]}</p></div>', unsafe_allow_html=True)
            # Add a placeholder option to force the user to select something
            options = ["(Selecciona una opción)"] + q["options"]
            selected_option = st.radio(f"Respuesta {q['id']}", options, index=0, label_visibility="collapsed", key=f"q_{q['id']}")
            st.session_state.user_answers[q["id"]] = selected_option
            st.markdown("<br>", unsafe_allow_html=True)
            
        submitted = st.form_submit_button("Enviar Prueba")
        
        if submitted:
            if st.session_state.candidate_name.strip() == "":
                st.error("Por favor, ingresa tu nombre antes de enviar la prueba.")
            else:
                # Validate all questions answered
                unanswered = [q["id"] for q in questions if st.session_state.user_answers[q["id"]] == "(Selecciona una opción)"]
                if unanswered:
                    st.error(f"Faltan por responder las preguntas: {', '.join(map(str, unanswered))}")
                else:
                    st.session_state.show_confirm = True
                    st.rerun()

    if st.session_state.show_confirm:
        st.warning("⚠️ ¿Seguro que deseas enviar la prueba? Por favor confirma para ver tus resultados.")
        col1, col2 = st.columns(2)
        if col1.button("✅ Sí, enviar prueba"):
            # Calculate score
            score = 0
            for q in questions:
                if st.session_state.user_answers[q["id"]] == q["answer"]:
                    score += 1
            
            percentage = (score / len(questions)) * 100
            if percentage < 60:
                level = "Junior / Analista Básico"
            elif percentage < 85:
                level = "Mid / Semi-Senior Data Analyst"
            else:
                level = "Senior Data Analyst"

            # Save to JSON
            result_data = {
                "timestamp": datetime.now().isoformat(),
                "candidato": st.session_state.candidate_name,
                "score": score,
                "total": len(questions),
                "percentage": percentage,
                "level": level,
                "answers": st.session_state.user_answers
            }
            
            file_path = "resultados_candidatos.json"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except:
                        data = []
            else:
                data = []
            data.append(result_data)
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            st.session_state.score = score
            st.session_state.submitted = True
            st.session_state.show_confirm = False
            st.rerun()
        if col2.button("❌ Cancelar y revisar respuestas"):
            st.session_state.show_confirm = False
            st.rerun()
else:
    st.header("✅ Prueba Completada")
    st.markdown(
        f"""
        <div style="background-color: #1E1E1E; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #4CAF50;">
            <h2 style="margin: 0; color: #FAFAFA;">¡Gracias, {st.session_state.candidate_name}!</h2>
            <p style="margin-top: 15px; font-size: 1.2em; color: #FAFAFA;">Tu prueba ha sido enviada exitosamente.</p>
            <p style="color: #FAFAFA;">El equipo de evaluación revisará tus resultados y se pondrá en contacto contigo pronto.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("Volver al Inicio"):
        st.session_state.submitted = False
        st.session_state.score = 0
        st.session_state.user_answers = {}
        st.session_state.candidate_name = ""
        st.rerun()
