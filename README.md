# QAPractices Resources

Companion repository for [qapractices.com](https://qapractices.com).

This repository hosts complete projects, templates, checklists, test cases and prompts referenced from the main site. Every resource lives in a self-contained folder under `resources/` and is described by a `meta.json` file. A static GitHub Pages browser makes it easy to search and filter resources.

## What is this repository for?

[QAPractices](https://qapractices.com) is a hub of QA resources. Many articles include code examples, templates or checklists. This repository keeps those files in one place so readers can:

- Clone or download complete, runnable projects.
- Copy individual files without extracting snippets from an article.
- See which resources belong to each topic and content type.

## Browse resources online

The resource browser is published at:

**https://mathiaspaulenko.github.io/qa-practices-resources/**

It loads the generated catalog `resources.json` and lets you search by title, description, type, topic and language.

> To enable the browser, go to **Settings → Pages** in this repository and set the source to **GitHub Actions**. The workflow in `.github/workflows/pages.yml` will build and deploy the site on every push to `main`.

## Use a resource

Each resource is a folder. For example, the Behave BDD shop example:

```bash
cd resources/documentation/behave/shop-bdd
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
behave
```

You can also download a single file using the **raw** link in the browser or by copying the URL from the resource folder.

## Repository structure

```text
qa-practices-resources/
├── scripts/
│   └── build-catalog.js       # generates resources.json from all meta.json files
├── .github/workflows/
│   └── pages.yml              # deploys the browser to GitHub Pages
├── docs/
│   └── CONTRIBUTING.md        # how to add a new resource
├── resources/                 # all resources, by type and topic
│   ├── documentation/
│   │   └── behave/
│   │       └── shop-bdd/
│   │           ├── meta.json
│   │           ├── README.md
│   │           ├── README.es.md
│   │           └── ...
│   ├── test-cases/
│   ├── checklists/
│   ├── templates/
│   └── prompts/
└── shared/                    # reusable snippets, assets and templates
    ├── snippets/
    ├── assets/
    └── templates/
```

- `type`: `documentation`, `templates`, `checklists`, `test-cases`, `prompts`.
- `topic`: matches a topic slug from qapractices.com.
- `slug`: unique, kebab-case identifier for the resource.
- `meta.json`: metadata, source URLs, tags and file list.
- `README.md` / `README.es.md`: human-readable instructions in English and Spanish.

## Build the catalog locally

```bash
npm run build
```

This runs `scripts/build-catalog.js`, scans every `resources/{type}/{topic}/{slug}/meta.json`, validates the file list and writes `resources.json`. Then open `index.html` in a browser or run a local server:

```bash
python -m http.server 8080
```

## Add a resource

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for the full guide.

Short version:

1. Create `resources/{type}/{topic}/{slug}/`.
2. Add a `meta.json` with at least `title`, `description`, `type`, `topic`, `slug`.
3. Add the files and a `README.md`.
4. Run `npm run build` to test the catalog.
5. Commit and push. GitHub Actions will redeploy the browser.

## Validation

The build script checks that:

- Every `meta.json` has the required fields.
- Every file listed in `files` exists.
- `source_urls` are valid URLs.

If the build fails, the GitHub Pages deploy is skipped.

## License

Resources are provided as-is for educational and professional use. Unless otherwise stated in a specific resource, code is released under the MIT license.
