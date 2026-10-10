# ISTQB Foundation Level Mock Exam Companion

Companion resource for the [ISTQB Foundation Level Exam Practice Questions](https://qapractices.com/documentation/istqb-foundation-level-exam-questions) guide. The same 40 CTFL practice questions in machine-readable format so you can drill them in your own tools instead of scrolling a web page.

## Files

| File | Purpose |
| ---- | ------- |
| `src/istqb-foundation-mock-exam.csv` | All 40 questions: syllabus chapter, question number, question text, options A-D, correct answer letter and the full explanation (why the right option wins and why each distractor fails). |

## CSV format

One row per question, UTF-8, comma-separated:

`chapter, question_number, question, option_a, option_b, option_c, option_d, correct_answer, explanation`

## Quick Start

- **Anki:** File → Import → select the CSV, map fields to Front (question + options) and Back (correct answer + explanation).
- **Quizlet/Kahoot:** import the CSV and pick question/options/correct columns.
- **Spreadsheet scoring:** open in Excel or Google Sheets, add a `my_answer` column and score yourself per chapter to find weak spots before a second timed run.

## Requirements

None. The CSV opens in Excel, Google Sheets, Anki, Quizlet or any LMS that accepts CSV imports.
