document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const href = link.getAttribute('href');
    if (!href || href === '#') return;
    const target = document.querySelector(href);
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({
      behavior: prefersReducedMotion ? 'auto' : 'smooth',
      block: 'start'
    });
  });
});

const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

if (navToggle && navLinks) {
  const setNavOpen = (isOpen) => {
    navToggle.setAttribute('aria-expanded', String(isOpen));
    navToggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    navLinks.classList.toggle('is-open', isOpen);
  };

  navToggle.addEventListener('click', () => {
    setNavOpen(navToggle.getAttribute('aria-expanded') !== 'true');
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setNavOpen(false));
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setNavOpen(false);
      navToggle.focus();
    }
  });

  document.addEventListener('click', (event) => {
    if (!navLinks.classList.contains('is-open')) return;
    if (navLinks.contains(event.target) || navToggle.contains(event.target)) return;
    setNavOpen(false);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 860) setNavOpen(false);
  });
}

// A miniature ReplyKit: expands a shortcut as soon as it is fully typed.
const replyDemo = document.querySelector('[data-replykit-demo]');
const replyStatus = document.querySelector('[data-replykit-status]');

if (replyDemo) {
  const snippets = {
    ';thanks': 'Hi,\n\nThanks for getting in touch. I’ve logged this as a ticket and we’ll update you as soon as we have more information.\n\nKind regards,\nThe Support Team',
    ';unlock': 'Hi,\n\nYour account has now been unlocked. Please sign in again, and if you’re asked to, choose a new password.\n\nKind regards,\nThe Support Team',
    ';escalate': 'Hi,\n\nI’ve escalated this to our specialist team with the details you’ve provided. They’ll be in touch directly with next steps.\n\nKind regards,\nThe Support Team'
  };

  replyDemo.addEventListener('input', () => {
    const caret = replyDemo.selectionStart;
    const before = replyDemo.value.slice(0, caret);
    const shortcut = Object.keys(snippets).find((key) => {
      if (!before.endsWith(key)) return false;
      const prev = before.charAt(before.length - key.length - 1);
      return prev === '' || /\s/.test(prev);
    });
    if (!shortcut) return;
    const start = caret - shortcut.length;
    replyDemo.setRangeText(snippets[shortcut], start, caret, 'end');
    if (replyStatus) {
      replyStatus.textContent = `Expanded ${shortcut} — the extension does this in any web app.`;
      replyStatus.classList.add('is-hit');
    }
  });
}
