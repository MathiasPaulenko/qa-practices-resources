# Expresiones Regulares para Testing: Cheat Sheet — Companion

Archivos ejecutables de la [guía de Expresiones Regulares para Testing](https://qapractices.com/es/documentation/regex-for-testing-cheat-sheet/) en QAPractices.com.

## Contenido

| Archivo | Qué es |
|---|---|
| `src/patterns.txt` | Todos los patrones de la guía, organizados por sección, con notas de dialecto |
| `src/patterns.test.js` | Script de Node sin dependencias que ejecuta cada patrón de validación contra muestras positivas y negativas |

## Uso

```bash
node src/patterns.test.js    # imprime "12 patterns checked, 0 failure(s)"
```

Copia las líneas de patrón que necesites desde `patterns.txt` a tus aserciones.
Si adaptas un patrón, agrega una muestra correspondiente en `patterns.test.js`
para que el cambio quede verificado, no asumido.
