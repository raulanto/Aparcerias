# 👥 Módulo 6 — Gestión de Socios y Aparceros
> **AparceríaPro** · Documentación técnica y funcional

---

## ¿Qué es y para qué sirve?

Este módulo es el **directorio relacional de socios de negocio** del rancho. Gestiona la información de todas las personas, ejidos o empresas con quienes se realizan contratos de aparcería, compras recurrentes o ventas directas. Va más allá de un simple catálogo: construye un **historial de desempeño** por socio que permite tomar mejores decisiones comerciales.

En la práctica ganadera, la relación con los aparceros es de **largo plazo y basada en confianza**. Digitalizar esa relación con datos objetivos (¿quién ha entregado mejores resultados?, ¿quién ha tenido más bajas?) reduce riesgos y profesionaliza los acuerdos.

---

## Tipos de Aparcero / Socio

| Tipo | Descripción | Características especiales |
|---|---|---|
| Productor individual | Persona física con ganado o tierra propia | RFC personal, CURP |
| Ejido | Núcleo agrario con derechos colectivos | Acta de asamblea, representante legal |
| Empresa / Rancho S.A. | Persona moral | RFC empresa, representante legal, acta constitutiva |
| Comprador recurrente | Rastro, carnicería, empresa cárnica | Datos fiscales para CFDI |
| Proveedor recurrente | Ferias ganaderas, agropecuarias | Datos para trazabilidad |

---

## Campos del Perfil del Aparcero

| Campo | Tipo | Descripción |
|---|---|---|
| ID interno | Texto único | Folio del sistema |
| Nombre / Razón social | Texto | Nombre completo o empresa |
| Tipo | Enum | Ver tabla anterior |
| RFC | Texto | Para facturación y trazabilidad |
| CURP | Texto | Solo personas físicas |
| Domicilio | Texto + mapa | Estado, municipio, localidad |
| Teléfono / WhatsApp | Texto | Contacto principal |
| Correo electrónico | Texto | Para envío de contratos y reportes |
| Número de cuenta bancaria | Texto | Para transferencias de liquidación |
| CLABE interbancaria | Texto | Pagos electrónicos |
| Referencias | Texto libre | Quién lo recomendó, historial previo |
| Documentos adjuntos | Archivos | INE, acta ejidal, acta constitutiva |
| Estado en el sistema | Enum | Activo / Inactivo / Bloqueado / Histórico |
| Calificación de confianza | 1–5 estrellas | Basada en historial de cumplimiento |
| Notas internas | Texto libre | Observaciones del administrador |

---

## Diagrama de ciclo de vida de un Aparcero

```mermaid
stateDiagram-v2
    [*] --> Prospecto : Se identifica como posible socio
    Prospecto --> En_Validacion : Se capturan sus datos
    En_Validacion --> Activo : Documentos validados y primer contrato firmado
    En_Validacion --> Rechazado : Documentos inválidos o antecedentes negativos
    Activo --> Con_Contrato_Activo : Se firma un contrato
    Con_Contrato_Activo --> Activo : Contrato finalizado
    Activo --> Inactivo : Sin actividad por >12 meses
    Inactivo --> Activo : Retoma actividad
    Activo --> Bloqueado : Incumplimiento / disputa legal
    Bloqueado --> Activo : Resolución del conflicto
    Activo --> Historico : Relación comercial cerrada formalmente
```

---

## Historial de desempeño del Aparcero

El sistema construye automáticamente un **score de confianza** basado en datos objetivos:

```mermaid
flowchart TD
    A[Aparcero: Ejido Morelos] --> B[Historial de contratos]
    B --> C1[3 contratos completados]
    B --> C2[0 contratos disputados]
    B --> C3[1 contrato activo]
    
    A --> D[Historial sanitario]
    D --> D1[Mortalidad: 1.2% promedio]
    D --> D2[GDP promedio: 0.95 kg/día]
    
    A --> E[Historial financiero]
    E --> E1[Pagos: siempre a tiempo]
    E --> E2[Utilidad generada: $87,000]
    
    C1 & C2 & D1 & D2 & E1 --> F[⭐⭐⭐⭐⭐ Calificación: 4.8/5]
    F --> G[🟢 Aparcero recomendado para renovar contrato]
```

---

## Diagrama entidad-relación del Aparcero

```mermaid
erDiagram
    APARCERO {
        string id PK
        string nombre
        string tipo
        string rfc
        string curp
        string domicilio
        string telefono
        string email
        string clabe
        string estado
        float calificacion
    }

    CONTRATO {
        string id PK
        string tipo
        date inicio
        date fin
        string estado
    }

    ANIMAL {
        string id PK
        string arete
        string especie
    }

    TRANSACCION {
        string id PK
        string tipo
        decimal monto
        date fecha
    }

    DOCUMENTO {
        string id PK
        string tipo_doc
        string archivo_url
        date vigencia
    }

    NOTA_INTERNA {
        string id PK
        string contenido
        date fecha
        string autor
    }

    APARCERO ||--|{ CONTRATO : "ha firmado"
    APARCERO ||--|{ ANIMAL : "tiene a cargo"
    APARCERO ||--|{ TRANSACCION : "ha realizado"
    APARCERO ||--|{ DOCUMENTO : "tiene adjunto"
    APARCERO ||--|{ NOTA_INTERNA : "tiene notas"
```

---

## Indicadores de desempeño por Aparcero

| Indicador | Descripción |
|---|---|
| Contratos completados | Total de contratos finalizados sin disputa |
| Tasa de mortalidad | % de animales perdidos bajo su cuidado |
| GDP promedio | Ganancia diaria de peso en sus lotes |
| Utilidad generada | Total de utilidad producida en todos sus contratos |
| Tiempo promedio de respuesta | Qué tan rápido responde a comunicaciones |
| Pagos a tiempo | % de liquidaciones pagadas en la fecha acordada |
| Cumplimiento de pesajes | % de pesajes periódicos reportados puntualmente |

---

## Comunicación integrada

El módulo permite enviar directamente desde el sistema:

```mermaid
sequenceDiagram
    participant A as Administrador
    participant S as Sistema
    participant E as Aparcero

    A->>S: Contrato próximo a vencer (5 días)
    S->>S: Genera alerta automática
    S->>A: Notificación en dashboard
    A->>S: Aprobar envío de recordatorio
    S->>E: Email: "Su contrato CONT-002 vence el 01/09/2024. Contacte al rancho para liquidación."
    E->>A: Respuesta por WhatsApp / correo
    A->>S: Registra respuesta en notas del aparcero
```

---

## Ventaja competitiva en la industria

> En el negocio ganadero, la selección de socios es crítica. Un aparcero irresponsable puede significar:
> - Alta mortalidad (pérdida directa de capital)
> - GDP bajo (engorda ineficiente, más tiempo = más gastos)
> - Conflictos legales al liquidar
>
> Este módulo permite:
> - **Elegir socios con base en datos**, no solo en recomendaciones verbales
> - Tener todos los **documentos legales al alcance** para cualquier trámite
> - **Comunicarse formalmente** con respaldo documental de cada intercambio
> - Construir una **red de proveedores y compradores** verificados y confiables
> - Presentar un **directorio profesional** ante instituciones financieras y sanitarias
