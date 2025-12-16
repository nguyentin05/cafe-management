document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.navbar');
  const scrollThreshold = 50;
  let lastScrollTop = 0;

  window.addEventListener('scroll', () => {
    const currentScrollTop = window.scrollY || document.documentElement.scrollTop;
    const isScrolled = currentScrollTop > scrollThreshold;

    header.classList.toggle('header-scrolled', isScrolled);
    header.classList.toggle('bg-light', isScrolled);
    header.classList.toggle('navbar-light', isScrolled);

    header.classList.toggle('navbar-dark', !isScrolled);
    header.classList.toggle('position-absolute', !isScrolled);

    const isScrollingDown = currentScrollTop > lastScrollTop && isScrolled;
    header.classList.toggle('header-hidden', isScrollingDown);

    lastScrollTop = Math.max(0, currentScrollTop);
  }, { passive: true });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      entry.target.classList.toggle("is-visible", entry.isIntersecting);
    });
  }, { threshold: 0.1 });

  document.querySelectorAll(".scroll-animate").forEach(target => observer.observe(target));
});