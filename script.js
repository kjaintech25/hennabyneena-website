// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (e) => {
    const targetId = anchor.getAttribute('href');
    if (!targetId || targetId.length <= 1) return;
    const target = document.querySelector(targetId);
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// Nav scroll state
const nav = document.getElementById('mainNav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('is-scrolled', window.scrollY > 40);
}, { passive: true });

// Reveal on scroll
document.querySelectorAll('.about-inner, .service-card, .portfolio-header, .reviews-carousel, .contact-header').forEach((el) => el.classList.add('reveal'));

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1 }
);

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

// Swiper init
const portfolioSwiper = new Swiper('.portfolio-swiper', {
  loop: true,
  slidesPerView: 'auto',
  spaceBetween: 18,
  speed: 420,
  grabCursor: true,
  centeredSlides: false,
  watchSlidesProgress: true,
  navigation: {
    prevEl: '#prevBtn',
    nextEl: '#nextBtn',
  },
  pagination: {
    el: '.portfolio-swiper .swiper-pagination',
    clickable: true,
  },
  resistance: true,
  resistanceRatio: 0.6,
});

const reviewsSwiper = new Swiper('.reviews-swiper', {
  loop: true,
  slidesPerView: 'auto',
  spaceBetween: 18,
  speed: 420,
  grabCursor: true,
  centeredSlides: false,
  watchSlidesProgress: true,
  navigation: {
    prevEl: '.reviews-prev',
    nextEl: '.reviews-next',
  },
  pagination: {
    el: '.reviews-swiper .swiper-pagination',
    clickable: true,
  },
  breakpoints: {
    640: { spaceBetween: 20 },
    900: { spaceBetween: 24 },
    1100: { spaceBetween: 28 },
  },
  resistance: true,
  resistanceRatio: 0.6,
});

document.getElementById('year').textContent = new Date().getFullYear();
