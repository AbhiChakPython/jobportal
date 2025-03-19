document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded script loaded successfully');

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(event) {
            event.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                window.scrollTo({
                top: targetElement.offsetTop,
                behavior:'smooth'
                });
            }
        });
    });
});