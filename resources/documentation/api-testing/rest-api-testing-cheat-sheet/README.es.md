# REST API Testing: Cheat Sheet — Companion

Companion ejecutable del [Cheat Sheet de REST API Testing](https://qapractices.com/es/documentation/rest-api-testing-cheat-sheet/) en QAPractices.com.

## Contenido

- `requests.http` — la pasada completa por método del cheat sheet: GET (con filtros y un 404 negativo), POST, PUT, PATCH, DELETE, HEAD, OPTIONS, tres variantes de headers de autenticación y cuatro sondas de seguridad (sin autenticación, SQLi, XSS, path traversal).

## Cómo ejecutarlo

Cualquier cliente `.http` sirve:

- **VS Code** — instala la extensión REST Client, abre `requests.http` y pulsa "Send Request" sobre cada bloque.
- **JetBrains** — abre el archivo y ejecuta cada request desde el icono del margen.
- **Postman** — importa el archivo (Postman lee colecciones `.http`/`.rest`).
- **curl** — cada bloque equivale a un comando curl; la versión bash de la pasada CRUD está en la sección "Ejemplo Práctico" del artículo.

## Destino

Las peticiones apuntan por defecto a `https://jsonplaceholder.typicode.com`, una API pública de pruebas que acepta escrituras sin persistirlas. Cambia `@baseUrl` a tu API de staging para correr la misma pasada contra un servicio real — las sondas de seguridad solo tienen sentido contra una API propia.
