document.querySelector('.cta-button').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('api-section').scrollIntoView({
        behavior: 'smooth'
    });
});