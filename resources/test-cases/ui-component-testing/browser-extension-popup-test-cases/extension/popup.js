const noteInput = document.getElementById('note');
const saveButton = document.getElementById('save');
const toast = document.getElementById('toast');
const list = document.getElementById('saved-list');
const compactToggle = document.getElementById('compact-view');

async function loadState() {
  const { savedPages = [], compactView = false } = await chrome.storage.local.get([
    'savedPages',
    'compactView',
  ]);
  compactToggle.checked = compactView;
  renderList(savedPages);
}

function renderList(pages) {
  list.innerHTML = '';
  for (const page of pages) {
    const item = document.createElement('li');
    item.className = 'saved-item';
    item.textContent = page.title;
    const meta = document.createElement('small');
    meta.textContent = `${page.url} · ${page.note || 'no note'}`;
    item.appendChild(meta);
    list.appendChild(item);
  }
}

async function requestActiveTab() {
  const granted = await chrome.permissions.request({ permissions: ['activeTab'] });
  if (!granted) {
    saveButton.disabled = true;
    saveButton.textContent = 'Permission required';
  }
  return granted;
}

saveButton.addEventListener('click', async () => {
  const granted = await requestActiveTab();
  if (!granted) return;

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const entry = {
    url: tab?.url ?? 'chrome-extension://popup',
    title: tab?.title ?? 'Extension page',
    note: noteInput.value.slice(0, 140),
    savedAt: new Date().toISOString(),
  };

  const response = await chrome.runtime.sendMessage({ type: 'SAVE', entry });
  if (!response?.ok) {
    toast.textContent = 'Save failed — retry';
    toast.style.display = 'block';
    return;
  }

  const { savedPages = [] } = await chrome.storage.local.get('savedPages');
  savedPages.unshift(entry);
  await chrome.storage.local.set({ savedPages });
  renderList(savedPages);
  noteInput.value = '';
  toast.textContent = 'Saved';
  toast.style.display = 'block';
});

compactToggle.addEventListener('change', async () => {
  await chrome.storage.local.set({ compactView: compactToggle.checked });
});

loadState();
