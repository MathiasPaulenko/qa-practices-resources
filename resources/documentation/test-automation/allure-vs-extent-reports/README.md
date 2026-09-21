# Allure vs Extent Reports — Companion

Companion for [Allure vs Extent Reports: Test Reporting Compared](https://qapractices.com/documentation/allure-vs-extent-reports/) on QAPractices.

The same login scenario (valid credentials + locked account) is implemented twice so you can compare setup cost, output format, and CI wiring side by side:

| Folder | Tool | Output |
|---|---|---|
| `allure/` | `allure-pytest` 2.x + Allure CLI | `allure-report/` web app (needs `allure generate`/`serve` or hosting) |
| `extent/` | ExtentReports 5.1.2 + JUnit 5 (Maven) | `extent-report.html` single self-contained file |
| `ci/` | GitHub Actions | Publishes both report formats as build artifacts |

## Run the Allure example

```bash
cd allure
pip install -r requirements.txt
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure serve allure-results   # live preview
```

Copy `categories.json` into `allure-results/` before `allure generate` to see custom failure categories (product defects vs test defects vs infrastructure issues).

## Run the ExtentReports example

```bash
cd extent
mvn test
# open extent/build/reports/extent-report.html
```

## What to compare

- **Setup cost**: Allure needs a CLI tool plus an adapter per framework; Extent is one dependency inside the JVM.
- **History**: keep `allure-results/history/` between runs for trends; Extent needs the self-hosted KLOV server.
- **Distribution**: an Extent HTML file attaches to an email or ticket; an Allure report needs `allure serve` or hosting.
- **Maintenance**: ExtentReports is sunset (last release 5.1.2, June 2024) in favor of ChainTest; Allure 3.x is actively developed.
