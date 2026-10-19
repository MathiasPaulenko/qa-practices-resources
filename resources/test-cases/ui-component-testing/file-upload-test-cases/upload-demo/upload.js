const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const queue = document.getElementById('queue');
const MAX_BYTES = 10 * 1024 * 1024;
const ALLOWED = ['.pdf', '.png', '.jpg', '.jpeg', '.docx'];

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  addFiles(e.dataTransfer.files);
});
fileInput.addEventListener('change', () => {
  addFiles(fileInput.files);
  fileInput.value = ''; // reset so the same file can be picked again
});

function addFiles(files) {
  for (const file of files) enqueue(file);
}

function enqueue(file) {
  const item = document.createElement('li');
  item.className = 'queue-item';
  item.dataset.testid = 'queue-item';
  item.innerHTML = `
    <div class="meta"><span class="name">${file.name}</span><span class="size">${formatSize(file.size)}</span></div>
    <progress max="100" value="0"></progress>
    <div class="error" data-testid="error" hidden></div>
    <div class="actions">
      <button type="button" data-testid="cancel-btn" aria-label="Cancel upload">Cancel</button>
      <button type="button" data-testid="retry-btn" hidden>Retry</button>
      <button type="button" data-testid="remove-btn" aria-label="Remove file">Remove</button>
    </div>`;
  queue.appendChild(item);

  const ext = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
  const errorEl = item.querySelector('[data-testid="error"]');
  const progress = item.querySelector('progress');
  const cancelBtn = item.querySelector('[data-testid="cancel-btn"]');
  const retryBtn = item.querySelector('[data-testid="retry-btn"]');
  const removeBtn = item.querySelector('[data-testid="remove-btn"]');

  removeBtn.addEventListener('click', () => { xhr?.abort(); item.remove(); });
  retryBtn.addEventListener('click', () => send(file, item, progress, errorEl, cancelBtn, retryBtn, (x) => (xhr = x)));
  cancelBtn.addEventListener('click', () => xhr?.abort());

  if (!ALLOWED.includes(ext)) return fail('file type not allowed');
  if (file.size === 0) return fail('file is empty');
  if (file.size > MAX_BYTES) return fail('exceeds the 10 MB limit');

  let xhr;
  function fail(msg) {
    progress.hidden = true;
    errorEl.textContent = `Upload failed: ${msg}`;
    errorEl.hidden = false;
    retryBtn.hidden = false;
    cancelBtn.hidden = true;
  }
  send(file, item, progress, errorEl, cancelBtn, retryBtn, (x) => (xhr = x));
}

function send(file, item, progress, errorEl, cancelBtn, retryBtn, setXhr = () => {}) {
  progress.hidden = false;
  progress.value = 0;
  errorEl.hidden = true;
  retryBtn.hidden = true;
  cancelBtn.hidden = false;

  const xhr = new XMLHttpRequest();
  setXhr(xhr);
  xhr.open('POST', '/api/upload');
  xhr.upload.addEventListener('progress', (e) => {
    if (e.lengthComputable) progress.value = (e.loaded / e.total) * 100;
  });
  xhr.addEventListener('load', () => {
    if (xhr.status >= 200 && xhr.status < 300) {
      progress.value = 100;
      item.querySelector('.meta').insertAdjacentHTML('beforeend', '<span data-testid="status">uploaded</span>');
      cancelBtn.hidden = true;
    } else {
      progress.hidden = true;
      errorEl.textContent = `Upload failed: server returned ${xhr.status}`;
      errorEl.hidden = false;
      retryBtn.hidden = false;
      cancelBtn.hidden = true;
    }
  });
  xhr.addEventListener('error', () => {
    progress.hidden = true;
    errorEl.textContent = 'Upload failed: network error';
    errorEl.hidden = false;
    retryBtn.hidden = false;
    cancelBtn.hidden = true;
  });
  xhr.addEventListener('abort', () => {
    progress.hidden = true;
    errorEl.textContent = 'Upload cancelled';
    errorEl.hidden = false;
    cancelBtn.hidden = true;
  });

  const form = new FormData();
  form.append('file', file);
  xhr.send(form);
}

function formatSize(bytes) {
  return bytes >= 1024 * 1024 ? `${(bytes / 1024 / 1024).toFixed(1)} MB` : `${(bytes / 1024).toFixed(0)} KB`;
}
