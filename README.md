# Sistema de Observabilidad - Agente de IA (Ferretería El Martillo)

## 🛠️ Requisitos
- Python 3.10 o superior
- Instalar librerías:
  ```bash
  pip install streamlit pandas
  ```

# Ejecución

Ejecute el siguiente comando en la terminal para iniciar el dashboard:

```bash
streamlit runpp.py
```

Abra su navegador web e ingrese a la siguiente dirección:

http://localhost:8501

Características del Sistema

Métricas: Monitoreo en tiempo real de latencia, volumen de consultas y consumo de tokens.

Trazabilidad: Logs estructurados en formato JSON vinculados mediante un identificador único (trace_id).

Seguridad: Bloqueo automático ante intentos de inyección de código o exposición de datos sensibles (PII).
