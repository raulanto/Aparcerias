# 📊 Módulo 1 — Dashboard General
> **AparceríaPro** · Documentación técnica y funcional

---

## ¿Qué es y para qué sirve?

El Dashboard es el **centro de comando operativo** del sistema. Concentra en una sola pantalla los indicadores más críticos del negocio ganadero: inventario vivo, salud financiera, contratos activos y alertas de atención. Está diseñado para que el administrador o dueño tome decisiones informadas en segundos, sin necesidad de navegar entre módulos.

En la industria pecuaria, la pérdida de utilidad frecuentemente ocurre por **falta de visibilidad en tiempo real**: un animal enfermo que no se detecta a tiempo, un contrato que vence sin liquidarse, o una compra que descapitaliza la operación. El dashboard previene todos estos escenarios.

---

## Información que concentra

| Categoría | Dato | Frecuencia de actualización |
|---|---|---|
| Inventario | Total de cabezas activas por especie | Tiempo real |
| Finanzas | Ingresos / Egresos / Utilidad neta | Al registrar transacción |
| Contratos | Activos, por vencer (≤30 días), finalizados | Tiempo real |
| Sanidad | Animales en tratamiento / alertas | Tiempo real |
| Aparceros | Socios activos y monto comprometido | Tiempo real |
| Mercado | Precio estimado del kg en pie (configurable) | Manual / API externa |

---

## Diagrama de flujo del Dashboard

```mermaid
flowchart TD
    A([Usuario entra al sistema]) --> B[Dashboard carga KPIs]
    B --> C{¿Hay alertas críticas?}
    C -- Sí --> D[🔴 Panel de alertas visible]
    C -- No --> E[✅ Estado normal]
    D --> F[Alerta: Animal en tratamiento]
    D --> G[Alerta: Contrato por vencer]
    D --> H[Alerta: Inventario bajo mínimo]
    B --> I[Gráfica flujo financiero mensual]
    B --> J[Distribución por especie]
    B --> K[Actividad reciente]
    I --> L[Usuario filtra por período]
    J --> M[Click → navega a módulo Ganado]
    K --> N[Click → navega a transacción]
```

---

## Diagrama de KPIs y sus fuentes

```mermaid
graph LR
    subgraph FUENTES
        G[📦 Módulo Ganado]
        C[📋 Módulo Contratos]
        F[💰 Módulo Finanzas]
        S[💊 Módulo Sanidad]
    end

    subgraph DASHBOARD
        K1[Cabezas activas]
        K2[Valor inventario]
        K3[Utilidad neta]
        K4[Contratos vigentes]
        K5[Alertas sanitarias]
        K6[ROI acumulado]
    end

    G --> K1
    G --> K2
    F --> K3
    F --> K6
    C --> K4
    S --> K5
```

---

## Alertas inteligentes

El sistema debe generar alertas automáticas basadas en reglas configurables:

```mermaid
stateDiagram-v2
    [*] --> Normal
    Normal --> Advertencia : Contrato vence en ≤30 días
    Normal --> Advertencia : Animal sin revisión ≥90 días
    Normal --> Crítico : Contrato vencido sin liquidar
    Normal --> Crítico : Animal en tratamiento >15 días
    Normal --> Crítico : Pérdida neta detectada
    Advertencia --> Normal : Condición resuelta
    Crítico --> Advertencia : En proceso de resolución
    Crítico --> Normal : Condición resuelta
```

---

## Campos de configuración del Dashboard

- **Rancho activo**: nombre, RFC, estado/municipio
- **Ejercicio fiscal**: año o período personalizado
- **Moneda base**: MXN (con soporte futuro USD)
- **Precio de referencia por kg**: actualizable manualmente
- **Widgets activos**: el usuario decide cuáles KPIs mostrar
- **Umbral de alertas**: días de anticipación configurables

---

## Ventaja competitiva en la industria

> La mayoría de los ranchos llevan la administración en **cuadernos físicos o Excel sin fórmulas**. Un dashboard digitalizado permite:
> - Detectar pérdidas antes de que sucedan
> - Presentar reportes a socios en tiempo real
> - Acceder al estado del negocio desde cualquier dispositivo
> - Comparar el desempeño entre temporadas
