# Automatización de Tests Mobile con Maestro — Companion

Proyecto companion para [Automatización de Tests Mobile con Maestro: iOS y Android](https://qapractices.com/es/documentation/mobile-test-automation-with-maestro/).

## Requisitos

- Maestro CLI 2.8.0
- Java 11+
- Node.js 20 LTS (para CI)
- Xcode (para simulador de iOS) o Android Studio (para emulador de Android)

## Instalar Maestro

```bash
curl -Ls "https://get.maestro.mobile.dev" | bash
export PATH="$PATH:$HOME/.maestro/bin"
maestro --version
```

## Archivos

| Archivo | Propósito |
| --- | --- |
| `flows/home-screen.yaml` | Flow básico de launch + search |
| `flows/profile-flow.yaml` | Subflow de login + navegación a perfil |
| `flows/checkout-flow.yaml` | Lógica condicional para carrito vacío + checkout |
| `subflows/login.yaml` | Subflow de login reutilizable con env vars |
| `.github/workflows/mobile-tests.yml` | Workflow de GitHub Actions CI para simulador macOS |

## Correr un Flow

```bash
maestro test flows/home-screen.yaml
```

## Correr Todos los Flows

```bash
maestro test flows/
```

## Correr con Variables de Entorno

```bash
EMAIL="qa-tester@qapractices.test" PASSWORD="TestPass123!" maestro test flows/profile-flow.yaml
```

## Integración CI

El workflow de GitHub Actions incluido corre todos los flows en `macos-latest` con un simulador iPhone 15. Sube screenshots y logs como artefactos en caso de falla.

## Recurso Relacionado

- [Automatización de Tests Mobile con Maestro](https://qapractices.com/es/documentation/mobile-test-automation-with-maestro/)
- [Tutorial de Testing Mobile con Appium](https://qapractices.com/es/documentation/appium-mobile-testing-tutorial/)
- [Checklist de Testing de Apps Mobile](https://qapractices.com/es/checklists/mobile-app-testing-checklist/)
