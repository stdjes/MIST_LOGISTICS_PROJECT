function loadPage(page) {
    const mainContent = document.getElementById('mainContent');
    
    // Clear previous content
    mainContent.innerHTML = '';

    // Load content based on the selected page
    switch (page) {
        case 'overview':
            // Example AJAX request to load My Shipments content
            fetch('overview')
                .then(response => response.text())
                .then(data => {
                    mainContent.innerHTML = data;
                })
                .catch(error => console.error('Error fetching data:', error));
            break;

        case 'shipments':
            // Example AJAX request to load My Shipments content
            fetch('shipments')
                .then(response => response.text())
                .then(data => {
                    mainContent.innerHTML = data;
                })
                .catch(error => console.error('Error fetching data:', error));
            break;
        case 'create':
            // Example AJAX request to load Create Shipment content
            fetch('create_shipment')
                .then(response => response.text())
                .then(data => {
                    mainContent.innerHTML = data;
                })
                .catch(error => console.error('Error fetching data:', error));
            break;
        case 'invoices':
            // Example AJAX request to load Invoices content
            fetch('invoices')
                .then(response => response.text())
                .then(data => {
                    mainContent.innerHTML = data;
                })
                .catch(error => console.error('Error fetching data:', error));
            break;
        case 'support':
            // Example AJAX request to load Support content
            fetch('support')
                .then(response => response.text())
                .then(data => {
                    mainContent.innerHTML = data;
                })
                .catch(error => console.error('Error fetching data:', error));
            break;
        case 'settings':
            // Example AJAX request to load Settings content
            fetch('settings')
                .then(response => response.text())
                .then(data => {
                    mainContent.innerHTML = data;
                })
                .catch(error => console.error('Error fetching data:', error));
            break;
        default:
            mainContent.innerHTML = `<section><h2>Page not found</h2></section>`;
            break;
    }

    // Optionally, you can add additional logic here such as handling loading indicators or errors.
}

document.addEventListener('DOMContentLoaded', function() {
    loadPage('overview'); // Load 'overview' page by default
});


function setActiveLink(page) {
    var links = document.querySelectorAll('.sidebar ul li a');
    links.forEach(function(link) {
        link.classList.remove('active');
        if (link.getAttribute('onclick').includes(page)) {
            link.classList.add('active');
        }
    });
}

function logout() {
    // Perform logout functionality, e.g., clearing session, redirecting to login page
    console.log('Logging out...');
    // Example: Redirect to login page
    window.location.href = '../login';
}
