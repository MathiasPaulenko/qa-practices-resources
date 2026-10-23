# Pruebas de APIs SOAP con Postman — Companion

Fixtures ejecutables para la guía de QAPractices [Pruebas de APIs SOAP con Postman](https://qapractices.com/es/documentation/soap-api-testing-postman/).

La colección llama a `NumberConversion` en `www.dataaccess.com`, un servicio demo SOAP público y gratuito, así que cada ejemplo corre de punta a punta sin backend propio. Cambia el endpoint y la operación por tu WSDL de staging cuando estés listo.

## Archivos

| Archivo | Qué es |
|---|---|
| `numberconversion-soap.postman_collection.json` | Colección Postman v11: camino feliz con assertions xml2Json, un request que provoca fault y una plantilla WS-Security UsernameToken |
| `soap-demo.postman_environment.json` | Environment con `ubiNum`, `soap_endpoint` y credenciales de relleno |
| `run-newman.sh` | Ejecución con Newman 6.x, reporters `cli,junit` y exportación JUnit |

## Uso

### En Postman

1. Importa `numberconversion-soap.postman_collection.json` (**File → Import → File**).
2. Importa `soap-demo.postman_environment.json` y selecciónalo como environment activo.
3. Ejecuta **NumberToWords — happy path**. Los cinco tests deberían pasar.
4. Ejecuta **NumberToWords — missing element triggers fault** para ver un `soap:Fault` validado correctamente.

### Con Newman 6.x

```bash
./run-newman.sh
```

El reporte JUnit queda en `results/soap-tests.xml`, listo para el reporting de tests de Jenkins, GitHub Actions o Azure DevOps. Para integrarlo en tu pipeline, ejecuta el script como paso después del deploy de tu servicio.

### Ejecuciones data-driven

Crea un CSV con una columna `ubiNum` y pásalo a Newman:

```bash
newman run numberconversion-soap.postman_collection.json \
  --environment soap-demo.postman_environment.json \
  --iteration-data boundary-values.csv
```

El pre-request script lee cada fila con `pm.iterationData`.

## Notas

- `{{soap_username}}` y `{{soap_password}}` vienen como `replace-me` — el servicio demo los ignora. Apunta `soap_endpoint` a tu servicio y completa credenciales reales en un environment privado, nunca en este archivo.
- Para servicios SOAP 1.2 cambia `Content-Type` a `application/soap+xml` y mueve el action al content type — mira el FAQ de la guía.
