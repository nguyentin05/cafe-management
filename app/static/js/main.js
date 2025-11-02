document.addEventListener('DOMContentLoaded', function() {

  const header = document.querySelector('.navbar');
  let lastScrollTop = 0;
  const scrollThreshold = 50;

  window.addEventListener('scroll', function() {
    let currentScrollTop = window.scrollY || document.documentElement.scrollTop;

    if (currentScrollTop > scrollThreshold) {
      header.classList.add('header-scrolled');
      header.classList.add('bg-light');
      header.classList.add('navbar-light');
      header.classList.remove('navbar-dark');
      header.classList.remove('position-absolute');
    }
    else {
      header.classList.remove('header-scrolled');
      header.classList.remove('bg-light');
      header.classList.remove('navbar-light');
      header.classList.add('navbar-dark');
      header.classList.add('position-absolute');
    }

    if (currentScrollTop > lastScrollTop && currentScrollTop > scrollThreshold) {
      header.classList.add('header-hidden');
    }
    else {
      header.classList.remove('header-hidden');
    }

    lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;

  }, false);
});