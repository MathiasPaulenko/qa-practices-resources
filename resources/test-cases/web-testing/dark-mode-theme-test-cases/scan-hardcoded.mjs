// Finds hex color literals assigned to real CSS properties — i.e. colors
// that bypass the token system and stay the same in every theme.
// Custom property definitions (`--color-x: #fff`) are allowed; a literal
// in `color:`, `background:` or `border-color:` is the leak TC-007 hunts.

const DECLARATION_RE = /([a-zA-Z-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\b/g;

export function findHardcodedColors(cssSource) {
  const hits = [];
  for (const match of cssSource.matchAll(DECLARATION_RE)) {
    const [, property, value] = match;
    if (!property.startsWith('--')) {
      hits.push({ property, value });
    }
  }
  return hits;
}
