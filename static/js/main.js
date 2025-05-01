// main.js - Main JavaScript for the application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile navigation toggle
    initMobileNav();
    
    // Initialize sidebar dropdowns
    initSidebarDropdowns();
    
    // Initialize topbar dropdowns
    initTopbarDropdowns();
    
    // Initialize flash message auto-dismiss
    initFlashMessages();
    
    // Initialize filter form functionality
    initFilterForms();
});

// Initialize mobile navigation
function initMobileNav() {
    const mobileToggle = document.querySelector('.topbar-mobile-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
}

// Initialize sidebar dropdowns
function initSidebarDropdowns() {
    const dropdownItems = document.querySelectorAll('.sidebar-item-dropdown');
    
    dropdownItems.forEach(item => {
        const link = item.querySelector('.sidebar-link');
        const dropdown = item.querySelector('.sidebar-dropdown');
        const toggle = item.querySelector('.sidebar-toggle');
        
        if (link && dropdown) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                dropdown.classList.toggle('active');
                if (toggle) {
                    toggle.classList.toggle('active');
                }
            });
        }
    });
}

// Initialize topbar dropdown menus
function initTopbarDropdowns() {
    const dropdownItems = document.querySelectorAll('.topbar-nav-item.dropdown');
    
    dropdownItems.forEach(item => {
        const toggle = item.querySelector('.topbar-nav-icon');
        const dropdown = item.querySelector('.topbar-dropdown');
        
        if (toggle && dropdown) {
            toggle.addEventListener('click', function(e) {
                e.stopPropagation();
                dropdown.classList.toggle('active');
            });
            
            // Close when clicking outside
            document.addEventListener('click', function() {
                dropdown.classList.remove('active');
            });
            
            // Prevent closing when clicking inside the dropdown
            dropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    });
}

// Initialize flash messages auto-dismiss
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000);
    });
}

// Initialize filter form functionality
function initFilterForms() {
    const filterForms = document.querySelectorAll('.filter-form');
    
    filterForms.forEach(form => {
        const resetBtn = form.querySelector('.filter-reset');
        
        if (resetBtn) {
            resetBtn.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Reset all form inputs
                const inputs = form.querySelectorAll('input, select');
                inputs.forEach(input => {
                    if (input.type === 'checkbox' || input.type === 'radio') {
                        input.checked = false;
                    } else {
                        input.value = '';
                    }
                });
            });
        }
    });
}

// Format currency values
function formatCurrency(value) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
    }).format(value);
}

// Format percentage values
function formatPercentage(value) {
    return value + '%';
}

// Format date values
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-MX', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Toggle sidebar collapse
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const contentArea = document.querySelector('.content-area');
    
    if (sidebar && contentArea) {
        sidebar.classList.toggle('sidebar-collapsed');
        contentArea.style.marginLeft = sidebar.classList.contains('sidebar-collapsed') ? '70px' : '250px';
    }
}

// Handle notifications
function markNotificationAsRead(notificationId) {
    // In a real application, this would make an API call
    console.log('Marked notification as read:', notificationId);
    
    // Update UI
    const notification = document.querySelector(`[data-notification-id="${notificationId}"]`);
    if (notification) {
        notification.classList.add('notification-read');
    }
    
    // Update badge count
    const badge = document.querySelector('.topbar-badge');
    if (badge) {
        let count = parseInt(badge.textContent) - 1;
        if (count <= 0) {
            badge.style.display = 'none';
        } else {
            badge.textContent = count;
        }
    }
}

// Function to toggle chart fullscreen mode
function toggleChartFullscreen(chartId) {
    const chartCard = document.getElementById(chartId).closest('.chart-card');

    if (chartCard) {
        const isFullscreen = chartCard.classList.toggle('chart-fullscreen');

        if (isFullscreen) {
            // Create overlay
            const overlay = document.createElement('div');
            overlay.className = 'chart-fullscreen-overlay';
            document.body.appendChild(overlay);

            // Position the chart
            chartCard.style.position = 'fixed';
            chartCard.style.top = '50%';
            chartCard.style.left = '50%';
            chartCard.style.transform = 'translate(-50%, -50%)';
            chartCard.style.width = '90%';
            chartCard.style.height = '80%';
            chartCard.style.zIndex = '1100';

            // Create close button
            const closeBtn = document.createElement('button');
            closeBtn.className = 'chart-fullscreen-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.onclick = function() {
                toggleChartFullscreen(chartId);
            };
            chartCard.appendChild(closeBtn);

            // Refresh chart if needed
            if (window.Chart) {
                const chartInstance = Chart.getChart(chartId);
                if (chartInstance) {
                    setTimeout(() => {
                        chartInstance.resize();
                    }, 100);
                }
            }
        } else {
            // Remove overlay
            const overlay = document.querySelector('.chart-fullscreen-overlay');
            if (overlay) {
                overlay.remove();
            }

            // Reset chart position
            chartCard.style.position = '';
            chartCard.style.top = '';
            chartCard.style.left = '';
            chartCard.style.transform = '';
            chartCard.style.width = '';
            chartCard.style.height = '';
            chartCard.style.zIndex = '';

            // Remove close button
            const closeBtn = chartCard.querySelector('.chart-fullscreen-close');
            if (closeBtn) {
                closeBtn.remove();
            }

            // Refresh chart if needed
            if (window.Chart) {
                const chartInstance = Chart.getChart(chartId);
                if (chartInstance) {
                    setTimeout(() => {
                        chartInstance.resize();
                    }, 100);
                }
            }
        }
    }
}