const state = {
  ingredients: [],
  results: [],
};

const elements = {
  input: document.getElementById('ingredientInput'),
  addButton: document.getElementById('addButton'),
  searchButton: document.getElementById('searchButton'),
  randomButton: document.getElementById('randomButton'),
  installButton: document.getElementById('installButton'),
  summary: document.getElementById('ingredientSummary'),
  list: document.getElementById('ingredientList'),
  warning: document.getElementById('warningText'),
  resultBody: document.getElementById('resultBody'),
  modal: document.getElementById('detailModal'),
  detailTitle: document.getElementById('detailTitle'),
  detailBody: document.getElementById('detailBody'),
  closeModal: document.getElementById('closeModal'),
  closeModalButton: document.getElementById('closeModalButton'),
  toast: document.getElementById('toast'),
};

let deferredInstallPrompt = null;

function normalizeLocal(text) {
  return text.trim().replace(/\s+/g, ' ').toLowerCase();
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add('show');
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => {
    elements.toast.classList.remove('show');
  }, 1800);
}

function shakeInput() {
  elements.input.classList.remove('shake');
  void elements.input.offsetWidth;
  elements.input.classList.add('shake');
}

function addIngredients() {
  const raw = elements.input.value.trim();
  if (!raw) {
    elements.summary.textContent = 'Ketik bahan terlebih dahulu.';
    shakeInput();
    showToast('Ketik bahan dulu, ya.');
    return;
  }

  const parts = raw.split(',').map((part) => part.trim()).filter(Boolean);
  const existing = new Set(state.ingredients.map(normalizeLocal));
  let added = 0;

  for (const part of parts) {
    const key = normalizeLocal(part);
    if (!existing.has(key)) {
      state.ingredients.push(part);
      existing.add(key);
      added += 1;
    }
  }

  elements.input.value = '';
  renderIngredients();

  if (added > 0) {
    showToast(`${added} bahan ditambahkan`);
  } else {
    showToast('Bahan sudah ada di daftar.');
  }
}

function removeIngredient(index, itemElement) {
  if (itemElement) {
    itemElement.classList.add('removing');
    setTimeout(() => {
      state.ingredients.splice(index, 1);
      renderIngredients();
      showToast('Bahan dihapus');
      if (state.results.length > 0) {
        searchRecipes();
      }
    }, 160);
    return;
  }

  state.ingredients.splice(index, 1);
  renderIngredients();
  showToast('Bahan dihapus');
  if (state.results.length > 0) {
    searchRecipes();
  }
}

function renderIngredients() {
  elements.list.innerHTML = '';

  if (state.ingredients.length === 0) {
    elements.list.innerHTML = '<li class="summary">Bahan yang ditambahkan akan muncul di sini.</li>';
    elements.summary.textContent = 'Belum ada bahan yang ditambahkan.';
  } else {
    elements.summary.textContent = `${state.ingredients.length} bahan sudah ditambahkan.`;
    state.ingredients.forEach((ingredient, index) => {
      const item = document.createElement('li');
      item.className = 'ingredient-item';
      item.style.animationDelay = `${index * 30}ms`;
      item.innerHTML = `
        <span>• ${escapeHtml(ingredient)}</span>
        <button class="remove-button" data-index="${index}">Hapus</button>
      `;
      elements.list.appendChild(item);
    });
  }

  elements.list.querySelectorAll('.remove-button').forEach((button) => {
    button.addEventListener('click', () => {
      const item = button.closest('.ingredient-item');
      removeIngredient(Number(button.dataset.index), item);
    });
  });
}

function setWarning(message) {
  elements.warning.textContent = message || '';
}

function showSkeleton(text) {
  elements.resultBody.innerHTML = `
    <p class="summary skeleton-text">${escapeHtml(text)}</p>
    <div class="skeleton-card"></div>
    <div class="skeleton-card"></div>
  `;
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function requestRecommendations() {
  const response = await fetch('/api/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ingredients: state.ingredients }),
  });

  if (!response.ok) {
    throw new Error('Gagal mengambil rekomendasi.');
  }

  return response.json();
}

async function searchRecipes() {
  if (state.ingredients.length === 0) {
    elements.resultBody.innerHTML = '<p class="summary">Tambahkan bahan makanan terlebih dahulu.</p>';
    setWarning('');
    return;
  }

  showSkeleton('Mencari resep yang cocok…');

  try {
    const [data] = await Promise.all([requestRecommendations(), delay(260)]);
    state.results = data.recommendations || [];
    setWarning(data.warnings && data.warnings.join(' '));

    if (data.only_risky) {
      elements.resultBody.innerHTML = `<p class="summary">${escapeHtml(data.message || 'Semua bahan yang dimasukkan berisiko.')}</p>`;
      showToast('Bahan berisiko tidak dipakai');
      return;
    }

    if (state.results.length === 0) {
      elements.resultBody.innerHTML = '<p class="summary">Belum ada menu yang cocok dengan bahan tersedia. Coba tambahkan bahan lain.</p>';
      showToast('Belum ada resep cocok');
      return;
    }

    renderResults(data.source === 'template' ? 'IDE MASAKAN ALTERNATIF' : 'IDE MASAKAN');
  } catch (error) {
    elements.resultBody.innerHTML = '<p class="summary">Gagal mengambil rekomendasi. Periksa koneksi atau coba lagi.</p>';
    showToast('Gagal mengambil data');
  }
}

