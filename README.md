# QAPractices Resources

Downloadable resources and runnable examples for [qapractices.com](https://qapractices.com).

This repository hosts complete projects, templates, checklists, test cases and prompts that are referenced from the main site. Each resource lives in a self-contained folder under `resources/` and is described by a `meta.json` file.

## Browse resources

Visit the resource browser: `https://mathiaspaulenko.github.io/qa-practices-resources/`

## Add a resource

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## Structure

```text
resources/
  {type}/
    {topic}/
      {slug}/
        meta.json
        README.md
        ...
```

- `type`: `documentation`, `templates`, `checklists`, `test-cases`, `prompts`.
- `topic`: matches a topic slug from qapractices.com.
- `slug`: unique identifier for the resource.
