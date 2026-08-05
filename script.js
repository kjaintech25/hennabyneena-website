// ========================================
// CAROUSEL DATA — Edit these arrays to change images/reviews
// ========================================

// Gallery carousels: one entry per carousel on gallery.html
// - id: must match the data-collection attribute on the markup block
// - dir: folder holding the images
// - count: how many images, named <id>-01.webp … <id>-NN.webp
// - alt: accessibility description (image number is appended automatically)
// To add photos: drop <id>-NN.webp in the folder and bump count.
const galleryCollections = [
  { id: "bridal",  dir: "Real Images/Gallery/bridal",  count: 16, alt: "Bridal mehndi design by Neena Jain" },
  { id: "feet",    dir: "Real Images/Gallery/feet",    count: 15, alt: "Feet mehndi design by Neena Jain" },
  { id: "stylish", dir: "Real Images/Gallery/stylish", count: 17, alt: "Stylish henna design by Neena Jain" },
  { id: "party",   dir: "Real Images/Gallery/party",   count: 18, alt: "Party henna design by Neena Jain" },
  { id: "guest",   dir: "Real Images/Gallery/guest",   count: 13, alt: "Event guest henna by Neena Jain" },
  { id: "family",  dir: "Real Images/Gallery/family",  count: 15, alt: "Family henna by Neena Jain" },
  { id: "jagua",   dir: "Real Images/Gallery/jagua",   count: 23, alt: "Jagua body art by Neena Jain" },
  { id: "white",   dir: "Real Images/Gallery/white",   count: 4,  alt: "White henna design by Neena Jain" },
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

// Swiper's loop needs roughly 2x the visible slides to build its buffer. At
// desktop width ~3 slides show, so a carousel with only a handful of photos
// silently stops advancing. Repeat the set until there are enough — a loop
// shows the same photos round and round anyway.
const MIN_SLIDES_FOR_LOOP = 8;

galleryCollections.forEach(({ id, dir, count, alt }) => {
  const block = document.querySelector(`.gallery-collection[data-collection="${id}"]`);
  if (!block) return;
  const wrapper = block.querySelector('.gallery-wrapper');
  if (!wrapper) return;

  const total = count < MIN_SLIDES_FOR_LOOP
    ? Math.ceil(MIN_SLIDES_FOR_LOOP / count) * count
    : count;

  for (let i = 0; i < total; i++) {
    const n = (i % count) + 1;
    const isRepeat = i >= count;
    const src = `${dir}/${id}-${String(n).padStart(2, '0')}.webp`;
    const slide = document.createElement('div');
    slide.className = 'swiper-slide';
    // src is withheld until the slide is actually needed — see hydrateWindow().
    // Native loading="lazy" can't be used here; it's unreliable inside a Swiper
    // (see CLAUDE_MEMORY.md), so the loading window is managed explicitly.
    slide.innerHTML = isRepeat
      ? `<img data-src="${src}" alt="" aria-hidden="true" decoding="async">`
      : `<img data-src="${src}" alt="${alt} (${n} of ${count})" decoding="async">`;
    wrapper.appendChild(slide);
  }
});

// ========================================
// Gallery image loading
// ========================================
// Loading all 85 gallery images up front costs ~11MB and, worse, ~385MB of
// decoded bitmap held in memory at once — enough to make scrolling crawl on a
// phone. Instead each carousel loads only a window of slides around the one
// you're looking at, and loads nothing at all until it scrolls near the
// viewport.
const HYDRATE_BEHIND = 3;
const HYDRATE_AHEAD = 6;

function hydrate(img) {
  if (!img || !img.dataset.src) return;
  // Slides start transparent and fade in once decoded, so a photo arriving
  // mid-scroll eases in rather than snapping into place.
  const reveal = () => img.classList.add('is-loaded');
  img.addEventListener('load', reveal, { once: true });
  img.addEventListener('error', reveal, { once: true });
  img.src = img.dataset.src;
  delete img.dataset.src;
  if (img.complete) reveal(); // already in cache — no load event coming
}

// Initialising a looping Swiper fires slideChange as it positions itself, which
// would otherwise load every carousel on the page before any of them is in view.
const activatedCarousels = new WeakSet();

function hydrateWindow(swiper) {
  if (!activatedCarousels.has(swiper)) return;
  const slides = swiper.slides;
  const n = slides.length;
  if (!n) return;
  for (let offset = -HYDRATE_BEHIND; offset <= HYDRATE_AHEAD; offset++) {
    const i = ((swiper.activeIndex + offset) % n + n) % n;
    hydrate(slides[i] && slides[i].querySelector('img'));
  }
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

// Every scroll-driven read below (scrollHeight, offsetTop, offsetHeight) forces
// the browser to recalculate layout. Firing them on each of the dozens of scroll
// events per second is what makes a long page feel sticky, so they share one
// handler that runs at most once per animation frame.
let scrollTicking = false;

function onScrollFrame() {
  scrollTicking = false;
  const scrollY = window.scrollY;

  nav.classList.toggle('is-scrolled', scrollY > 40);

  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;
  scrollProgress.style.width = progress + '%';

  scrollSpy();
  if (backToTop) backToTop.classList.toggle('is-visible', scrollY > 600);
  hydrateNearbyCollections(); // no-op off the gallery page
}

window.addEventListener('scroll', () => {
  if (scrollTicking) return;
  scrollTicking = true;
  requestAnimationFrame(onScrollFrame);
}, { passive: true });

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
// A carousel loads its first images once it's within this many pixels of the
// viewport. Checked explicitly against getBoundingClientRect rather than with
// IntersectionObserver, so the trigger point is predictable and testable.
const HYDRATE_MARGIN_PX = 600;
const pendingCollections = [];

// window.innerHeight can still read 0 when this first runs (layout not settled,
// web fonts not swapped in yet). Falling back to 0 would collapse the threshold
// and leave even the top carousel unloaded until the first scroll, so assume a
// typical viewport until a real measurement is available.
function viewportHeight() {
  return window.innerHeight || document.documentElement.clientHeight || 800;
}

function hydrateNearbyCollections() {
  const vh = viewportHeight();
  for (let i = pendingCollections.length - 1; i >= 0; i--) {
    const { block, swiper } = pendingCollections[i];
    const rect = block.getBoundingClientRect();
    const near = rect.top < vh + HYDRATE_MARGIN_PX && rect.bottom > -HYDRATE_MARGIN_PX;
    if (!near) continue;
    activatedCarousels.add(swiper);
    hydrateWindow(swiper); // slideChange keeps it topped up from here
    pendingCollections.splice(i, 1);
  }
}

// One Swiper per gallery collection, each wired to its own arrows and dots
document.querySelectorAll('.gallery-collection').forEach((block) => {
  const el = block.querySelector('.portfolio-swiper');
  if (!el) return;
  const swiper = new Swiper(el, {
    loop: true,
    slidesPerView: 'auto',
    spaceBetween: 18,
    speed: 420,
    grabCursor: true,
    centeredSlides: false,
    watchSlidesProgress: true,
    navigation: {
      prevEl: block.querySelector('.gallery-prev'),
      nextEl: block.querySelector('.gallery-next'),
    },
    pagination: {
      el: block.querySelector('.gallery-pagination'),
      clickable: true,
      // Stylish has 26 slides — a full bullet row would overflow on mobile
      dynamicBullets: true,
      dynamicMainBullets: 3,
    },
    resistance: true,
    resistanceRatio: 0.6,
    on: {
      slideChange() { hydrateWindow(this); },
      resize() { hydrateWindow(this); },
    },
  });

  pendingCollections.push({ block, swiper });
});

hydrateNearbyCollections();

// Positions shift as fonts swap in and images settle, so re-check once the page
// has fully loaded and whenever it's resized. Scrolling already triggers this
// via onScrollFrame.
window.addEventListener('load', hydrateNearbyCollections);
window.addEventListener('resize', hydrateNearbyCollections, { passive: true });

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
  // Read the hero height once instead of on every scroll event
  let heroHeight = hero.offsetHeight;
  window.addEventListener('resize', () => { heroHeight = hero.offsetHeight; }, { passive: true });

  let heroTicking = false;
  window.addEventListener('scroll', () => {
    if (heroTicking) return;
    heroTicking = true;
    requestAnimationFrame(() => {
      heroTicking = false;
      const scrolled = window.scrollY;
      // Only parallax while hero is visible
      if (scrolled < heroHeight) {
        const speed = 0.3; // Subtle — 30% of scroll speed
        heroBg.style.transform = `translateY(${scrolled * speed}px)`;
      }
    });
  }, { passive: true });
}

// Back to top button — visibility is handled in onScrollFrame above
const backToTop = document.getElementById('backToTop');

onScrollFrame();

document.getElementById('year').textContent = new Date().getFullYear();

// FAQ category accordion — groups start collapsed, one open at a time
// ========================================
// FAQ — collapsible categories, each holding collapsible questions
// ========================================

function setFaqItemOpen(item, open) {
  item.classList.toggle('is-open', open);
  item.querySelector('.faq-question').setAttribute('aria-expanded', String(open));
}

function setFaqGroupOpen(group, open) {
  group.classList.toggle('is-open', open);
  group.querySelector('.faq-group-toggle').setAttribute('aria-expanded', String(open));
  if (!open) {
    // Reset the questions inside so the category reopens clean
    group.querySelectorAll('.faq-item.is-open').forEach((item) => setFaqItemOpen(item, false));
  }
}

document.querySelectorAll('.faq-group-toggle').forEach((btn) => {
  btn.addEventListener('click', () => {
    const group = btn.closest('.faq-group');
    const isOpen = group.classList.contains('is-open');
    document.querySelectorAll('.faq-group.is-open').forEach((g) => setFaqGroupOpen(g, false));
    if (!isOpen) setFaqGroupOpen(group, true);
  });
});

document.querySelectorAll('.faq-question').forEach((btn) => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('is-open');

    document.querySelectorAll('.faq-item.is-open').forEach((openItem) => {
      if (openItem !== item) setFaqItemOpen(openItem, false);
    });

    setFaqItemOpen(item, !isOpen);
  });
});
