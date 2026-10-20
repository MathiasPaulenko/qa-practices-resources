# Email Marketing Campaign Testing — Runnable Companion

Dependency-free Node script covering the mechanical checks of the [Email Marketing Campaign Testing Checklist](https://qapractices.com/checklists/email-marketing-campaign-testing-checklist/): unresolved merge tags, links without UTMs, missing alt text, Gmail clipping, and absent unsubscribe.

## Contents

| File | Purpose |
|---|---|
| `check-email-html.js` | Static pre-send checks on exported campaign HTML |
| `meta.json` | Resource metadata |

## Requirements

- Node.js 20+ — no dependencies.

## Usage

```bash
node check-email-html.js campaign-export.html
node check-email-html.js campaign-export.html --utm-required=utm_campaign,utm_source
```

Example output:

```text
  unresolved merge tag: {{first_name}} (line 42)
  link missing utm_campaign: https://shop.example.com/promo (line 88)
  img without alt: hero-banner.png (line 15)
  HTML size 104 KB — Gmail clips at 102 KB and can cut the CTA or footer links

4 issue(s) — fix before sending.
```

## What it checks

| Check | Why it matters |
|---|---|
| Merge tags `{{x}}`, `*|X|*`, `%x%` | Tokens without fallback ship as literal text |
| Required UTM params on external links | Clicks attribute to the wrong campaign or none |
| `<img>` without alt | Broken context with images disabled + a11y fail |
| HTML > 102 KB | Gmail clips the message — often the CTA |
| Unsubscribe link | Legal requirement and spam-complaint prevention |
| Plain-text sibling `.txt` file | Some clients and spam filters expect it |

## What it does not check

Rendering across email clients, spam score, and actual deliverability need real sends (Litmus, Email on Acid, seed lists). This script covers only what a static pass on the exported HTML can prove.

[Compañero en español](README.es.md)
