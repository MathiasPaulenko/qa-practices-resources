Skill Assessment
- Manual testing: 4/5 — strong exploratory habits, solid test design
- API testing: 3/5 — comfortable with Postman collections, no contract testing
- Automation: 2/5 — records-and-edits Selenium scripts, no framework design
- CI/CD: 2/5 — uses Jenkins jobs others configured
- Performance / Security: 1/5
- Leadership: 2/5 — informally onboards new testers

Gap Analysis (Senior QA / SDET target)
Critical: automation framework design (2→4), CI/CD pipeline ownership (2→4)
High: programming depth in Java or a second language, code review skills
Medium: performance testing basics, mentoring

Learning Path
- Month 1-2: Playwright fundamentals (Java or TypeScript). Search "Playwright
  official course" — the free Microsoft docs track is enough. Rebuild 5 of your
  existing Selenium tests in Playwright.
- Month 3-4: Framework design — Page Object Model, fixtures, parallelization.
  Book: "Selenium Design Patterns and Best Practices" (Dima Kovalenko) for
  concepts that transfer to Playwright.
- Month 5-6: CI/CD ownership — move your suite into GitHub Actions with
  sharding and HTML reports. Read the Actions docs, not a paid course.

Certification
- ISTQB CTAL Test Automation Engineer (CTAL-TAE) — ~40 study hours, ~USD 250
  exam fee. Justified: it formalizes the framework design knowledge you're
  building anyway. Skip CEH and CKA for this profile.

6-Month Milestones
- Month 2: Playwright suite running locally with 10 migrated tests
- Month 4: Framework in team repo, reviewed by a senior dev
- Month 6: Suite in CI on every PR; you presented it in a team demo
