# Companion del Simulacro ISTQB Foundation Level

Recurso complementario de la guía [Preguntas de Examen ISTQB Foundation Level](https://qapractices.com/es/documentation/istqb-foundation-level-exam-questions). Las mismas 40 preguntas de práctica CTFL en formato legible por máquina para repasarlas en tus propias herramientas en lugar de hacer scroll en la web.

## Archivos

| Archivo | Propósito |
| ------- | --------- |
| `src/istqb-foundation-mock-exam.csv` | Las 40 preguntas: capítulo del syllabus, número, texto de la pregunta, opciones A-D, letra de la respuesta correcta y la explicación completa (por qué la opción correcta gana y por qué falla cada distractor). |

## Formato del CSV

Una fila por pregunta, UTF-8, separado por comas:

`chapter, question_number, question, option_a, option_b, option_c, option_d, correct_answer, explanation`

## Inicio rápido

- **Anki:** Archivo → Importar → selecciona el CSV y mapea los campos a Frente (pregunta + opciones) y Reverso (respuesta + explicación).
- **Quizlet/Kahoot:** importa el CSV y elige las columnas de pregunta, opciones y respuesta.
- **Puntuación en hoja de cálculo:** abre en Excel o Google Sheets, añade una columna `mi_respuesta` y puntúate por capítulo para detectar puntos débiles antes de un segundo simulacro cronometrado.

## Requisitos

Ninguno. El CSV abre en Excel, Google Sheets, Anki, Quizlet o cualquier LMS que acepte importación CSV.
