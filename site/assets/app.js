/* Interface controls and Wix CMS hydration. The reviewed static snapshot is
   retained as a fallback if Wix CMS is temporarily unavailable. */
const menu = document.querySelector('.menu-toggle');
const currentYear = String(new Date().getFullYear());
document.querySelectorAll('[data-current-year]').forEach(element => {
  element.textContent = currentYear;
});
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  document.querySelector('#site-nav').classList.toggle('is-open', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    menu.click();
    menu.focus();
  }
});

const escapeHtml = value => String(value ?? '').replace(/[&<>"]/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'
})[character]);

function mediaHtml(item, language) {
  const parts = [];
  if (item.audioUrl) {
    parts.push(`<div class="recording"><div class="recording-label"><span aria-hidden="true">♫</span><strong>${escapeHtml(item.audioTitle || item.title)}</strong><span>${escapeHtml(item.audioCredit || '')}</span></div><audio controls preload="none" src="${escapeHtml(item.audioUrl)}" aria-label="${escapeHtml(item.audioTitle || item.title)}"><a href="${escapeHtml(item.audioUrl)}">${escapeHtml(item.audioTitle || item.title)}</a></audio></div>`);
  }
  if (item.videoEmbedUrl) {
    const watchLabel = language === 'zh' ? '在 YouTube 觀看 ↗' : 'Watch on YouTube ↗';
    const watch = item.videoWatchUrl ? `<a href="${escapeHtml(item.videoWatchUrl)}" target="_blank" rel="noopener">${watchLabel}</a>` : '';
    parts.push(`<div class="performance"><iframe loading="lazy" src="${escapeHtml(item.videoEmbedUrl)}" title="${escapeHtml(item.title)}" allow="encrypted-media; picture-in-picture; fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>${watch}</div>`);
  }
  if (item.imageUrl) {
    parts.push(`<img class="publication-cover" src="${escapeHtml(item.imageUrl)}" alt="${escapeHtml(item.imageAlt || item.title)}" loading="lazy">`);
  }
  return parts.join('');
}

function renderWorks(items, language) {
  const rail = document.querySelector('.work-rail');
  const works = document.querySelector('.works');
  if (!rail || !works) return;
  rail.querySelectorAll('a[href^="#work-"]').forEach(link => link.remove());
  const sourceLink = rail.querySelector('.source-site');
  items.forEach((item, index) => {
    const number = String(index + 1).padStart(2, '0');
    const link = document.createElement('a');
    link.href = `#work-${index + 1}`;
    link.innerHTML = `<span>${number}</span>${escapeHtml(item.title)}`;
    rail.insertBefore(link, sourceLink);
  });
  works.querySelectorAll('article.work').forEach(article => article.remove());
  const markup = items.map((item, index) => {
    const number = String(index + 1).padStart(2, '0');
    return `<article class="work" id="work-${index + 1}"><div class="work-number">${number} <span>↘</span></div><div class="work-body prose">${item.body || ''}${mediaHtml(item, language)}</div></article>`;
  }).join('');
  works.insertAdjacentHTML('beforeend', markup);
}

function renderAcademic(items, language) {
  const container = document.querySelector('#paper-groups');
  if (!container) return;
  const groups = new Map();
  items.forEach(item => {
    const year = String(item.year || 'Undated');
    if (!groups.has(year)) groups.set(year, []);
    groups.get(year).push(item);
  });
  container.innerHTML = [...groups.entries()].map(([year, papers]) => {
    const rows = papers.map((item, index) => {
      const abstract = item.abstract ? `<details class="abstract"><summary data-interface="true">${language === 'zh' ? '閱讀摘要' : 'Read abstract'}<span aria-hidden="true">＋</span></summary><div class="abstract-body">${item.abstract}</div></details>` : '';
      return `<article class="paper" id="${escapeHtml(item.entryKey)}" data-year="${escapeHtml(year)}"><span class="paper-index" aria-hidden="true">${String(index + 1).padStart(2, '0')}</span><div class="source">${item.body || ''}${abstract}</div></article>`;
    }).join('');
    return `<section class="year-group" id="year-${escapeHtml(year)}" data-year="${escapeHtml(year)}"><div class="year-heading"><h2>${escapeHtml(year)}</h2><span>${String(papers.length).padStart(2, '0')}</span></div>${rows}</section>`;
  }).join('');
  const yearLinks = document.querySelector('.year-links');
  if (yearLinks) yearLinks.innerHTML = [...groups.entries()].map(([year, papers]) => `<a href="#year-${escapeHtml(year)}" data-year-link="${escapeHtml(year)}">${escapeHtml(year)}<span>${String(papers.length).padStart(2, '0')}</span></a>`).join('');
  const select = document.querySelector('#year-select');
  if (select) select.innerHTML = `<option value="">${language === 'zh' ? '所有年份' : 'All years'}</option>` + [...groups.keys()].map(year => `<option value="${escapeHtml(year)}">${escapeHtml(year)}</option>`).join('');
  const allCount = document.querySelector('.all-years span');
  if (allCount) allCount.textContent = String(items.length);
}

