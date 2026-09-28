/* Interface controls only. Original source content is never rewritten. */
const menu = document.querySelector('.menu-toggle');
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
const search = document.querySelector('#paper-search');
if (search) {
  const year = document.querySelector('#year-select');
  const papers = [...document.querySelectorAll('.paper')];
  const groups = [...document.querySelectorAll('.year-group')];
  const expand = document.querySelector('#expand-all');
  const zh = document.body.dataset.language === 'zh';
  const normalized = text => text.normalize('NFKC').replace(/\u200b/g, '').toLocaleLowerCase();
  const corpus = new Map(papers.map(paper => [paper, normalized(paper.querySelector('.source').textContent)]));
  function updateExpandLabel() {
    const details = papers.filter(p => !p.hidden).flatMap(p => [...p.querySelectorAll('details')]);
    const allOpen = details.length > 0 && details.every(d => d.open);
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
    for (const group of groups) group.hidden = ![...group.querySelectorAll('.paper')].some(p => !p.hidden);
    document.querySelector('#result-count').textContent = zh ? `共 ${count} 篇` : `${count} ${count === 1 ? 'paper' : 'papers'}`;
    document.querySelector('#empty-state').hidden = count > 0;
    document.querySelectorAll('[data-year-link]').forEach(a => {
      a.hidden = !groups.some(g => g.dataset.year === a.dataset.yearLink && !g.hidden);
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
    papers.filter(p => !p.hidden).forEach(p => p.querySelectorAll('details').forEach(d => { d.open = open; }));
    updateExpandLabel();
  });
  document.querySelectorAll('details').forEach(d => d.addEventListener('toggle', updateExpandLabel));
  filter();
}
