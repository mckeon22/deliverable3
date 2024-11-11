// Dropdown Toggle for Both Mouse and Keyboard
document.querySelectorAll('.dropdown button').forEach(button => {
    button.addEventListener('click', () => {
        toggleDropdown(button);
    });

    button.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleDropdown(button);
        }
    });
});

function toggleDropdown(button) {
    const dropdown = button.nextElementSibling;
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', !isExpanded);
    dropdown.style.display = isExpanded ? 'none' : 'block';

    // Focus first item in the dropdown if expanded
    if (!isExpanded) {
        dropdown.querySelector('a').focus();
    }
}

// Close Dropdown on Click Outside or on Escape Key
document.addEventListener('click', function(event) {
    const dropdowns = document.querySelectorAll('.dropdown-content');
    dropdowns.forEach(dropdown => {
        const button = dropdown.previousElementSibling;
        if (!button.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.style.display = 'none';
            button.setAttribute('aria-expanded', 'false');
        }
    });
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.dropdown-content').forEach(dropdown => {
            dropdown.style.display = 'none';
            dropdown.previousElementSibling.setAttribute('aria-expanded', 'false');
        });
    }
});

// Back to Top Button Functionality
const backToTopButton = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        backToTopButton.style.display = 'block';
    } else {
        backToTopButton.style.display = 'none';
    }
});
backToTopButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

backToTopButton.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

// Filtering Functionality for Sorting Options
document.getElementById('sortFilter').addEventListener('change', (e) => {
    const sortBy = e.target.value;
    const container = document.getElementById('results-container');
    const athletes = Array.from(container.querySelectorAll('.athlete'));

    athletes.sort((a, b) => {
        if (sortBy === 'time') {
            return a.getAttribute('data-time').localeCompare(b.getAttribute('data-time'));
        } else if (sortBy === 'alphabetical') {
            return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
        } else if (sortBy === 'team') {
            return a.getAttribute('data-team').localeCompare(b.getAttribute('data-team'));
        } else {
            return 0;
        }
    });

   // Reorder the athletes' elements displayed on the page.

    athletes.forEach(athlete => container.appendChild(athlete));
});