async function randomMenu() {
  if (state.ingredients.length === 0) {
    elements.resultBody.innerHTML = '<p class="summary">Belum ada bahan yang dimasukkan. Tambahkan bahan terlebih dahulu.</p>';
    setWarning('');
    return;
  }

  showSkeleton('Mengacak menu untuk hari ini…');

  try {
    const [data] = await Promise.all([requestRecommendations(), delay(420)]);
    state.results = data.recommendations || [];
    setWarning(data.warnings && data.warnings.join(' '));

    if (data.only_risky) {
      elements.resultBody.innerHTML = `<p class="summary">${escapeHtml(data.message || 'Semua bahan yang dimasukkan berisiko.')}</p>`;
      showToast('Bahan berisiko tidak dipakai');
      return;
    }

    if (state.results.length === 0) {
      elements.resultBody.innerHTML = '<p class="summary">Belum ada menu yang cocok dengan bahan tersedia. Coba tambahkan bahan lain.</p>';
      showToast('Belum ada resep cocok');
      return;
    }

    const choice = state.results[Math.floor(Math.random() * state.results.length)];
    renderResults('PILIHAN ACAK UNTUK HARI INI', choice);
  } catch (error) {
    elements.resultBody.innerHTML = '<p class="summary">Gagal mengambil rekomendasi. Periksa koneksi atau coba lagi.</p>';
    showToast('Gagal mengambil data');
  }
}

function renderResults(title, single) {
  elements.resultBody.innerHTML = `<h3 class="panel-title">${escapeHtml(title)}</h3>`;

  const items = single ? [single] : state.results;

  items.forEach((rec, index) => {
    const card = document.createElement('article');
    card.className = 'result-card';
    card.style.animationDelay = `${index * 55}ms`;

    const missing = rec.missing_ingredients.length > 0
      ? `Bahan yang kurang: ${escapeHtml(rec.missing_ingredients.join(', '))}`
      : 'Bahan yang kurang: Tidak ada';

    const optional = rec.matched_optional.length > 0
      ? `<p class="result-meta">Bahan opsional tersedia: ${escapeHtml(rec.matched_optional.join(', '))}</p>`
      : '';

    card.innerHTML = `
      <h4 class="result-name">${escapeHtml(rec.name)}</h4>
      <p class="result-meta">Bahan cocok: ${rec.matched} dari ${rec.required}</p>
      <p class="result-missing">${missing}</p>
      ${optional}
      <button class="button button-primary button-wide open-detail">Lihat Detail Masakan</button>
    `;

    card.querySelector('.open-detail').addEventListener('click', () => openDetail(rec));
    elements.resultBody.appendChild(card);
  });
}

function openDetail(rec) {
  elements.detailTitle.textContent = rec.name;

  const matched = rec.matched_ingredients.length > 0
    ? escapeHtml(rec.matched_ingredients.join(', '))
    : 'Tidak ada';

  const missing = rec.missing_ingredients.length > 0
    ? escapeHtml(rec.missing_ingredients.join(', '))
    : 'Tidak ada';

  const optional = rec.matched_optional.length > 0
    ? `<div class="detail-section">BAHAN OPSIONAL</div><div>${escapeHtml(rec.matched_optional.join(', '))}</div>`
    : '';

  const steps = rec.steps.map((step, index) => `<li>${escapeHtml(step)}</li>`).join('');

  elements.detailBody.innerHTML = `
    <div class="detail-section">BAHAN TERSEDIA</div>
    <div>${matched}</div>

    <div class="detail-section">BAHAN YANG KURANG</div>
    <div>${missing}</div>

    ${optional}

    <div class="detail-section">LANGKAH MEMASAK</div>
    <ol class="step-list">${steps}</ol>
  `;

  elements.modal.hidden = false;
}

function closeModal() {
  elements.modal.hidden = true;
}

elements.addButton.addEventListener('click', addIngredients);
elements.input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') addIngredients();
});
elements.searchButton.addEventListener('click', searchRecipes);
elements.randomButton.addEventListener('click', randomMenu);
elements.closeModal.addEventListener('click', closeModal);
elements.closeModalButton.addEventListener('click', closeModal);
elements.modal.addEventListener('click', (event) => {
  if (event.target === elements.modal) closeModal();
});

window.addEventListener('beforeinstallprompt', (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  elements.installButton.hidden = false;
});

elements.installButton.addEventListener('click', async () => {
  if (!deferredInstallPrompt) return;

  deferredInstallPrompt.prompt();
  await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  elements.installButton.hidden = true;
});

window.addEventListener('appinstalled', () => {
  elements.installButton.hidden = true;
});

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js').catch(() => {});
  });
}

renderIngredients();
