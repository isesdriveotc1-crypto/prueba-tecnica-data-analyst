import streamlit as st
import json
import os
from fpdf import FPDF
import os

st.set_page_config(page_title="Panel Evaluador", page_icon="🔐", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a2a6c, #11998e, #38ef7d);
        color: #FFFFFF;
    }
    p, span, h1, h2, h3, h4, label, .stMarkdown {
        color: #FFFFFF !important;
    }
    .metric-box {
        background: rgba(0, 0, 0, 0.4);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #38ef7d;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- QUESTIONS DATABASE PARA VALIDACION ---
questions_db = {
    "1": {"q": "¿Cuál es la principal diferencia entre usar CTEs (Common Table Expressions) y subconsultas en SQL?", "a": "Los CTEs mejoran principalmente la legibilidad y permiten recursividad, mientras que el optimizador suele tratar a ambos de forma similar en consultas simples."},
    "2": {"q": "Se requiere calcular el 'Total Sales Year-to-Date (YTD)' en Power BI utilizando DAX, pero el año fiscal de la empresa termina en Junio. ¿Qué función o combinación es la más adecuada?", "a": "TOTALYTD([Total Sales], 'Date'[Date], \"06-30\")"},
    "3": {"q": "En Python (Pandas), tienes un DataFrame con millones de registros y necesitas aplicar una lógica compleja de limpieza que depende de múltiples columnas. ¿Cuál es el método más eficiente en términos de rendimiento?", "a": "Utilizar funciones vectorizadas de NumPy o el método df.apply() con axis=1."},
    "4": {"q": "El perfil menciona el uso de Power Automate. ¿Cuál es el disparador (trigger) más eficiente para actualizar un reporte de Power BI solo cuando un archivo Excel específico llega a una carpeta de SharePoint?", "a": "Trigger: 'When a file is created (properties only)' en SharePoint seguido de la acción 'Refresh a Power BI dataset'."},
    "5": {"q": "Al diseñar un modelo de datos en Power BI para el área de Operaciones, ¿por qué es preferible un 'Esquema de Estrella' (Star Schema) sobre un 'Esquema de Copo de Nieve' (Snowflake)?", "a": "Porque reduce la cantidad de uniones (joins) necesarias, mejorando el rendimiento de las medidas DAX y la facilidad de uso para el usuario final."},
    "6": {"q": "Estás analizando la correlación entre dos variables operativas en Python. Si el coeficiente de correlación de Pearson es 0.85, pero el gráfico de dispersión muestra una relación curva (parabólica), ¿qué conclusión es correcta?", "a": "Pearson puede estar sobreestimando la relación lineal; se debería considerar una transformación de variables o un coeficiente de Spearman."},
    "7": {"q": "Se te pide crear un dashboard para la Gerencia de Operaciones. ¿Cuál es la mejor práctica de 'Data Storytelling' para presentar un hallazgo crítico sobre la caída de la productividad?", "a": "Usar un gráfico que resalte claramente la anomalía, acompañado de una narrativa breve que explique la causa y una recomendación de acción."},
    "8": {"q": "En SQL, necesitas encontrar los clientes que realizaron compras en el mes actual pero que no compraron nada en el mes anterior. ¿Cuál es la técnica más eficiente?", "a": "Un SELECT de los clientes actuales con una cláusula EXCEPT (o MINUS) que reste los clientes del mes pasado."},
    "9": {"q": "Al trabajar con Modelado en Microsoft Fabric, ¿cuál es la ventaja clave de utilizar el modo 'Direct Lake' en comparación con 'Import' o 'DirectQuery'?", "a": "Permite analizar volúmenes masivos de datos directamente desde OneLake sin necesidad de importarlos, manteniendo el rendimiento de alta velocidad."},
    "10": {"q": "Como facilitador de cultura 'Data-Driven', un equipo se queja de que los datos del dashboard 'no coinciden con sus archivos manuales'. ¿Cuál debe ser tu primera acción como Senior Analyst?", "a": "Realizar un ejercicio de 'Lineage' y conciliación de datos para identificar la fuente de la discrepancia y explicar las reglas de negocio aplicadas."}
}

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "Admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.header("🔐 Acceso Restringido")
        st.text_input(
            "Por favor, ingresa la contraseña para acceder al panel de evaluador:",
            type="password",
            on_change=password_entered,
            key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.header("🔐 Acceso Restringido")
        st.text_input(
            "Por favor, ingresa la contraseña para acceder al panel de evaluador:",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("😕 Contraseña incorrecta")
        return False
    else:
        return True

def generate_pdf_report(cand_data, questions_db):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(26, 42, 108)
    
    # Manejar posibles problemas de codificación de caracteres pasando a ascii ignorando acentos si falla
    # Pero fpdf2 maneja utf-8 con fuentes TTF integradas u opciones básicas.
    
    pdf.cell(0, 10, "Reporte de Prueba Tecnica: Data Analyst", ln=True, align="C")
    
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Fecha de realizacion: {cand_data['timestamp'][:10]} a las {cand_data['timestamp'][11:16]}", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, f"Candidato: {cand_data['candidato']}", ln=True, fill=True)
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 8, f"Puntaje: {cand_data['score']} / {cand_data['total']} ({cand_data['percentage']:.0f}%)", ln=True, fill=True)
    pdf.cell(0, 8, f"Nivel Clasificado: {cand_data['level']}", ln=True, fill=True)
    pdf.ln(10)
    
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(26, 42, 108)
    pdf.cell(0, 10, "Desglose de Respuestas", ln=True)
    pdf.ln(5)
    
    for q_id_str, user_ans in cand_data.get("answers", {}).items():
        q_info = questions_db.get(str(q_id_str), {"q": f"Pregunta {q_id_str}", "a": "Desconocida"})
        is_correct = (user_ans == q_info["a"])
        
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(0, 0, 0)
        q_text = f"Pregunta {q_id_str}: {q_info['q']}".encode('latin-1', 'replace').decode('latin-1')
        pdf.write(6, q_text)
        pdf.ln(8)
        
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        user_ans_clean = f"Su respuesta: {user_ans}".encode('latin-1', 'replace').decode('latin-1')
        pdf.write(6, user_ans_clean)
        pdf.ln(8)
        
        if not is_correct:
            pdf.set_text_color(220, 53, 69) # Red
            pdf.write(6, "Estado: INCORRECTA")
            pdf.ln(6)
            pdf.set_text_color(40, 167, 69) # Green
            correct_ans_clean = f"Respuesta correcta: {q_info['a']}".encode('latin-1', 'replace').decode('latin-1')
            pdf.write(6, correct_ans_clean)
            pdf.ln(6)
        else:
            pdf.set_text_color(40, 167, 69) # Green
            pdf.write(6, "Estado: CORRECTA")
            pdf.ln(6)
            
        pdf.ln(5)
        
    return pdf.output()

if check_password():
    st.title("📊 Panel de Control: Resultados de Evaluaciones")
    
    file_path = "resultados_candidatos.json"
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []
        
    if not data:
        st.info("Aún no hay resultados registrados. Los datos aparecerán aquí cuando un aspirante complete la prueba.")
    else:
        st.markdown("### Resumen de Candidatos")
        
        # Display as a table
        import pandas as pd
        
        df = pd.DataFrame(data)
        # Format the dataframe for display
        display_df = df[["timestamp", "candidato", "score", "total", "percentage", "level"]].copy()
        display_df["timestamp"] = pd.to_datetime(display_df["timestamp"]).dt.strftime('%Y-%m-%d %H:%M')
        display_df["percentage"] = display_df["percentage"].apply(lambda x: f"{x:.0f}%")
        display_df.columns = ["Fecha/Hora", "Nombre del Candidato", "Puntos", "Total Preguntas", "Porcentaje", "Nivel Clasificado"]
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### Detalles por Candidato")
        
        # Select a candidate to see detailed answers
        candidatos_list = [f"{d['candidato']} ({d['timestamp'][:10]})" for d in data]
        selected_cand_idx = st.selectbox("Selecciona un candidato para ver sus respuestas:", range(len(candidatos_list)), format_func=lambda x: candidatos_list[x])
        
        if selected_cand_idx is not None:
            cand_data = data[selected_cand_idx]
            
            st.markdown(
                f"""
                <div class="metric-box">
                    <h2 style="margin: 0; color: #FAFAFA;">Candidato: {cand_data['candidato']}</h2>
                    <h1 style="font-size: 3em; margin: 10px 0; color: #38ef7d;">{cand_data['score']} / {cand_data['total']}</h1>
                    <h3 style="margin: 0; color: #FAFAFA;">Porcentaje: {cand_data['percentage']:.0f}%</h3>
                    <h3 style="margin-top: 5px; color: #FAFAFA;">Nivel Clasificado: {cand_data['level']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("Desglose de Respuestas")
            with col2:
                pdf_report_bytes = generate_pdf_report(cand_data, questions_db)
                st.download_button(
                    label="📄 Descargar Reporte en PDF",
                    data=bytes(pdf_report_bytes),
                    file_name=f"Reporte_DataAnalyst_{cand_data['candidato'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            answers = cand_data.get("answers", {})
            
            # Show a filter to view only errors
            show_only_errors = st.checkbox("Mostrar SOLO las respuestas incorrectas")
            
            for q_id_str, user_ans in answers.items():
                q_info = questions_db.get(str(q_id_str), {"q": f"Pregunta {q_id_str}", "a": "Desconocida"})
                is_correct = (user_ans == q_info["a"])
                
                if show_only_errors and is_correct:
                    continue
                
                icon = "✅" if is_correct else "❌"
                color = "#4CAF50" if is_correct else "#F44336"
                
                st.markdown(
                    f"""
                    <div style="border-left: 5px solid {color}; padding: 15px; margin-bottom: 10px; background-color: rgba(255,255,255,0.05); border-radius: 5px;">
                        <p><strong>Pregunta {q_id_str}: {q_info['q']}</strong></p>
                        <p style="margin-bottom: 5px;">Su respuesta: {icon} <span style="color: {'#A5D6A7' if is_correct else '#EF9A9A'}">{user_ans}</span></p>
                        {f'<p style="margin-bottom: 0;">Respuesta correcta: <span style="color: #A5D6A7">{q_info["a"]}</span></p>' if not is_correct else ''}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
