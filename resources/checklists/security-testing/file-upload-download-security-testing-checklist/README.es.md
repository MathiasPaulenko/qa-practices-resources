# Checklist de Seguridad de Subida y Descarga de Archivos — Companion

Archivos companion del [Checklist de Seguridad de Subida y Descarga de Archivos](https://qapractices.com/es/checklists/file-upload-download-security-testing-checklist).

## Contenido

| Archivo | Descripción |
|---|---|
| `upload-payloads.csv` | 20 payloads adversariales de subida/descarga — bypass de extensión, null bytes, spoofing de MIME, magic bytes, path traversal, zip slip, XSS en SVG/HTML, EICAR, autorización de descarga |

## Uso

Importa el CSV en tu herramienta de gestión de tests o alimenta un bucle de script:

```bash
# Enviar cada payload de traversal al endpoint de descarga
tail -n +2 upload-payloads.csv | grep traversal | cut -d, -f3 | while read p; do
  curl -s -o /dev/null -w "$p -> %{http_code}\n" "https://staging.example.io/download?file=$p"
done
```

Esperado: cada fila de payload mapea a un rechazo, sanitización o servicio seguro — nunca a un archivo peligroso aceptado.
