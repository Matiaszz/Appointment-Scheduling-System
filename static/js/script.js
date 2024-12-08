const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');

menuToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

const switchTheme = document.getElementById('switchTheme');

// Selecione os dois botões "Trocar Tema" com os novos IDs
const buttonThemeDesktop = document.getElementById('buttonThemeDesktop');
const buttonThemeMobile = document.getElementById('buttonThemeMobile');

// Função para alternar os temas
const toggleTheme = () => {
    if (switchTheme.classList.contains('bg-zinc-900')) {
        switchTheme.classList.remove('bg-zinc-900');
        switchTheme.classList.remove('text-white');
        switchTheme.classList.add('bg-gray-100');
        switchTheme.classList.add('text-black');
        return;
    } 
    switchTheme.classList.remove('bg-gray-100');
    switchTheme.classList.remove('text-black');
    switchTheme.classList.add('bg-zinc-900');
    switchTheme.classList.add('text-white');
    
}

buttonThemeDesktop.addEventListener('click', toggleTheme);
buttonThemeMobile.addEventListener('click', toggleTheme);
