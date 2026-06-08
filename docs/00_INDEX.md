# 🐄 AparceríaPro — Documentación General del Sistema
> Sistema de administración de aparcería y compra-venta de ganado

---

## Visión del sistema

**AparceríaPro** es una plataforma web diseñada para digitalizar y profesionalizar la administración del negocio ganadero en México. Atiende específicamente las necesidades de productores que operan bajo esquemas de **aparcería pecuaria**, donde la gestión de contratos, inventario y finanzas es compleja y actualmente se realiza en papel o sin ningún control formal.

---

## Módulos del sistema

| # | Módulo | Propósito principal | Usuarios clave |
|---|---|---|---|
| 1 | [Dashboard General](./01_DASHBOARD.md) | Centro de comando — KPIs y alertas en tiempo real | Dueño, administrador |
| 2 | [Registro de Ganado](./02_REGISTRO_GANADO.md) | Inventario individual de animales con trazabilidad completa | Administrador, vaquero |
| 3 | [Contratos de Aparcería](./03_CONTRATOS.md) | Gestión del ciclo completo de cada contrato | Administrador, aparcero |
| 4 | [Compra / Venta](./04_COMPRA_VENTA.md) | Registro de transacciones con cálculo de utilidad real | Administrador, contador |
| 5 | [Finanzas](./05_FINANZAS.md) | Estado de resultados, flujo de caja y control presupuestal | Dueño, contador |
| 6 | [Aparceros](./06_APARCEROS.md) | Directorio de socios con historial de desempeño | Administrador |
| 7 | [Reportes](./07_REPORTES.md) | Exportación de documentos para trámites, socios y auditorías | Todos |

---

## Arquitectura general del sistema

```mermaid
graph TB
    subgraph FRONTEND
        FE[Angular 20 — Web App]
    end

    subgraph BACKEND
        API[NestJS REST API]
        AUTH[Módulo Auth / JWT]
        NOTIF[Módulo Notificaciones]
        PDF_SVC[Servicio PDF]
    end

    subgraph BASE_DE_DATOS
        DB[(SQL Server)]
        STORAGE[Almacenamiento de archivos]
    end

    subgraph EXTERNOS
        SAT[API SAT — validación CFDI]
        SENASICA[SENASICA — trazabilidad]
        EMAIL[Servicio Email]
        SMS[WhatsApp / SMS]
    end

    FE <--> API
    API --> AUTH
    API --> NOTIF
    API --> PDF_SVC
    API <--> DB
    API --> STORAGE
    API --> SAT
    API --> SENASICA
    NOTIF --> EMAIL
    NOTIF --> SMS
```

---

## Diagrama de relación entre módulos

```mermaid
flowchart TD
    GAN[🐄 Registro de Ganado] -->|animales asignados| CON[📋 Contratos]
    GAN -->|animales vendidos| CV[↕ Compra/Venta]
    CV -->|ingresos y egresos| FIN[💰 Finanzas]
    CON -->|liquidaciones| FIN
    CON -->|socios vinculados| APA[👥 Aparceros]
    CV -->|contrapartes| APA
    GAN --> DASH[📊 Dashboard]
    FIN --> DASH
    CON --> DASH
    APA --> DASH
    GAN -->|datos| REP[📑 Reportes]
    CON -->|datos| REP
    FIN -->|datos| REP
    CV -->|datos| REP
    APA -->|datos| REP
```

---

## Flujo de negocio completo (de punta a punta)

```mermaid
sequenceDiagram
    participant D as Dueño del rancho
    participant A as Aparcero
    participant S as Sistema

    D->>S: Registra animales en inventario (Módulo Ganado)
    D->>S: Crea contrato de aparcería con división 60/40 (Módulo Contratos)
    S->>A: Envía PDF del contrato para firma
    A->>S: Firma digitalmente el contrato
    S->>S: Contrato ACTIVO — animales marcados "En Aparcería"

    loop Cada 30 días
        A->>S: Registra pesaje de los animales
        S->>S: Calcula GDP y actualiza valor estimado
        S->>D: Notificación con avance del lote
    end

    Note over D,S: Al alcanzar peso meta o fecha fin

    S->>S: Calcula utilidad neta (venta - compra - gastos)
    S->>S: Aplica división 60/40
    S->>D: Genera liquidación en PDF
    S->>A: Envía liquidación para revisión
    A->>S: Acepta liquidación
    D->>S: Registra pago de la parte del aparcero
    S->>S: Contrato FINALIZADO — animales VENDIDOS — Inventario actualizado
    S->>S: Actualiza KPIs en Dashboard y Finanzas
```

---

## Roles del sistema

| Rol | Permisos |
|---|---|
| **Administrador** | Acceso total a todos los módulos |
| **Dueño / Propietario** | Dashboard, Finanzas, Reportes (solo lectura en Ganado/Contratos) |
| **Capturista** | Registro de Ganado, Compra/Venta (sin eliminar) |
| **Contador** | Finanzas, Reportes, Compra/Venta (solo lectura) |
| **Aparcero** (portal externo) | Ver sus contratos, pesajes e historial propio |

---

## Stack tecnológico recomendado

| Capa | Tecnología | Justificación |
|---|---|---|
| Frontend | Angular 20 (Signals + Standalone) | Arquitectura moderna, rendimiento, ecosistema enterprise |
| Backend | NestJS + TypeORM | Modular, escalable, soporte SQL Server nativo |
| Base de datos | SQL Server / SQLite (dev) | Robustez para datos financieros, soporte ACID |
| Autenticación | JWT + Refresh tokens | Seguridad estándar para APIs |
| PDF | Puppeteer / PDFKit | Generación de documentos legales con firma |
| Almacenamiento | S3 / Azure Blob | Documentos, contratos, fotos de ganado |
| Despliegue | PM2 + Nginx + Angular SSR | Producción estable y SEO-ready |

---

## Hoja de ruta de desarrollo sugerida

```mermaid
gantt
    title Roadmap AparceríaPro
    dateFormat  YYYY-MM-DD
    section Fase 1 - Core
    Módulo Ganado (inventario)       :a1, 2024-07-01, 21d
    Módulo Aparceros                 :a2, after a1, 14d
    Módulo Contratos                 :a3, after a2, 21d
    section Fase 2 - Comercial
    Módulo Compra/Venta              :b1, after a3, 14d
    Módulo Finanzas                  :b2, after b1, 21d
    section Fase 3 - Inteligencia
    Dashboard con KPIs               :c1, after b2, 14d
    Módulo Reportes y PDF            :c2, after c1, 21d
    section Fase 4 - Avanzado
    Portal externo para aparceros    :d1, after c2, 21d
    Integración SENASICA / SAT       :d2, after d1, 30d
```
