// Smooth scroll for in-page anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (e) => {
    const targetId = anchor.getAttribute('href');
    if (targetId.length <= 1) return;
    const target = document.querySelector(targetId);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Nav shadow on scroll
const nav = document.getElementById('mainNav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('is-scrolled', window.scrollY > 40);
});

// Portfolio carousel controls
const carousel = document.getElementById('carousel');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

function carouselScrollAmount() {
  const item = carousel.querySelector('.carousel-item');
  return item ? item.getBoundingClientRect().width + 16 : 300;
}

prevBtn.addEventListener('click', () => {
  carousel.scrollBy({ left: -carouselScrollAmount(), behavior: 'smooth' });
});
nextBtn.addEventListener('click', () => {
  carousel.scrollBy({ left: carouselScrollAmount(), behavior: 'smooth' });
});

// Booking calendar — visual-only day selection
const calendarGrid = document.getElementById('calendarGrid');
const timeLabel = document.getElementById('timeLabel');

calendarGrid.querySelectorAll('.calendar-day').forEach((day) => {
  if (day.classList.contains('is-muted') || day.classList.contains('is-unavailable')) return;
  day.addEventListener('click', () => {
    calendarGrid.querySelectorAll('.calendar-day').forEach((d) => d.classList.remove('is-selected'));
    day.classList.add('is-selected');
    timeLabel.textContent = `Available Times (Oct ${day.textContent.trim()})`;
  });
});

// Booking — visual-only time slot selection (desktop button variant)
const timeSlots = document.getElementById('timeSlots');
timeSlots.querySelectorAll('button').forEach((btn) => {
  btn.addEventListener('click', () => {
    timeSlots.querySelectorAll('button').forEach((b) => b.classList.remove('is-selected'));
    btn.classList.add('is-selected');
  });
});

// Reveal-on-scroll for section content
const revealTargets = document.querySelectorAll('.service-card, .about-inner, .booking-card, .location-inner');
revealTargets.forEach((el) => el.classList.add('reveal'));

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

revealTargets.forEach((el) => observer.observe(el));
