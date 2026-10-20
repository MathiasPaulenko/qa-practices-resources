# Tree View Expand/Collapse Testing — Companion

Companion resource for [Tree View Expand Collapse Test Cases: Navigation](https://qapractices.com/test-cases/tree-view-expand-collapse-test-cases/).

## Contents

- `tree_model.py` — stdlib-only executable model of tree view logic: expand/collapse with expansion-state snapshot/restore (re-render persistence), lazy loading with fetcher injection and retryable error state, single-select, keyboard navigation (arrows, Home/End, type-ahead), checkbox cascade with indeterminate state, drag-and-drop with circular-reference rejection, and search filtering that keeps ancestor context.
- `tests/test_tree_model.py` — pytest 8.3 suite covering the model against the article's test cases TC001–TC024.
- `fixtures/tree.json` — the Documents/Work/Personal/Projects hierarchy used across the article.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/ui-component-testing/tree-view-expand-collapse-test-cases
pytest tests/ -v
```

## What this covers

- Expansion lifecycle: expand, collapse, expand-all visibility order (TC001–TC005, TC011).
- Lazy loading: success, 500 with retryable collapsed state, loaded caching (TC012–TC013).
- State persistence: snapshot/restore of expanded IDs across a rebuild (TC014).
- Keyboard contract: arrows, Home/End, type-ahead with no-match (TC006–TC007, TC022–TC023).
- Checkbox cascade: checked → indeterminate on partial uncheck (TC024).
- Drag-and-drop validation: move across parents, reject self/descendant drops (TC016–TC017).
- Search filter: matching nodes plus ancestor paths (TC015).
