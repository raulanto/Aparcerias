# 🐄 Módulo 2 — Registro de Ganado (Inventario)
> **AparceríaPro** · Documentación técnica y funcional

---

## ¿Qué es y para qué sirve?

El Registro de Ganado es el **corazón del sistema**: sin un inventario preciso, no es posible calcular utilidades reales, liquidar contratos correctamente ni tomar decisiones de compra/venta. Este módulo funciona como el expediente clínico y comercial de cada animal.

En México, la trazabilidad del ganado es exigida por la **SENASICA** (Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria) y es requisito para exportar o ingresar a ciertos mercados. Un sistema de registro completo da ventaja legal y comercial.

---

## Entidades principales

### Animal (ficha individual)

| Campo | Tipo | Descripción |
|---|---|---|
| ID / Arete | Texto único | Identificador físico del animal (arete oficial SENASICA) |
| Especie | Catálogo | Bovino, Ovino, Caprino, Equino, Porcino |
| Raza | Catálogo | Angus, Hereford, Simmental, Charolais, etc. |
| Sexo | Enum | Macho / Hembra / Castrado |
| Fecha de nacimiento | Fecha | Para cálculo automático de edad |
| Peso de ingreso | Decimal (kg) | Peso al momento del registro |
| Peso actual | Decimal (kg) | Actualizable en cada revisión |
| Color / Señas | Texto | Descripción física para identificación rápida |
| Procedencia | Texto | Rancho, ejido o productor de origen |
| Aparcero asignado | FK → Aparcero | Dueño o co-propietario del animal |
| Contrato asociado | FK → Contrato | Si aplica aparcería |
| Propósito | Enum | Cría, Engorda, Leche, Doble propósito, Reproductor |
| Estado sanitario | Enum | Sano, En tratamiento, Cuarentena, Baja |
| Fecha de ingreso | Fecha | Al inventario del rancho |
| Valor de compra | Decimal (MXN) | Costo de adquisición |
| Valor estimado actual | Decimal (MXN) | Calculado por peso × precio kg en pie |
| Fotografía | Imagen | Opcional, para identificación visual |
| Notas | Texto libre | Observaciones del administrador |

---

## Diagrama de ciclo de vida de un animal

```mermaid
stateDiagram-v2
    [*] --> Ingreso : Compra o nacimiento
    Ingreso --> Inventario_Activo : Registro completo
    Inventario_Activo --> En_Aparceria : Asignado a contrato
    Inventario_Activo --> En_Tratamiento : Problema sanitario
    En_Aparceria --> Inventario_Activo : Contrato finaliza
    En_Tratamiento --> Inventario_Activo : Recuperado
    En_Tratamiento --> Baja_Sanitaria : Muerte / sacrificio obligatorio
    En_Aparceria --> Venta : Se liquida en contrato
    Inventario_Activo --> Venta : Venta directa
    Venta --> [*] : Sale del inventario
    Baja_Sanitaria --> [*] : Sale del inventario
```

---

## Diagrama de relaciones del Animal con otros módulos

```mermaid
erDiagram
    ANIMAL {
        string id PK
        string especie
        string raza
        string sexo
        date fecha_nacimiento
        float peso_actual
        string estado_sanitario
        decimal valor_compra
        decimal valor_estimado
    }

    APARCERO {
        string id PK
        string nombre
        string tipo
        string telefono
    }

    CONTRATO {
        string id PK
        string tipo
        date fecha_inicio
        date fecha_fin
        string division_utilidades
    }

    TRANSACCION {
        string id PK
        string tipo
        decimal monto
        date fecha
    }

    REVISION_SANITARIA {
        string id PK
        date fecha
        string diagnostico
        string tratamiento
        string veterinario
    }

    PESAJE {
        string id PK
        date fecha
        float peso_kg
        float ganancia_diaria
    }

    ANIMAL ||--o{ PESAJE : "tiene registros de"
    ANIMAL ||--o{ REVISION_SANITARIA : "tiene historial de"
    ANIMAL ||--o| APARCERO : "pertenece a"
    ANIMAL ||--o| CONTRATO : "está bajo"
    ANIMAL ||--o{ TRANSACCION : "genera"
```

---

## Flujo de registro de un animal nuevo

```mermaid
flowchart TD
    A([Inicio: Nuevo animal]) --> B[Escanear / ingresar número de arete]
    B --> C{¿Arete ya existe?}
    C -- Sí --> D[❌ Error: arete duplicado]
    C -- No --> E[Capturar datos básicos: especie, raza, sexo, fecha nacimiento]
    E --> F[Registrar peso de ingreso]
    F --> G[Asignar propósito: cría / engorda / leche]
    G --> H{¿El animal viene de un contrato de aparcería?}
    H -- Sí --> I[Asociar a aparcero y contrato correspondiente]
    H -- No --> J[Marcar como propiedad directa del rancho]
    I --> K[Registrar valor de compra o valor pactado]
    J --> K
    K --> L[Tomar fotografía opcional]
    L --> M[Guardar en inventario activo]
    M --> N[✅ Animal registrado — Dashboard actualizado]
```

---

## Control de pesajes (ganancia de peso)

El seguimiento del peso es clave para determinar la **rentabilidad real de la engorda**:

```mermaid
sequenceDiagram
    participant U as Usuario
    participant S as Sistema
    participant BD as Base de datos

    U->>S: Registra pesaje de animal MX-003 (510 kg)
    S->>BD: Consulta peso anterior (480 kg, hace 30 días)
    BD-->>S: Peso anterior encontrado
    S->>S: Calcula GDP = (510-480) / 30 = 1.0 kg/día
    S->>BD: Guarda nuevo pesaje con GDP
    S-->>U: Muestra progreso: +30 kg en 30 días (GDP: 1.0 kg/día)
    S->>S: Actualiza valor estimado = 510 × $65/kg = $33,150
```

---

## Historial sanitario

Cada animal debe tener expediente de:
- Vacunas aplicadas (fecha, tipo, dosis, veterinario)
- Desparasitaciones internas y externas
- Tratamientos médicos (diagnóstico, medicamento, dosis, duración)
- Cirugías o procedimientos (descorne, castración, marcaje)
- Mortalidad o bajas (causa, fecha, peso final)

---

## Ventaja competitiva en la industria

> Con este módulo, el rancho puede:
> - **Acreditar trazabilidad** ante compradores, exportadores y autoridades (SENASICA / TIF)
> - Calcular automáticamente la **ganancia diaria de peso (GDP)**
> - Identificar animales **improductivos** que consumen recursos sin generar utilidad
> - Generar **constancias de existencia** para trámites legales y crediticios
> - Comparar el desempeño de razas y propósitos entre temporadas
