// ========================================
// CAROUSEL DATA — Edit these arrays to change images/reviews
// ========================================

// Portfolio images: Add/remove objects below
// - src: path to image (local "Real Images/your-image.jpg" or remote URL)
// - alt: description for accessibility
const portfolioImages = [
  { src: "https://images.unsplash.com/photo-1661885411165-a08c34f40488?w=800&q=80", alt: "Bridal mehndi detail" },
  { src: "https://images.unsplash.com/photo-1669257966198-5243002b0ca8?w=800&q=80", alt: "Intricate hand mehndi" },
  { src: "https://images.unsplash.com/photo-1735158238825-a133e43c8ae4?w=800&q=80", alt: "Bridal arm mehndi" },
  { src: "https://images.unsplash.com/photo-1633104502901-10d124036629?w=800&q=80", alt: "Groom's hand mehndi" },
  { src: "https://images.unsplash.com/photo-1782876224837-e7163083c4c7?w=800&q=80", alt: "Ceremonial mehndi feet" },
  { src: "https://images.unsplash.com/photo-1681519251874-91d0e62d4268?w=800&q=80", alt: "Floral mehndi" },
  { src: "https://images.unsplash.com/photo-1684813910513-11e6b30adc22?w=800&q=80", alt: "Party henna session" },
  { src: "https://images.unsplash.com/photo-1566360896955-1ebb427d0e14?w=800&q=80", alt: "Dark mehndi design" },
];

// Reviews: Add/remove objects below
// - text: the review quote
// - author: reviewer name
// Sourced and paraphrased from Neena's real Google Business reviews (5.0 stars, 184 reviews)
const reviews = [
  { text: "Neena did henna for my entire wedding party — me, my sister-in-law, my mother-in-law, and even my husband. She worked quickly without ever cutting corners on quality, and it showed in every detail.", author: "Amy T." },
  { text: "Neena walked me through exactly how to prep my skin before and care for it after, and the results were stunning — intricate, beautiful, and the stain came out richer than I expected.", author: "Seema R." },
  { text: "Neena did a fantastic job on our bridal henna. She's fast, incredibly talented, and the color always turns out beautifully — you won't regret booking her.", author: "Liron & Julia" },
];

// ========================================
// Populate carousels from data above
// ========================================

const portfolioWrapper = document.getElementById('portfolioWrapper');
if (portfolioWrapper) {
  portfolioImages.forEach(({ src, alt }) => {
    const slide = document.createElement('div');
    slide.className = 'swiper-slide';
    slide.innerHTML = `<img src="${src}" alt="${alt}" loading="lazy">`;
    portfolioWrapper.appendChild(slide);
  });
}

const reviewsWrapper = document.getElementById('reviewsWrapper');
if (reviewsWrapper) {
  reviews.forEach(({ text, author }) => {
    const slide = document.createElement('div');
    slide.className = 'swiper-slide';
    slide.innerHTML = `
      <div class="review-card">
        <div class="review-stars" aria-label="5 of 5 stars">★★★★★</div>
        <p class="review-text">"${text}"</p>
        <span class="review-author">${author}</span>
      </div>
    `;
    reviewsWrapper.appendChild(slide);
  });
}

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

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const mobileNav = document.getElementById('mobileNav');
const mobileNavBackdrop = document.getElementById('mobileNavBackdrop');

function closeMobileNav() {
  navToggle.classList.remove('is-open');
  navToggle.setAttribute('aria-expanded', 'false');
  navToggle.querySelector('.nav-toggle-icon').textContent = 'menu';
  mobileNav.classList.remove('is-open');
  mobileNav.setAttribute('aria-hidden', 'true');
  mobileNavBackdrop.classList.remove('is-open');
  document.body.style.overflow = '';
}

function openMobileNav() {
  navToggle.classList.add('is-open');
  navToggle.setAttribute('aria-expanded', 'true');
  navToggle.querySelector('.nav-toggle-icon').textContent = 'close';
  mobileNav.classList.add('is-open');
  mobileNav.setAttribute('aria-hidden', 'false');
  mobileNavBackdrop.classList.add('is-open');
  document.body.style.overflow = 'hidden';
}

if (navToggle && mobileNav && mobileNavBackdrop) {
  navToggle.addEventListener('click', () => {
    if (mobileNav.classList.contains('is-open')) closeMobileNav();
    else openMobileNav();
  });
  mobileNavBackdrop.addEventListener('click', closeMobileNav);
  mobileNav.querySelectorAll('a').forEach((a) => a.addEventListener('click', closeMobileNav));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMobileNav();
  });
}

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
document.querySelectorAll('.about-inner, .service-card, .portfolio-header, .reviews-carousel, .contact-header, .faq-header').forEach((el) => el.classList.add('reveal'));

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
if (document.querySelector('.portfolio-swiper')) {
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
}

if (document.querySelector('.reviews-swiper')) {
const reviewsSwiper = new Swiper('.reviews-swiper', {
  loop: true,
  slidesPerView: 1,
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
    640: {
      slidesPerView: 1.5,
      spaceBetween: 20,
    },
    900: {
      slidesPerView: 2.5,
      spaceBetween: 24,
    },
    1100: {
      slidesPerView: 3,
      spaceBetween: 28,
    },
  },
  resistance: true,
  resistanceRatio: 0.6,
});
}

// Hero parallax — subtle background movement on scroll
const heroBg = document.querySelector('.hero-bg img');
const hero = document.querySelector('.hero');

if (heroBg && hero) {
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const heroHeight = hero.offsetHeight;
    
    // Only parallax while hero is visible
    if (scrolled < heroHeight) {
      const speed = 0.3; // Subtle — 30% of scroll speed
      heroBg.style.transform = `translateY(${scrolled * speed}px)`;
    }
  }, { passive: true });
}

// Back to top button
const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
  backToTop.classList.toggle('is-visible', window.scrollY > 600);
}, { passive: true });

document.getElementById('year').textContent = new Date().getFullYear();

// FAQ accordion
document.querySelectorAll('.faq-question').forEach((btn) => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('is-open');

    document.querySelectorAll('.faq-item.is-open').forEach((openItem) => {
      if (openItem !== item) {
        openItem.classList.remove('is-open');
        openItem.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
      }
    });

    item.classList.toggle('is-open', !isOpen);
    btn.setAttribute('aria-expanded', String(!isOpen));
  });
});
