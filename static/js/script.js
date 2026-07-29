// Global JavaScript for Family Tree Application

// Toast Notification Function
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        setTimeout(() => alertDiv.remove(), 5000);
    }
}

// Confirm Delete Action
function confirmDelete(message = 'Are you sure you want to delete this?') {
    return confirm(message);
}

// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add loading state to form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitButton && !submitButton.dataset.originalText) {
            submitButton.dataset.originalText = submitButton.innerHTML;
        }

        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');

                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.innerHTML = submitButton.dataset.originalText || submitButton.innerHTML;
                }
                return;
            }

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Loading...`;
            }
        }, false);
    });

    // Dropdown toggle functionality
    const dropdownButtons = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
        });
    });

    // Search form enhancement
    const searchForm = document.querySelector('form[action*="/search"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        if (searchInput) {
            searchInput.addEventListener('keyup', function(e) {
                if (e.key === 'Enter') {
                    searchForm.submit();
                }
            });
        }
    }

    // Photo upload preview
    const photoInputs = document.querySelectorAll('input[name="photo"]');
    photoInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const preview = document.querySelector('.image-preview');
                    if (preview) {
                        preview.src = event.target.result;
                    }
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // Modal confirmations
    const deleteButtons = document.querySelectorAll('.btn-delete, [data-action="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
});

// Format date to readable format
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Calculate age from date
function calculateAge(birthDate) {
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    
    return age;
}

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showNotification('Failed to copy', 'danger');
    });
}

// Export table to CSV
function exportTableToCSV(filename = 'export.csv') {
    const table = document.querySelector('table');
    if (!table) {
        showNotification('No table found', 'danger');
        return;
    }

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvrow = [];
        cols.forEach(col => {
            csvrow.push('"' + col.innerText.replace(/"/g, '""') + '"');
        });
        csv.push(csvrow.join(','));
    });

    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.getAttribute('data-src');
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.getAttribute('data-src');
            img.removeAttribute('data-src');
        });
    }
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Real-time search
function initializeRealtimeSearch() {
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        const debouncedSearch = debounce(function(e) {
            const query = e.target.value.trim();
            if (query.length > 2) {
                // You can add real-time search here
                console.log('Searching for:', query);
            }
        }, 300);

        searchInput.addEventListener('keyup', debouncedSearch);
    }
}

// Print page function
function printPage() {
    window.print();
}

// Go back function
function goBack() {
    window.history.back();
}

// Reload page
function reloadPage() {
    location.reload();
}

// Initialize all on page load
window.addEventListener('load', function() {
    initializeTooltips();
    lazyLoadImages();
    initializeRealtimeSearch();
});

// Export functions globally
window.Family = {
    showNotification,
    confirmDelete,
    copyToClipboard,
    exportTableToCSV,
    formatDate,
    calculateAge,
    printPage,
    goBack,
    reloadPage
};
