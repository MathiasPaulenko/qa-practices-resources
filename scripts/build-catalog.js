const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const RESOURCES_DIR = path.join(ROOT, 'resources');
const SHARED_DIR = path.join(ROOT, 'shared');
const OUTPUT = path.join(ROOT, 'resources.json');

const REPO = process.env.REPO_URL || 'https://github.com/MathiasPaulenko/qa-practices-resources';
const BRANCH = process.env.REPO_BRANCH || 'main';

const IGNORED_FILES = new Set([
  'meta.json',
  'README.md',
  'README.es.md',
  '.DS_Store',
  'Thumbs.db',
]);

function isHidden(name) {
  return name.startsWith('.') || name === '__pycache__';
}

function toRawUrl(relativePath) {
  return `${REPO}/raw/${BRANCH}/${relativePath.replace(/\\/g, '/')}`;
}

function toViewUrl(relativePath) {
  return `${REPO}/blob/${BRANCH}/${relativePath.replace(/\\/g, '/')}`;
}

function toTreeUrl(relativePath) {
  return `${REPO}/tree/${BRANCH}/${relativePath.replace(/\\/g, '/')}`;
}

function listFiles(dir, relativeDir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) continue;
    if (isHidden(entry.name) || IGNORED_FILES.has(entry.name)) continue;
    const relativePath = path.join(relativeDir, entry.name);
    files.push({
      name: entry.name,
      path: relativePath.replace(/\\/g, '/'),
      raw_url: toRawUrl(relativePath),
      view_url: toViewUrl(relativePath),
    });
  }
  return files;
}

function readMeta(metaPath) {
  try {
    return JSON.parse(fs.readFileSync(metaPath, 'utf8'));
  } catch (err) {
    throw new Error(`Invalid JSON in ${metaPath}: ${err.message}`);
  }
}

function validateMeta(meta, metaPath) {
  const required = ['title', 'description', 'type', 'topic', 'slug'];
  for (const key of required) {
    if (!meta[key]) {
      throw new Error(`Missing required field "${key}" in ${metaPath}`);
    }
  }
}

function scanResources(baseDir, section) {
  const resources = [];
  if (!fs.existsSync(baseDir)) return resources;

  for (const typeEntry of fs.readdirSync(baseDir, { withFileTypes: true })) {
    if (!typeEntry.isDirectory()) continue;
    const typePath = path.join(baseDir, typeEntry.name);

    for (const topicEntry of fs.readdirSync(typePath, { withFileTypes: true })) {
      if (!topicEntry.isDirectory()) continue;
      const topicPath = path.join(typePath, topicEntry.name);

      for (const slugEntry of fs.readdirSync(topicPath, { withFileTypes: true })) {
        if (!slugEntry.isDirectory()) continue;
        const slugPath = path.join(topicPath, slugEntry.name);
        const metaPath = path.join(slugPath, 'meta.json');
        if (!fs.existsSync(metaPath)) {
          console.warn(`WARN: no meta.json found in ${slugPath}`);
          continue;
        }

        const meta = readMeta(metaPath);
        validateMeta(meta, metaPath);

        const relativePath = path.relative(ROOT, slugPath);
        const fileEntries = listFiles(slugPath, relativePath);

        const files = meta.files
          ? meta.files.map((name) => {
              const filePath = path.join(slugPath, name);
              const relativeFilePath = path.join(relativePath, name);
              if (!fs.existsSync(filePath)) {
                throw new Error(`File "${name}" listed in ${metaPath} does not exist`);
              }
              return {
                name,
                path: relativeFilePath.replace(/\\/g, '/'),
                raw_url: toRawUrl(relativeFilePath),
                view_url: toViewUrl(relativeFilePath),
              };
            })
          : fileEntries;

        resources.push({
          ...meta,
          section,
          path: relativePath.replace(/\\/g, '/'),
          github_url: toTreeUrl(relativePath),
          files,
        });
      }
    }
  }

  return resources;
}

function main() {
  const resources = scanResources(RESOURCES_DIR, 'resources');

  const catalog = {
    generatedAt: new Date().toISOString(),
    repo: REPO,
    branch: BRANCH,
    count: resources.length,
    resources,
  };

  fs.writeFileSync(OUTPUT, JSON.stringify(catalog, null, 2));
  console.log(`Wrote ${OUTPUT} with ${resources.length} resources`);
}

main();
