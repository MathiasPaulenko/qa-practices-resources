# SonarQube vs CodeClimate vs ESLint Security — Companion

This companion provides runnable files for the [SonarQube vs CodeClimate vs ESLint Security](https://qapractices.com/documentation/sonarqube-vs-codeclimate-vs-eslint-security) guide.

## Files

| File | Purpose |
|------|---------|
| `configs/sonar-project.properties` | SonarQube project configuration with quality gate |
| `configs/.codeclimate.yml` | CodeClimate configuration with ESLint and SonarJava plugins |
| `configs/eslint.config.js` | ESLint flat config with eslint-plugin-security |
| `configs/.eslintrc.json` | Legacy ESLint config with eslint-plugin-security |
| `.github/workflows/quality.yml` | GitHub Actions workflow running all three tools on PR |

## Quick Start

```bash
# Copy configs to your project
cp configs/sonar-project.properties /your-project/
cp configs/.codeclimate.yml /your-project/
cp configs/eslint.config.js /your-project/

# Run ESLint Security locally
npx eslint src/ --max-warnings 0

# Run the CI workflow locally with act
act -W .github/workflows/quality.yml
```

## CI Integration

The included GitHub Actions workflow runs ESLint Security, CodeClimate, and SonarQube in parallel on every pull request. Each job must pass before the PR can merge.