async function hydrateCms() {
  const pageKey = document.body.dataset.page;
  const language = document.body.dataset.language;
  if (!pageKey || !language) return;
  try {
    const response = await fetch(`/api/content.json?pageKey=${encodeURIComponent(pageKey)}&language=${encodeURIComponent(language)}`, { headers: { accept: 'application/json' } });
    if (!response.ok) return;
    const payload = await response.json();
    const items = Array.isArray(payload.items) ? payload.items : [];
    if (!items.length) return;
    if (pageKey === 'home') {
      const profile = items.find(item => item.entryKey === 'profile');
      const biography = document.querySelector('.biography .prose > .source');
      const portrait = document.querySelector('.portrait');
      if (profile?.body && biography) biography.innerHTML = profile.body;
      if (profile?.imageUrl && portrait) {
        portrait.src = profile.imageUrl;
        portrait.alt = profile.imageAlt || profile.title;
      }
    } else if (pageKey === 'academic') {
      renderAcademic(items, language);
    } else {
      renderWorks(items, language);
    }
    document.body.dataset.contentSource = 'wix-cms';
  } catch (error) {
    console.warn('Using reviewed static content because Wix CMS was unavailable.', error);
  }
}

function initPaperTools() {
  const search = document.querySelector('#paper-search');
  if (!search || search.dataset.ready === 'true') return;
  search.dataset.ready = 'true';
  const year = document.querySelector('#year-select');
  const papers = [...document.querySelectorAll('.paper')];
  const groups = [...document.querySelectorAll('.year-group')];
  const expand = document.querySelector('#expand-all');
  const zh = document.body.dataset.language === 'zh';
  const normalized = text => text.normalize('NFKC').replace(/\u200b/g, '').toLocaleLowerCase();
  const corpus = new Map(papers.map(paper => [paper, normalized(paper.querySelector('.source')?.textContent || '')]));
  function updateExpandLabel() {
    const details = papers.filter(paper => !paper.hidden).flatMap(paper => [...paper.querySelectorAll('details')]);
    const allOpen = details.length > 0 && details.every(detail => detail.open);
    expand.disabled = details.length === 0;
    expand.setAttribute('aria-expanded', String(allOpen));
    expand.textContent = (allOpen ? (zh ? '收合全部摘要' : 'Collapse all abstracts') : (zh ? '展開全部摘要' : 'Expand all abstracts')) + (allOpen ? ' −' : ' ＋');
  }
  function filter() {
    const terms = normalized(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const paper of papers) {
      paper.hidden = Boolean(year.value && paper.dataset.year !== year.value) || !terms.every(term => corpus.get(paper).includes(term));
      if (!paper.hidden) count++;
    }
    for (const group of groups) group.hidden = ![...group.querySelectorAll('.paper')].some(paper => !paper.hidden);
    document.querySelector('#result-count').textContent = zh ? `共 ${count} 篇` : `${count} ${count === 1 ? 'paper' : 'papers'}`;
    document.querySelector('#empty-state').hidden = count > 0;
    document.querySelectorAll('[data-year-link]').forEach(link => {
      link.hidden = !groups.some(group => group.dataset.year === link.dataset.yearLink && !group.hidden);
    });
    updateExpandLabel();
  }
  search.addEventListener('input', filter);
  year.addEventListener('change', filter);
  document.querySelector('.search-tools').addEventListener('submit', event => event.preventDefault());
  document.querySelector('#clear-search').addEventListener('click', () => { search.value = ''; year.value = ''; filter(); search.focus(); });
  document.querySelector('.all-years').addEventListener('click', () => { search.value = ''; year.value = ''; filter(); });
  expand.addEventListener('click', () => {
    const open = expand.getAttribute('aria-expanded') !== 'true';
    papers.filter(paper => !paper.hidden).forEach(paper => paper.querySelectorAll('details').forEach(detail => { detail.open = open; }));
    updateExpandLabel();
  });
  document.querySelectorAll('details').forEach(detail => detail.addEventListener('toggle', updateExpandLabel));
  filter();
}

hydrateCms().finally(initPaperTools);
