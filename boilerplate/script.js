const root = document.documentElement;
const hero = document.querySelector(".hero");

let targetMouseX = 0;
let targetMouseY = 0;
let currentMouseX = 0;
let currentMouseY = 0;
let targetScroll = 0;
let currentScroll = 0;
let rafId = 0;
let isPointerInside = false;

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const startTime = performance.now();

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function readScrollProgress() {
  if (!hero) {
    return 0;
  }

  const rect = hero.getBoundingClientRect();
  const scrollable = Math.max(1, rect.height - window.innerHeight);
  return clamp(-rect.top / scrollable, 0, 1);
}

function render() {
  const lerp = prefersReducedMotion ? 1 : 0.12;
  const elapsed = (performance.now() - startTime) / 1000;

  currentMouseX += (targetMouseX - currentMouseX) * lerp;
  currentMouseY += (targetMouseY - currentMouseY) * lerp;
  currentScroll += (targetScroll - currentScroll) * lerp;

  root.style.setProperty("--mouse-x", currentMouseX.toFixed(4));
  root.style.setProperty("--mouse-y", currentMouseY.toFixed(4));
  root.style.setProperty("--scroll-progress", currentScroll.toFixed(4));
  root.style.setProperty("--float-a", prefersReducedMotion ? "0" : Math.sin(elapsed * 0.72).toFixed(4));
  root.style.setProperty("--float-b", prefersReducedMotion ? "0" : Math.cos(elapsed * 0.53).toFixed(4));

  const isMoving =
    Math.abs(targetMouseX - currentMouseX) > 0.001 ||
    Math.abs(targetMouseY - currentMouseY) > 0.001 ||
    Math.abs(targetScroll - currentScroll) > 0.001 ||
    (!prefersReducedMotion && isPointerInside);

  if (isMoving) {
    rafId = requestAnimationFrame(render);
  } else {
    rafId = 0;
  }
}

function requestRender() {
  targetScroll = readScrollProgress();

  if (!rafId) {
    rafId = requestAnimationFrame(render);
  }
}

window.addEventListener("scroll", requestRender, { passive: true });
window.addEventListener("resize", requestRender);

window.addEventListener("pointermove", (event) => {
  const width = window.innerWidth || 1;
  const height = window.innerHeight || 1;
  isPointerInside = true;
  targetMouseX = (event.clientX / width - 0.5) * 2;
  targetMouseY = (event.clientY / height - 0.5) * 2;
  requestRender();
}, { passive: true });

window.addEventListener("pointerleave", () => {
  isPointerInside = false;
  targetMouseX = 0;
  targetMouseY = 0;
  requestRender();
});

requestRender();
