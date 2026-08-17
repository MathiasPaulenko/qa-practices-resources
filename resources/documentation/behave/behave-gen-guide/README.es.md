# Ejemplo de BDD generado con behave-gen

Esta carpeta contiene un proyecto Behave BDD ejecutable que fue creado con [behave-gen](https://github.com/MathiasPaulenko/behave-gen) y refleja el ejemplo de la guía de QAPractices [Scaffolding de Proyectos Behave con behave-gen](https://qapractices.com/es/documentation/behave-gen-guide/).

Muestra el resultado de `behave-gen init`, `behave-gen add feature` y `behave-gen add steps --lib auth`. El feature de marcador que genera `behave-gen` fue reemplazado por un `login.feature` real que usa la librería de steps de autenticación.

## Estructura del proyecto

```text
inventory-bdd/
├── README.md
├── pyproject.toml
├── behave.toml
├── environment.py
└── features/
    ├── login.feature
    └── steps/
        └── auth_steps.py
```

## Qué demuestra

- `pyproject.toml` y `behave.toml` vienen de `behave-gen init`.
- `environment.py` contiene los hooks de ciclo de vida vacíos generados por `behave-gen`.
- `features/login.feature` reemplaza el placeholder con tres escenarios concretos sobre autenticación de sesión.
- `features/steps/auth_steps.py` se agregó con `behave-gen add steps --lib auth` y provee helpers de sesión en memoria.

## Correr localmente

```bash
cd inventory-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
behave
```

Los tres escenarios deberían pasar.

## Regenerar desde cero

```bash
pip install behave-gen
behave-gen init inventory-bdd
cd inventory-bdd
behave-gen add feature login
behave-gen add steps --lib auth
```

Luego reemplazá `features/login.feature` por el archivo feature de esta carpeta.
