# 📋 Módulo 3 — Contratos de Aparcería
> **AparceríaPro** · Documentación técnica y funcional

---

## ¿Qué es la Aparcería Ganadera?

La **aparcería pecuaria** es un contrato en el que el dueño del capital (animales, tierra, recursos) entrega ganado a un aparcero para que lo cuide, críe o engorde, a cambio de dividir los beneficios según lo pactado. Está regulada en México por el **Código Agrario** y el **Código Civil Federal (Art. 2741-2766)**.

Existen dos tipos principales:
- **Aparcería de Cría**: el aparcero cuida los vientres, y las crías se reparten al nacimiento o al destete
- **Aparcería de Engorda**: el aparcero alimenta y cuida el ganado hasta el peso de mercado; la utilidad se divide al vender

---

## Campos del Contrato

| Campo | Tipo | Descripción |
|---|---|---|
| Número de contrato | Texto único | Folio interno (ej. CONT-2024-001) |
| Tipo de aparcería | Enum | Cría / Engorda / Mixta |
| Aparcero | FK → Aparcero | Quien recibe el ganado |
| Propietario | FK → Rancho | Quien entrega el ganado |
| Fecha de inicio | Fecha | Inicio del contrato |
| Fecha de fin estimada | Fecha | Plazo acordado |
| Animales incluidos | Lista FK → Animal | Aretes específicos |
| División de utilidades | Texto | Ej: 50/50, 60/40, 70/30 |
| Gastos a cargo de | Enum | Aparcero / Propietario / Compartidos |
| Precio de referencia kg | Decimal | Para calcular valor en pie |
| Peso de entrega inicial | Decimal (kg) | Peso total al iniciar |
| Peso mínimo de venta | Decimal (kg) | Peso acordado para vender |
| Cláusulas especiales | Texto libre | Mortalidad, enfermedades, seguros |
| Estado | Enum | Borrador / Activo / Suspendido / Finalizado |
| Firma del aparcero | Booleano | Acuse digital |
| Firma del propietario | Booleano | Acuse digital |
| Notario / Testigos | Texto | Opcional para contratos formales |

---

## Diagrama de estados de un Contrato

```mermaid
stateDiagram-v2
    [*] --> Borrador : Se captura el contrato
    Borrador --> Revision : Enviado para revisión
    Revision --> Borrador : Requiere correcciones
    Revision --> Activo : Ambas partes firman
    Activo --> Suspendido : Problema durante vigencia
    Suspendido --> Activo : Resolución del problema
    Activo --> En_Liquidacion : Se alcanza fecha fin o peso meta
    En_Liquidacion --> Finalizado : Liquidación aceptada y pagada
    En_Liquidacion --> Disputado : Desacuerdo en montos
    Disputado --> Finalizado : Resolución negociada
    Finalizado --> [*]
```

---

## Flujo completo de un contrato de engorda

```mermaid
flowchart TD
    A([Inicio: Acuerdo verbal entre partes]) --> B[Propietario captura contrato en sistema]
    B --> C[Selecciona animales del inventario]
    C --> D[Define términos: división, plazo, gastos]
    D --> E[Sistema genera PDF del contrato]
    E --> F[Aparcero firma / acepta digitalmente]
    F --> G[Contrato ACTIVO — animales marcados como 'En Aparcería']
    G --> H[Aparcero registra pesajes periódicos]
    H --> I{¿Se alcanzó peso meta o fecha fin?}
    I -- No --> H
    I -- Sí --> J[Sistema calcula utilidad bruta]
    J --> K[Resta: gastos veterinarios, alimentación, transporte]
    K --> L[Calcula utilidad neta]
    L --> M[Aplica división pactada: ej. 60/40]
    M --> N[Sistema genera liquidación detallada]
    N --> O{¿Aparcero acepta liquidación?}
    O -- Sí --> P[Se registra pago / transferencia]
    O -- No --> Q[Entra en proceso de disputa]
    P --> R[✅ Contrato FINALIZADO — animales regresan o salen del inventario]
    Q --> R
```

---

## Cálculo de liquidación de aparcería de engorda

```mermaid
flowchart LR
    A[Peso final total: 5,100 kg] --> C[Valor bruto: 5100 × $65 = $331,500]
    B[Precio kg en pie: $65] --> C
    C --> D[Gastos veterinarios: $8,200]
    D --> E[Alimentación extra: $15,000]
    E --> F[Transporte a rastro: $3,500]
    F --> G[Utilidad neta: $304,800]
    G --> H{División 60/40}
    H --> I[Propietario: $182,880]
    H --> J[Aparcero: $121,920]
```

---

## Diagrama entidad-relación del Contrato

```mermaid
erDiagram
    CONTRATO {
        string id PK
        string tipo
        date fecha_inicio
        date fecha_fin
        string division_pct
        string estado
        decimal monto_total
        decimal utilidad_calculada
    }

    APARCERO {
        string id PK
        string nombre
        string rfc
        string domicilio
    }

    ANIMAL {
        string id PK
        float peso_ingreso_contrato
        float peso_salida_contrato
    }

    GASTO_CONTRATO {
        string id PK
        string concepto
        decimal monto
        string a_cargo_de
        date fecha
    }

    LIQUIDACION {
        string id PK
        date fecha_calculo
        decimal utilidad_bruta
        decimal total_gastos
        decimal utilidad_neta
        decimal pago_aparcero
        decimal pago_propietario
        boolean firmada
    }

    CONTRATO ||--|{ ANIMAL : "incluye"
    CONTRATO }|--|| APARCERO : "firmado con"
    CONTRATO ||--|{ GASTO_CONTRATO : "acumula"
    CONTRATO ||--|| LIQUIDACION : "genera"
```

---

## Tipos de división y cómo impactan la utilidad

| Modalidad | Propietario | Aparcero | Cuándo usarla |
|---|---|---|---|
| 50/50 | 50% | 50% | Aparcero aporta tierra + mano de obra + alimentación |
| 60/40 | 60% | 40% | Propietario aporta más capital o ganado fino |
| 70/30 | 70% | 30% | Aparcero solo da mano de obra, todo lo demás es del propietario |
| Variable | Negociado | Negociado | Por metas de peso, crías nacidas, mortalidad cero |

---

## Ventaja competitiva en la industria

> Este módulo digitaliza lo que en el campo se hace en "acuerdos de palabra" o en hojas sueltas, generando:
> - **Contratos con validez documental** (PDF firmado, con fecha y condiciones)
> - **Liquidaciones transparentes y auditables** que evitan conflictos entre socios
> - **Historial por aparcero**: quién ha sido rentable, quién ha tenido pérdidas
> - **Alertas automáticas** cuando se acerca la fecha de vencimiento o el peso meta
> - Base para acceder a **financiamiento bancario** (los contratos formales son garantía)
