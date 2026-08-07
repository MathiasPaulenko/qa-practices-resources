# Contributing to QAPractices Resources

This repository hosts downloadable resources and runnable examples referenced from [qapractices.com](https://qapractices.com).

## How to add a resource

1. Pick the right place under `resources/`:

   ```text
   resources/{type}/{topic}/{slug}/
   ```

   - `type` must be one of: `test-cases`, `checklists`, `templates`, `prompts`, `documentation`.
   - `topic` should match a topic slug already used on qapractices.com.
   - `slug` is a short, unique, kebab-case identifier.

2. Create a `meta.json` file in that folder. Example:

   ```json
   {
     "title": "Behave BDD Shop Example",
     "title_es": "Ejemplo de tienda con Behave BDD",
     "description": "Complete runnable Behave and Gherkin example for an e-commerce cart.",
     "description_es": "Ejemplo completo y ejecutable de Behave y Gherkin para un carrito de comercio electrónico.",
     "type": "documentation",
     "topic": "behave",
     "slug": "shop-bdd",
     "source_urls": [
       "https://qapractices.com/documentation/gherkin-best-practices-behave/"
     ],
     "language": "python",
     "tags": ["behave", "gherkin", "bdd", "python"],
     "files": [
       "shop_domain.py",
       "behave.ini",
       "features/environment.py",
       "features/steps/shop_steps.py",
       "features/order_discount.feature"
     ]
   }
   ```

3. Add the actual files. If you do not list them in `files`, the build script will discover them automatically, but explicit lists are safer.

4. Optional: add `README.md` and `README.es.md` with usage instructions.

5. Run the catalog builder locally:

   ```bash
   npm install
   npm run build
   ```

   This generates `resources.json` used by the GitHub Pages browser.

6. Commit and push. The GitHub Action will rebuild and redeploy the browser.

## Reusable assets

If a snippet or helper is reused by multiple resources, place it under `shared/`:

```text
shared/snippets/python/behave/helpers/money_parser.py
```

Reference it from the resource `README.md` or `meta.json` `shared_dependencies` field.

## Validation

The build script checks that:

- `meta.json` contains `title`, `description`, `type`, `topic`, `slug`.
- Every file listed in `files` exists.
- `source_urls` are valid URLs.

If the build fails, the GitHub Pages deploy does not run.
