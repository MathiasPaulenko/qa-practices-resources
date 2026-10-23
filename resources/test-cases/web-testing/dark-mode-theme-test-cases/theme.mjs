// Theme resolution model matching the cases on qapractices.com:
// stored preference → prefers-color-scheme → default, with corrupted
// stored values falling back instead of throwing.

export const THEMES = {
  light: {
    '--color-bg': '#ffffff',
    '--color-surface': '#f5f5f5',
    '--color-surface-raised': '#ffffff',
    '--color-text': '#111111',
    '--color-text-muted': '#5a5a5a',
    '--color-border': '#d0d0d0',
    '--color-focus': '#005fcc',
    '--color-error': '#b3261e',
  },
  dark: {
    '--color-bg': '#111111',
    '--color-surface': '#1a1a1a',
    '--color-surface-raised': '#242424',
    '--color-text': '#eeeeee',
    '--color-text-muted': '#a8a8a8',
    '--color-border': '#3a3a3a',
    '--color-focus': '#8ab4ff',
    '--color-error': '#f28b82',
  },
};

export const SEMANTIC_TOKENS = Object.keys(THEMES.light);

export const VALID_THEMES = ['light', 'dark'];

/**
 * Resolution order (the same one the article's diagram shows):
 *   1. a valid stored preference always wins;
 *   2. otherwise the OS/system preference applies;
 *   3. otherwise the app default.
 * Anything else in storage — garbage, older enums, null — is ignored.
 */
export function resolveTheme(stored, system = 'none', fallback = 'light') {
  if (VALID_THEMES.includes(stored)) return stored;
  if (VALID_THEMES.includes(system)) return system;
  return fallback;
}

/**
 * Minimal localStorage-shaped store so tests can exercise persistence
 * and cross-tab sync without a browser. Two ThemeStores built over the
 * same Map behave like two tabs sharing origin storage.
 */
export class ThemeStore {
  constructor(map = new Map(), system = 'light') {
    this.map = map;
    this.system = system;
  }

  get stored() {
    const value = this.map.get('theme');
    return VALID_THEMES.includes(value) ? value : null;
  }

  get theme() {
    return resolveTheme(this.stored, this.system);
  }

  setTheme(theme) {
    this.map.set('theme', theme);
  }

  clear() {
    this.map.delete('theme');
  }
}
