# SonarQube vs CodeClimate vs ESLint Security — Companion

Este companion provee archivos ejecutables para la guía [SonarQube vs CodeClimate vs ESLint Security](https://qapractices.com/es/documentation/sonarqube-vs-codeclimate-vs-eslint-security).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `configs/sonar-project.properties` | Configuración de proyecto SonarQube con quality gate |
| `configs/.codeclimate.yml` | Configuración de CodeClimate con plugins ESLint y SonarJava |
| `configs/eslint.config.js` | ESLint flat config con eslint-plugin-security |
| `configs/.eslintrc.json` | ESLint config legacy con eslint-plugin-security |
| `.github/workflows/quality.yml` | Workflow de GitHub Actions que corre las tres herramientas en PR |

## Inicio Rápido

```bash
# Copiar configs a tu proyecto
cp configs/sonar-project.properties /your-project/
cp configs/.codeclimate.yml /your-project/
cp configs/eslint.config.js /your-project/

# Correr ESLint Security localmente
npx eslint src/ --max-warnings 0

# Correr el workflow de CI localmente con act
act -W .github/workflows/quality.yml
```

## Integración CI

El workflow de GitHub Actions incluido corre ESLint Security, CodeClimate y SonarQube en paralelo en cada pull request. Cada job debe pasar antes de que el PR pueda mergear.