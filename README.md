# QueryMind: Agente Analista de Datos MiBici GDL 🚲🤖

[![Presentación en Prezi](https://img.shields.io/badge/Prezi-Presentación-blue?logo=prezi&logoColor=white)](https://prezi.com/p/equt8wg8trwy/?referral_token=aeQi97lnB3FN)

Este repositorio contiene el **demo técnico** oficial de la presentación: 
> **"Más allá del Chat: Construyendo Agentes Autónomos con Python y Google Cloud"** > **Speaker:** Jose Muñoz  
> **Presentación:** [Ver en Prezi](https://prezi.com/p/equt8wg8trwy/?referral_token=aeQi97lnB3FN)

## 1. El Concepto: De Chatbots a Agentes
A diferencia de un chatbot tradicional que sigue un flujo lineal y "muere" ante un error de API o una alucinación, **QueryMind** demuestra los principios de la **Ingeniería Agéntica**. El código sirve para ilustrar cómo pasar de "rogarle" al LLM con prompts largos a diseñar arquitecturas de razonamiento cíclicas con **LangGraph**.

## 2. Arquitectura del Demo
El proyecto está estructurado para comparar dos paradigmas discutidos en la sesión:

* **Linear Chain (Legacy Flow):** Implementado en `strategies/linear_chain/`, muestra las limitaciones de los flujos secuenciales (Arquitecto -> Validador -> Intérprete).
* **Stateful Graph (Agentic Flow):** La pieza central del demo. Utiliza un grafo de estados para permitir que el agente use herramientas, se equivoque, aprenda del error de BigQuery y genere una consulta corregida de forma autónoma.

## 3. Desafíos Reales de Producción Resueltos
Este demo aborda problemas específicos del dataset de **MiBici Guadalajara** mencionados en la presentación:

* **El Problema de la "ñ":** Manejo programático y vía prompt del campo `` `Año_de_nacimiento` `` en BigQuery para evitar errores de sintaxis comunes.
* **Geo-Resolución Local:** Implementación de un `guadalajara_geo_resolver` que traduce lenguaje coloquial ("La Minerva", "Chapu") en coordenadas y filtros SQL.
* **Observabilidad de Grafos:** Un sistema de logs personalizado en la UI que permite ver "el cerebro del agente" trabajando en tiempo real, latencias y veredictos de seguridad.

## 4. Stack Tecnológico
* **LLM:** Google Gemini 1.5 Pro/Flash.
* **Orquestación:** LangGraph.
* **Data Warehouse:** Google BigQuery.
* **Cloud:** Google Cloud Platform (GCP).

## 5. Estructura del Proyecto
```text
├── core/                   # Configuración y proveedores de Gemini
├── strategies/
│   ├── linear_chain/       # Ejemplo de flujo lineal (Legacy)
│   └── stateful_graph/     # Demo de Agente Autónomo (LangGraph)
│       ├── tools/          # Herramientas de consulta e introspección
│       └── skills/         # Habilidades: SQL Expert y Geo-Resolver
├── ui/                     # Formateador visual para la consola
└── main.py                 # Punto de entrada del demo
```

## 6. Instalación y Uso
### 1. Clonar y configurar:

```bash
git clone <repository-url>
cp .env-template .env
```

### 2. Configurar credenciales de GCP:
Asegúrate de tener acceso al dataset público de MiBici o al dataset configurado en tu proyecto de BigQuery.
Ejecutar:

```bash
python main.py
```

## 7. Conclusión de la Charla
Como se vio en el demo, la meta no es solo consultar datos, sino evolucionar hacia Movilidad Autónoma, donde los agentes propongan estrategias de rebalanceo de unidades en estaciones críticas basándose en insights generados automáticamente.

Este código fue diseñado con fines educativos para demostrar el poder de los agentes autónomos en el ecosistema de Google Cloud.