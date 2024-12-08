const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');

menuToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

const switchTheme = document.getElementById('switchTheme');
const buttonTheme = document.getElementById('buttonTheme');
buttonTheme.addEventListener('click', () => {
    if (switchTheme.classList.contains('bg-zinc-900')){
        switchTheme.classList.remove('bg-zinc-900');
        switchTheme.classList.add('bg-gray-100');
        return;
    }
    switchTheme.classList.remove('bg-gray-100');
    switchTheme.classList.add('bg-zinc-900');
})