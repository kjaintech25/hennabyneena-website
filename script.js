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

// Nav scroll state + scroll progress
const nav = document.getElementById('mainNav');
const scrollProgress = document.getElementById('scrollProgress');

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  nav.classList.toggle('is-scrolled', scrollY > 40);

  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;
  scrollProgress.style.width = progress + '%';
}, { passive: true });

// Scroll-spy — highlight active nav link
const sections = document.querySelectorAll('section[id], header[id]');
const navLinks = document.querySelectorAll('.nav-links a');

const scrollSpy = () => {
  const scrollY = window.scrollY + 120;
  let current = '';

  sections.forEach((section) => {
    const top = section.offsetTop;
    const height = section.offsetHeight;
    if (scrollY >= top && scrollY < top + height) {
      current = '#' + section.getAttribute('id');
    }
  });

  navLinks.forEach((link) => {
    link.classList.toggle('active', link.getAttribute('href') === current);
  });
};

window.addEventListener('scroll', scrollSpy, { passive: true });
scrollSpy();

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
