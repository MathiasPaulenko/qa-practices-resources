# behave-steplib Example

Runnable example for the [Behave Step Library Guide](https://qapractices.com/documentation/behave-steplib-guide/).

## What this is

A minimal Behave project that uses `behave-steplib` 1.5.1 to run API, data and
IO scenarios without writing custom step definitions.

## Requirements

- Python 3.11+
- `behave-steplib[api,io,data]` 1.5.1
- `behave` 1.3.3

## Install

```bash
cd api-example
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Version 1.5.1 is now on PyPI, so the normal install works. If you need the latest development build, use the GitHub main branch:

```bash
pip install "git+https://github.com/MathiasPaulenko/behave-steplib.git@main#egg=behave-steplib[api,io,data]"
```

## Run

```bash
behave
```

You should see three passing features: API, data and IO.
