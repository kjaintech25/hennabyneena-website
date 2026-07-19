// ========================================
// CAROUSEL DATA — Edit these arrays to change images/reviews
// ========================================

// Portfolio images: Add/remove objects below
// - src: path to image (local "Real Images/your-image.jpg" or remote URL)
// - alt: description for accessibility
const portfolioImages = [
  { src: "https://images.unsplash.com/photo-1606800052052-a08af7148866?w=800&q=80", alt: "Bridal mehndi detail" },
  { src: "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800&q=80", alt: "Intricate hand mehndi" },
  { src: "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&q=80", alt: "Mehndi process" },
  { src: "https://images.unsplash.com/photo-1507504031003-b417219a0fde?w=800&q=80", alt: "Groom's hand mehndi" },
  { src: "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800&q=80", alt: "Ceremonial hands" },
  { src: "https://images.unsplash.com/photo-1529636798458-92182e662485?w=800&q=80", alt: "Floral mehndi" },
  { src: "https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=800&q=80", alt: "Party henna session" },
  { src: "https://images.unsplash.com/photo-1544457070-4cd773b4d71e?w=800&q=80", alt: "Jagua shoulder" },
];

// Reviews: Add/remove objects below
// - text: the review quote
// - author: reviewer name
const reviews = [
  { text: "Neena's bridal mehndi was exquisite. Every guest asked who did my hands. The patterns were personal, delicate, and stayed beautiful for over a week.", author: "Priya R." },
  { text: "I've worked with many henna artists, but Neena's organic paste and steady hand are unmatched. Her studio is warm, calm, and truly professional.", author: "Amina S." },
  { text: "We booked Neena for our wedding party and she made every guest feel special. Fast, beautiful designs and the aftercare tips were invaluable.", author: "Mira K." },
  { text: "The jagua design was stunning—dark, crisp, and exactly what I wanted without the commitment of a tattoo. Will book again.", author: "Zara H." },
  { text: "Neena came to our Eid gathering and created the most delicate patterns for my mother and grandmother. It felt like a blessing, not just an appointment.", author: "Layla M." },
  { text: "From consultation to final reveal, the experience was first-class. She understood my vision and made it even better on the wedding day.", author: "Riya D." },
  { text: "My jagua tattoo lasted beautifully and the removal instructions were easy. Totally worth every minute and penny.", author: "Sophia T." },
  { text: "Professional, patient, and precise. Neena took time to adjust the design for my sensitive skin and the result was flawless.", author: "Anika P." },
  { text: "Best mehendi in the Triangle area, hands down. I keep getting compliments weeks later.", author: "Deepa S." },
  { text: "I love supporting local artists who care about purity and craft. Neena's organic paste smelled amazing and the designs were unforgettable.", author: "Kavya R." },
];

// ========================================
// Populate carousels from data above
// ========================================

const portfolioWrapper = document.getElementById('portfolioWrapper');
portfolioImages.forEach(({ src, alt }) => {
  const slide = document.createElement('div');
  slide.className = 'swiper-slide';
  slide.innerHTML = `<img src="${src}" alt="${alt}" loading="lazy">`;
  portfolioWrapper.appendChild(slide);
});

const reviewsWrapper = document.getElementById('reviewsWrapper');
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
