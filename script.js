document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const cvDownload = {
  href: 'assets/Lewis-Price-CV.pdf',
  filename: 'Lewis-Price-CV.pdf',
};

function addCvDownload(selector) {
  const actions = document.querySelector(selector);
  if (!actions || actions.querySelector('[data-cv-download]')) return;

  const link = document.createElement('a');
  link.className = 'btn secondary';
  link.href = cvDownload.href;
  link.download = cvDownload.filename;
  link.dataset.cvDownload = '';
  link.setAttribute('aria-label', 'Download Lewis Price CV as a PDF');
  link.textContent = 'Download CV ↓';

  actions.insertBefore(link, actions.children[1] || null);
}

addCvDownload('.hero-actions');
addCvDownload('.cta-actions');

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
