# ↕ Módulo 4 — Compra / Venta de Ganado
> **AparceríaPro** · Documentación técnica y funcional

---

## ¿Qué es y para qué sirve?

Este módulo registra **todas las transacciones comerciales** que involucran movimiento de animales: compras al mercado, ventas a rastros o empresas, canje entre socios, subasta, etc. Es la fuente principal del flujo de caja del negocio y el historial que permite calcular el **costo real de producción** y la **utilidad por lote**.

En la industria ganadera, muchas pérdidas ocurren porque no se documentan correctamente los costos de adquisición y los gastos asociados (flete, cuarentena, vacunas de ingreso), inflando artificialmente las utilidades al vender.

---

## Campos de una Transacción

### Compra

| Campo | Tipo | Descripción |
|---|---|---|
| Folio | Texto único | Ej: CMP-2024-001 |
| Fecha | Fecha/hora | Momento exacto de la transacción |
| Tipo | Enum | Compra directa / Subasta / Canje / Donación |
| Vendedor | Texto / FK → Aparcero | Quién vende |
| Animales adquiridos | Lista FK → Animal | Aretes específicos o lote |
| Peso total de compra | Decimal (kg) | Peso en báscula al comprar |
| Precio por kg | Decimal (MXN) | Precio acordado |
| Monto total | Decimal (MXN) | Peso × precio/kg |
| Gastos adicionales | Lista de conceptos | Flete, cuarentena, vacunas, comisión |
| Costo total real | Decimal (MXN) | Monto + gastos adicionales |
| Forma de pago | Enum | Efectivo / Transferencia / Cheque / Crédito |
| Comprobante fiscal | Booleano + archivo | CFDI / factura adjunta |
| Notas | Texto libre | Observaciones |

### Venta

| Campo | Tipo | Descripción |
|---|---|---|
| Folio | Texto único | Ej: VTA-2024-001 |
| Fecha | Fecha/hora | Momento de la venta |
| Tipo | Enum | Rastro / Directo a carnicería / Exportación / Subasta |
| Comprador | Texto | Razón social o nombre |
| Animales vendidos | Lista FK → Animal | Aretes específicos |
| Peso total de venta | Decimal (kg) | Peso en báscula al vender |
| Precio por kg | Decimal (MXN) | Precio de venta |
| Ingresos brutos | Decimal (MXN) | Peso × precio/kg |
| Deducciones | Lista | Comisiones, transporte, impuestos |
| Ingreso neto | Decimal (MXN) | Ingreso bruto - deducciones |
| Contrato relacionado | FK → Contrato | Si es liquidación de aparcería |
| Utilidad por animal | Decimal (MXN) | Ingreso neto - costo real de compra |

---

## Diagrama de flujo de una Compra

```mermaid
flowchart TD
    A([Decisión de compra en feria/rancho]) --> B[Negociación de precio por kg]
    B --> C[Pesaje en báscula — registrar kg]
    C --> D[Capturar datos del vendedor]
    D --> E[Registrar animales individualmente por arete]
    E --> F[¿Se conocen los aretes?]
    F -- Sí --> G[Asociar aretes existentes o crear nuevos]
    F -- No --> H[Registrar como lote — asignar aretes al llegar al rancho]
    G --> I[Registrar gastos adicionales]
    H --> I
    I --> J[Flete de traslado]
    I --> K[Vacunas de ingreso]
    I --> L[Cuarentena]
    J & K & L --> M[Sistema calcula costo real total]
    M --> N[¿Se adjunta CFDI / factura?]
    N -- Sí --> O[Subir comprobante fiscal]
    N -- No --> P[Marcar como compra sin factura]
    O & P --> Q[✅ Transacción registrada — Inventario actualizado]
```

---

## Diagrama de flujo de una Venta

