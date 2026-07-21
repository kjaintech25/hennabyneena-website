// ========================================
// CAROUSEL DATA — Edit these arrays to change images/reviews
// ========================================

// Portfolio images: Add/remove objects below
// - src: path to image (local "Real Images/your-image.jpg" or remote URL)
// - alt: description for accessibility
const portfolioImages = [
  { src: "Real Images/Gallery 01.webp", alt: "Bridal mehndi hands with bangles" },
  { src: "Real Images/Gallery 02.webp", alt: "Detailed floral mehndi design" },
  { src: "Real Images/Gallery 03.webp", alt: "Full-coverage mehndi on both hands" },
  { src: "Real Images/Gallery 04.webp", alt: "Bridal mehndi on arms and feet" },
  { src: "Real Images/Gallery 05.webp", alt: "Bride and groom celebrating with henna" },
  { src: "Real Images/Gallery 06.webp", alt: "Bridal mehndi close-up with engagement ring" },
  { src: "Real Images/Gallery 07.webp", alt: "Detailed bridal mehndi on forearms" },
  { src: "Real Images/Gallery 08.webp", alt: "Bridal mehndi portrait" },
  { src: "Real Images/Gallery 09.webp", alt: "Intricate bridal mehndi on forearms" },
  { src: "Real Images/Gallery 10.webp", alt: "Bridal mehndi feet design" },
  { src: "Real Images/Gallery 11.webp", alt: "Elegant bridal mehndi hand design" },
  { src: "Real Images/Gallery 12.webp", alt: "Bride portrait with bridal mehndi and jewelry" },
];

// Reviews: Add/remove objects below
// - text: the review quote (shortened where needed for card length)
// - author: reviewer name
// Sourced from Neena's real Google Business reviews (5.0 stars, 184 reviews)
const reviews = [
  { text: "Neena did henna for my entire wedding party — me, my sister-in-law, my mother-in-law, and even my husband. She worked quickly without ever cutting corners on quality, and it showed in every detail.", author: "Amy T." },
  { text: "Neena walked me through exactly how to prep my skin before and care for it after, and the results were stunning — intricate, beautiful, and the stain came out richer than I expected.", author: "Seema R." },
  { text: "Neena did a fantastic job on our bridal henna. She's fast, incredibly talented, and the color always turns out beautifully — you won't regret booking her.", author: "Liron & Julia" },
  { text: "Neena brought my vision to life with Adinkra symbols, executed with such precision, care, and cultural respect. Every symbol was intentional and beautifully rendered — I left feeling adorned and truly seen.", author: "Desiree A." },
  { text: "My bridal henna was stunning — intricate, detailed, and completely customized to what I wanted. You can tell how much pride she takes in her art.", author: "Tazeen F." },
  { text: "Neena is so talented and easy to work with! I was thrilled with the results and got compliments all weekend on her design.", author: "Emily M." },
  { text: "Neena did henna for me, my mom, and my sister for my wedding — every stain turned out stunning with incredible longevity. She's deliberate, precise, and so much fun to work with.", author: "Ahana W." },
  { text: "Her henna work is absolutely stunning — detailed, precise, and unique. She made the whole experience so enjoyable, and our henna turned out more beautiful than we imagined.", author: "Victoria I." },
  { text: "Neena did my bridal henna and my whole family's. Her attention to detail and patience is unmatched, and she's a wonderful communicator throughout booking.", author: "Tiffany W." },
  { text: "Neena did my henna for my wedding and it was beautiful. Despite the long session, she kept it low-stress and fun — I got so many compliments.", author: "Shreya N." },
  { text: "Neena incorporated everything I wanted — peacock, bells, a puppy paw print — with incredible detail. She made me feel completely comfortable throughout.", author: "Harini S." },
  { text: "A wonderful experience getting my henna done by Neena. Professional, quick, and creative — the color turned out beautifully deep.", author: "Bina J." },
  { text: "Absolutely the best work ever! Her dedication and passion show in every design — wait until the stain sets in, it's stunning.", author: "Abhirayna H." },
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
document.querySelectorAll('.about-header, .about-body, .service-card, .portfolio-header, .reviews-carousel, .contact-header, .faq-header').forEach((el) => el.classList.add('reveal'));

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

if (document.querySelector('.stain-swiper')) {
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const stainSwiper = new Swiper('.stain-swiper', {
  loop: true,
  slidesPerView: 1,
  spaceBetween: 20,
  speed: 420,
  grabCursor: true,
  centeredSlides: false,
  watchSlidesProgress: true,
  autoplay: prefersReducedMotion ? false : {
    delay: 2600,
    disableOnInteraction: false,
  },
  navigation: {
    prevEl: '.stain-prev',
    nextEl: '.stain-next',
  },
  pagination: {
    el: '.stain-stages .swiper-pagination',
    clickable: true,
  },
  breakpoints: {
    640: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    1024: {
      slidesPerView: 3,
      spaceBetween: 22,
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
