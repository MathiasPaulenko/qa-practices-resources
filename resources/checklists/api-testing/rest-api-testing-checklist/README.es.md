# Checklist de Pruebas de API REST — Companion

Companion ejecutable para la [Checklist de Pruebas de API REST](https://qapractices.com/es/checklists/rest-api-testing-checklist): un probador de contrato HTTP más una colección smoke para Newman.

## Archivos

| Archivo | Qué hace |
|---------|----------|
| `check_contract.py` | Sondea una ruta buscando violaciones de contrato: clases de estado incorrectas, cuerpos de error vacíos, `Allow` ausente, `PUT` no idempotente, `DELETE` repetido inseguro. Solo stdlib de Python, sin dependencias. |
| `sample_collection.json` | Esqueleto de colección Postman/Newman — happy path + `401` + `404` por ruta, con aserciones estado-primero. |

## Uso

```bash
# Sondeo de contrato contra un endpoint vivo
python check_contract.py --base http://localhost:8080 --route /users/1 \
    --token $TOKEN --methods GET,PUT,DELETE

# Smoke run con Newman
newman run sample_collection.json --env-var base_url=http://localhost:8080 --env-var token=$TOKE