```mermaid
flowchart TD
    A([Decisión de venta]) --> B{¿Es liquidación de contrato?}
    B -- Sí --> C[Ir a Módulo Contratos → Liquidación]
    B -- No --> D[Seleccionar animales a vender del inventario]
    D --> E[Registrar peso en báscula]
    E --> F[Capturar precio por kg negociado]
    F --> G[Sistema calcula ingreso bruto]
    G --> H[Registrar deducciones: flete, comisión, impuesto]
    H --> I[Sistema calcula ingreso neto]
    I --> J[Sistema recupera costo real de compra por animal]
    J --> K[Sistema calcula UTILIDAD REAL = Ingreso neto - Costo real]
    K --> L{¿Utilidad positiva?}
    L -- Sí --> M[✅ Venta rentable]
    L -- No --> N[⚠️ Venta con pérdida — notificar al administrador]
    M & N --> O[Registrar forma de cobro y adjuntar CFDI]
    O --> P[Marcar animales como VENDIDOS — salen del inventario]
    P --> Q[Dashboard actualizado]
```

---

## Cálculo de utilidad real por animal

```mermaid
flowchart LR
    A["Costo de compra: $18,500"] --> E
    B["Gastos de ingreso: $1,200\n(vacunas + flete)"] --> E
    C["Alimentación extra: $3,400\n(90 días × $38/día)"] --> E
    D["Veterinaria: $800"] --> E
    E["Costo real total: $23,900"] --> G
    F["Ingreso neto de venta: $28,500\n(430 kg × $67/kg − comisión)"] --> G
    G{Utilidad real}
    G --> H["✅ Utilidad: +$4,600\n(19.2% de margen)"]
```

---

## Diagrama entidad-relación de la Transacción

```mermaid
erDiagram
    TRANSACCION {
        string id PK
        string tipo
        date fecha
        decimal monto_total
        decimal gastos_adicionales
        decimal costo_real_total
        string forma_pago
        boolean tiene_cfdi
    }

    ANIMAL {
        string id PK
        string arete
        float peso_transaccion
        decimal precio_kg
    }

    CONTRAPARTE {
        string id PK
        string nombre
        string rfc
        string tipo
    }

    GASTO_TRANSACCION {
        string id PK
        string concepto
        decimal monto
    }

    DOCUMENTO_FISCAL {
        string id PK
        string folio_cfdi
        string uuid_sat
        string archivo_xml
        string archivo_pdf
    }

    TRANSACCION ||--|{ ANIMAL : "involucra"
    TRANSACCION }|--|| CONTRAPARTE : "con"
    TRANSACCION ||--|{ GASTO_TRANSACCION : "tiene"
    TRANSACCION ||--o| DOCUMENTO_FISCAL : "genera"
```

---

## Indicadores clave del módulo

| Indicador | Fórmula | Para qué sirve |
|---|---|---|
| Margen por animal | (Venta neta − Costo real) / Costo real × 100 | Medir rentabilidad individual |
| GDP (Ganancia diaria de peso) | (Peso venta − Peso compra) / días | Evaluar eficiencia de la engorda |
| Costo por kg ganado | Gastos totales / (Peso venta − Peso compra) | Comparar lotes y razas |
| Precio promedio compra | Total pagado / kg total comprado | Referencia para negociar |
| Precio promedio venta | Total cobrado / kg total vendido | Referencia para negociar |
| ROI del lote | Utilidad / Inversión × 100 | Comparar entre lotes y temporadas |

---

## Ventaja competitiva en la industria

> El ganadero promedio **no sabe el costo real de producción** porque no suma los gastos de alimentación, veterinaria y transporte al precio de compra. Este módulo:
> - Calcula automáticamente el **costo de producción por animal**
> - Identifica **lotes y razas más rentables**
> - Genera evidencia de compra-venta para **trámites ante el SAT**
> - Detecta si una venta es rentable **antes de cerrar el trato**
> - Conecta directamente con los módulos de Finanzas y Contratos para coherencia total
