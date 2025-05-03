if (localStorage.getItem('dark-mode') === 'true') {
    document.body.classList.add('dark-mode');
    document.getElementById('toggle-theme').querySelector('i').classList.replace('fa-sun', 'fa-moon');
    document.getElementById('logo').src = '/static/Images/Smart-chekad-logo-dark-theme.png';
} else {
    document.getElementById('logo').src = '/static/Images/Smart-chekad-logo.png';
}

document.getElementById('toggle-theme').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    
    const icon = this.querySelector('i');
    
    if (document.body.classList.contains('dark-mode')) {
        icon.classList.replace('fa-sun', 'fa-moon');
        localStorage.setItem('dark-mode', 'true');
        document.getElementById('logo').src = '/static/Images/Smart-chekad-logo-dark-theme.png';
    } else {
        icon.classList.replace('fa-moon', 'fa-sun');
        localStorage.setItem('dark-mode', 'false');
        document.getElementById('logo').src = '/static/Images/Smart-chekad-logo.png';
    }
});

