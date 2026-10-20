# Pruebas de Campañas de Email Marketing — Compañero Ejecutable

Script de Node sin dependencias que cubre las verificaciones mecánicas del [Checklist de Pruebas de Campañas de Email Marketing](https://qapractices.com/es/checklists/email-marketing-campaign-testing-checklist/): merge tags sin resolver, enlaces sin UTM, alt text faltante, clipping de Gmail y unsubscribe ausente.

## Contenido

| Archivo | Propósito |
|---|---|
| `check-email-html.js` | Verificaciones estáticas pre-envío sobre el HTML exportado |
| `meta.json` | Metadata del recurso |

## Requisitos

- Node.js 20+ — sin dependencias.

## Uso

```bash
node check-email-html.js campaign-export.html
node check-email-html.js campaign-export.html --utm-required=utm_campaign,utm_source
```

Salida de ejemplo:

```text
  unresolved merge tag: {{first_name}} (line 42)
  link missing utm_campaign: https://shop.example.com/promo (line 88)
  img without alt: hero-banner.png (line 15)
  HTML size 104 KB — Gmail clips at 102 KB and can cut the CTA or footer links

4 issue(s) — fix before sending.
```

## Qué verifica

| Verificación | Por qué importa |
|---|---|
| Merge tags `{{x}}`, `*|X|*`, `%x%` | Los tokens sin fallback salen como texto literal |
| UTM requeridos en enlaces externos | Los clics se atribuyen a la campaña equivocada o a ninguna |
| `<img>` sin alt | Contexto roto con imágenes deshabilitadas + fallo de accesibilidad |
| HTML > 102 KB | Gmail recorta el mensaje — a menudo justo el CTA |
| Enlace de unsubscribe | Requisito legal y prevención de quejas de spam |
| Archivo `.txt` hermano (plain text) | Algunos clientes y filtros de spam lo esperan |

## Qué no verifica

El renderizado entre clientes, el spam score y la entregabilidad real requieren envíos reales (Litmus, Email on Acid, seed lists). Este script cubre solo lo que una pasada estática sobre el HTML exportado puede demostrar.
