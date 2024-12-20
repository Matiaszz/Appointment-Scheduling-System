const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const serviceType = document.getElementById('id_service_type');

menuToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

const switchTheme = document.getElementById('switchTheme');

const buttonThemeDesktop = document.getElementById('buttonThemeDesktop');
const buttonThemeMobile = document.getElementById('buttonThemeMobile');

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

const customServiceType = () => {
    if (serviceType.value === 'custom') {
        const input = document.createElement('input');
        input.type = 'text';
        input.id = 'custom_service';
        input.name = 'custom_service';
        input.placeholder = 'Digite o nome do serviço personalizado';
        input.className = 'p-3 bg-gray-700 text-white rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none w-full mt-2';

        const label = document.createElement('label');
        label.htmlFor = 'custom_service';
        label.innerText = 'Nome do serviço personalizado:';
        label.className = 'text-gray-200 font-semibold mt-4';

        if (!document.getElementById('custom_service')) {
            customServiceDiv.innerHTML = '';
            customServiceDiv.classList.remove('hidden');
            customServiceDiv.classList.add('space-y-4');

            customServiceDiv.appendChild(label);
            customServiceDiv.appendChild(input);
        }

        customServiceDiv.classList.remove('hidden');
    } else {
        customServiceDiv.innerHTML = '';
        customServiceDiv.classList.add('hidden');
    }
}

function filterServices(serviceType) {
    const serviceItems = document.querySelectorAll('.service-item');

    if (serviceType === '') {
        serviceItems.forEach(item => {
            item.style.display = 'block';
        });
    } else {
        serviceItems.forEach(item => {
            if (item.getAttribute('data-service-type') === serviceType) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }
}


function toggleDropdown(dropdownId) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.classList.toggle('hidden');
}

function showDeleteModal() {
    document.getElementById('deleteModal').classList.remove('hidden');
}

function hideDeleteModal() {
    document.getElementById('deleteModal').classList.add('hidden');
}

const dropdownButton = document.getElementById('dropdownButton');
const dropdownMenu = document.getElementById('dropdownMenu');

dropdownButton.addEventListener('click', () => {
    dropdownMenu.classList.toggle('hidden');
});

const closeDropdown = () => {
    dropdownMenu.classList.add('hidden');
};

document.getElementById('closeDropdown').addEventListener('click', closeDropdown);

serviceType.addEventListener('change', customServiceType);
buttonThemeDesktop.addEventListener('click', toggleTheme);
buttonThemeMobile.addEventListener('click', toggleTheme);
