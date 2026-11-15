# Plantilla de Matriz de Testing de Mobile Deep Link — Companion

Archivos independientes de la [Plantilla de Matriz de Testing de Mobile Deep Link](https://qapractices.com/es/templates/mobile-deep-link-testing-matrix-template/) de QAPractices. Copia la matriz en blanco a tu wiki, Notion o herramienta de gestión de tests y empieza a completar filas — sin copy-paste desde el navegador.

## Archivos

| Archivo | Qué es |
|---|---|
| `deep-link-testing-matrix.md` | La matriz en blanco: detalles de deep link, universal links, app links, custom URI scheme, deferred links, fallback, routing multiplataforma, analytics, tracking de defectos y sign-off |
| `deep-link-testing-matrix-sample.md` | La misma matriz completada para una app de e-commerce ficticia (`shop.example.io`, Branch para deferred links) |
| `deep-link-commands.sh` | Los comandos `adb` y `xcrun simctl` usados para lanzar deep links y comprobar la verificación de dominio en Android, con comentarios |

## Uso

1. Completa la tabla **Detalles de Deep Link** con el nombre de tu app, tipos de link y dominios.
2. Reemplaza las URLs de `example.com` y el esquema `myapp://` por tus rutas reales.
3. Prueba cada fila en los tres estados de la app: primer plano, segundo plano y sin instalar.
4. Usa `deep-link-commands.sh` como punto de partida para las verificaciones manuales en dispositivos reales.

## Relacionados

- [Plantilla de Matriz de Testing de Mobile Deep Link](https://qapractices.com/es/templates/mobile-deep-link-testing-matrix-template/) — la plantilla completa con checklists, mejores prácticas y FAQ
- [Casos de Test de Deep Links y Universal Links](https://qapractices.com/es/test-cases/deep-link-universal-link-testing/) — casos de test ejecutables sobre los mismos escenarios
