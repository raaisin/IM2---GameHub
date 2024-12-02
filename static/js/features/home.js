let carouselIndex = 0;
const carouselImages = [
    "{% static 'images/wildsale.jpg' %}",
    "{% static 'images/hugesale.jpg' %}"
];

function updateCarousel() {
    document.querySelector('.carousel img').src = carouselImages[carouselIndex];
}

document.addEventListener('DOMContentLoaded', function () {
    updateCarousel();
    setInterval(() => {
        carouselIndex = (carouselIndex + 1) % carouselImages.length;
        updateCarousel();
    }, 3000);
});

function moveCarousel(n) {
    carouselIndex += n;
    if (carouselIndex >= carouselImages.length) {
        carouselIndex = 0;
    } else if (carouselIndex < 0) {
        carouselIndex = carouselImages.length - 1;
    }
    updateCarousel();
}

function scrollCategories(direction) {
    const container = document.querySelector('.category-grid');
    const scrollAmount = 400; 
    
    if (direction === 'left') {
        container.scrollBy({
            left: -scrollAmount,
            behavior: 'smooth'
        });
    } else {
        container.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });
    }
}

function updateScrollButtons() {
    const container = document.querySelector('.category-grid');
    const leftBtn = document.querySelector('.scroll-left');
    const rightBtn = document.querySelector('.scroll-right');
    
    if (container.scrollLeft >= container.scrollWidth - container.clientWidth) {
        rightBtn.style.opacity = '0.5';
    } else {
        rightBtn.style.opacity = '1';
    }
}

document.querySelector('.category-grid').addEventListener('scroll', updateScrollButtons);

document.addEventListener('DOMContentLoaded', function() {
    updateScrollButtons();
    updateCarousel();
    setInterval(() => {
        carouselIndex = (carouselIndex + 1) % carouselImages.length;
        updateCarousel();
    }, 3000);
});

   