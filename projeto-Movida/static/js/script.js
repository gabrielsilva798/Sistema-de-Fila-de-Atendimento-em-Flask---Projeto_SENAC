// Animação do titulo

const heroTimeline = gsap.timeline({
  delay: 0.1, 
  defaults: {
    duration: 1.1,
    ease: "power3.out",
    opacity: 1,
    y: 0,
  },
});

// Animação da Overlay
heroTimeline.fromTo(
  ".hero-overlay",
  { opacity: 0.4 },
  { opacity: 1, duration: 1.5, ease: "power2.inOut" },
  0
);

// Título: entra primeiro
heroTimeline.to(".hero-content h2", { opacity: 1, y: 0 }, 0.5);

// Parágrafo: entra logo depois do título
heroTimeline.to(".hero-content p", { opacity: 1, y: 0 }, 0.8);

// Botão: entra por último
heroTimeline.to(".hero-content .btn", { opacity: 1, y: 0 }, 1.1);

document.addEventListener("DOMContentLoaded", function () {
  gsap.registerPlugin(ScrollTrigger);

  // ANIMAÇÃO: Efeito de Fade-In-Up para Seções Principais
  const fadeElements = [
    ".visual-data-column",
    ".text-cta-column",
    ".testimonials h2",
    ".testimonial-container",
  ];

  fadeElements.forEach((selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el) => el.classList.add("animar-entrada"));
    elements.forEach((el) => {
      gsap.to(el, {
        opacity: 1,
        y: 0,
        duration: 1.5,
        ease: "power3.out",
        scrollTrigger: {
          trigger: el,
          start: "top 65%",
          toggleActions: "play none none none",
          // markers: true,
        },
      });
    });
  });

  // ANIMAÇÃO: Cards de Serviço
  // Seleciona os cards que terão a animação pela direita
  const serviceCards = gsap.utils.toArray(".service-cards .card");

  // Aplica a classe inicial para todos os cards que vão entrar pela direita
  serviceCards.forEach((card) => card.classList.add("card-animar-direita"));
  const serviceTimeline = gsap.timeline({
    scrollTrigger: {
      trigger: ".services",
      start: "top 60%",
      toggleActions: "play none none none",
      // markers: true,
    },
  });
  serviceTimeline.to(serviceCards, {
    opacity: 1,
    x: 0,
    duration: 0.8,
    ease: "power2.out",
    stagger: 0.2,
  });
});

// ANIMAÇÃO Rodapé (Footer
const footerElements = [
    // As colunas principais
    '.footer-col-info',
    '.footer-col-links',
    '.footer-col-contact',
    '.footer-bottom'
];

// 1. Define o estado inicial (invisível e um pouco abaixo)
footerElements.forEach(selector => {
    gsap.set(selector, {
        opacity: 0,
        y: 30 
    });
});

// 2. Cria a animação de Timeline no ScrollTrigger
gsap.timeline({
    scrollTrigger: {
        trigger: ".main-footer", 
        start: "top 55%",        
        toggleActions: "play none none none",
        // markers: true, 
    }
})
// Anima a entrada sequencial das três colunas do topo
.to('.footer-col-info', { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, 0) 
.to('.footer-col-links', { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, 0.2) 
.to('.footer-col-contact', { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, 0.4)
.to('.footer-bottom p', { opacity: 1, y: 0, duration: 0.8, ease: "power2.out", stagger: 0.1 }, 0.6);