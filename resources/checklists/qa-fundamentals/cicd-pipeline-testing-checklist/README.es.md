# CI/CD Pipeline Testing Checklist — Companion

Este companion provee archivos ejecutables para el checklist [Checklist de CI/CD Pipeline](https://qapractices.com/es/checklists/cicd-pipeline-testing-checklist).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `workflows/test-and-deploy.yml` | Pipeline de GitHub Actions con stages de test y deploy |
| `workflows/gitlab-ci.yml` | Config de GitLab CI con stages de build, SAST y deploy |
| `tests/test_smoke.py` | Smoke test en Python para verificación post-deploy |

## Inicio Rápido

```bash
# GitHub Actions: push a main para disparar el pipeline
git push origin main

# GitLab CI: push para disparar el pipeline
git push origin main

# Correr smoke tests localmente
pip install requests
python tests/test_smoke.py
```