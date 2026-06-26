import streamlit as st
import pandas as pd
import time
import random
import logging
import json

# 1. CONFIGURACIÓN DE LOGS ESTRUCTURADOS
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "trace_id": getattr(record, 'trace_id', 'N/A'),
            "mensaje": record.getMessage(),
            "componente": "Agente_Ferreteria_IA"
        })

logger = logging.getLogger("ObservabilidadIA")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# 2. MOTOR DEL AGENTE CON MÉTRICAS Y SEGURIDAD
def procesar_consulta_ia(prompt, trace_id):
    start_time = time.time()
    
    # Protocolo de Seguridad y Privacidad (Filtro PII / Inyección de Prompts)
    palabras_bloqueadas = ["rut", "clave", "tarjeta", "password", "drop table"]
    if any(palabra in prompt.lower() for palabra in palabras_bloqueadas):
        logger.warning("Alerta de Seguridad: Intento de fuga de datos o inyección detectada.", extra={"trace_id": trace_id})
        return {"Trace_ID": trace_id, "Latencia": 0.1, "Consistencia": 0.0, "Tokens": 0, "Estado": "Bloqueado por Seguridad"}

    # Simulación de procesamiento con variabilidad de datos
    time.sleep(random.uniform(0.3, 2.4)) 
    tokens_estimados = len(prompt.split()) + random.randint(100, 500)
    
    # Simulación de consistencia y tasa de errores del modelo
    exito = random.choices([True, False], weights=[0.88, 0.12])[0]
    consistencia = random.uniform(0.85, 0.99) if exito else random.uniform(0.20, 0.55)
    latencia = time.time() - start_time

    if exito:
        logger.info(f"Consulta procesada exitosamente. Tokens: {tokens_estimados}", extra={"trace_id": trace_id})
        estado = "Exitoso"
    else:
        logger.error("Falla de Consistencia: El modelo generó una respuesta alucinada o incompleta.", extra={"trace_id": trace_id})
        estado = "Error de Precisión"

    return {
        "Trace_ID": trace_id,
        "Latencia": latencia,
        "Consistencia": consistencia,
        "Tokens": tokens_estimados,
        "Estado": estado
    }

# 3. DASHBOARD VISUAL INTERACTIVO
st.set_page_config(page_title="Dashboard Observabilidad IA", layout="wide")
st.title("Panel de Observabilidad y Trazabilidad - Agente IA")
st.markdown("### Sistema de Monitoreo en Tiempo Real para Ferretería El Martillo")

# Mantener el historial de ejecuciones en la sesión
if "logs_df" not in st.session_state:
    datos_simulados = []
    for i in range(25):
        datos_simulados.append({
            "Trace_ID": f"tr-{random.randint(1000, 1999)}",
            "Latencia": random.uniform(0.4, 2.2),
            "Consistencia": random.uniform(0.70, 0.99) if random.random() > 0.1 else random.uniform(0.3, 0.5),
            "Tokens": random.randint(120, 600),
            "Estado": random.choices(["Exitoso", "Error de Precisión"], weights=[0.90, 0.10])[0]
        })
    st.session_state.logs_df = pd.DataFrame(datos_simulados)

df = st.session_state.logs_df

# Cuadro de pruebas en vivo
with st.expander("Probar Agente de IA en Vivo (Evaluación de Escenarios)", expanded=True):
    col_txt, col_btn = st.columns([4, 1])
    with col_txt:
        prompt_input = st.text_input("Consulta del cliente:", "Cotizar 50 planchas de zinc y 3 cajas de tornillos")
    with col_btn:
        st.write("#")
        if st.button("Enviar Consulta", use_container_width=True):
            nuevo_id = f"tr-{random.randint(2000, 9999)}"
            res = procesar_consulta_ia(prompt_input, nuevo_id)
            st.session_state.logs_df = pd.concat([st.session_state.logs_df, pd.DataFrame([res])], ignore_index=True)
            df = st.session_state.logs_df
            st.success(f"Procesado con Trace ID: {nuevo_id} | Estado: {res['Estado']}")

st.markdown("---")

# Métricas Principales
total_req = len(df)
errores = len(df[df["Estado"] != "Exitoso"])
error_rate = (errores / total_req) * 100
avg_lat = df["Latencia"].mean()
avg_cons = df["Consistencia"].mean() * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Consultas (Volumen)", f"{total_req}")
c2.metric("Latencia Promedio", f"{avg_lat:.2f} s")
c3.metric("Consistencia Lógica", f"{avg_cons:.1f}%")
c4.metric("Tasa de Error", f"{error_rate:.1f}%", delta=f"{error_rate:.1f}%", delta_color="inverse")

# Gráficos de Rendimiento y Análisis de Anomalías
st.subheader("Análisis de Patrones y Cuellos de Botella")
g1, g2 = st.columns(2)

with g1:
    st.markdown("**Variabilidad de Latencia por Transacción (Métrica de Rendimiento)**")
    st.line_chart(df["Latencia"])

with g2:
    st.markdown("**Uso de Recursos (Consumo de Tokens por Petición)**")
    st.bar_chart(df["Tokens"])

# Tabla de Trazabilidad / Registros logs
st.subheader("Registros de Trazabilidad Recientes (Dataframe de Logs)")
st.dataframe(df.tail(10), use_container_width=True)