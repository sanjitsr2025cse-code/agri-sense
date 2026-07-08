// ===== Modal Management =====
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "block";
    }
}

function closeModal(modalId = 'trendModal') {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "none";
    }
}

// Close modal when clicking outside of it
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
});

// ===== Price Trend Chart =====
let priceChart = null;

function viewTrend(listingId) {
    openModal('trendModal');
    
    fetch(`/price_trend/${listingId}/`)
        .then(response => response.json())
        .then(data => {
            displayChart(data.chart_data);
            const stats = `
                <strong>Price Statistics (Last 7 Days):</strong><br>
                Min: ₹${data.min_price.toFixed(2)} | 
                Max: ₹${data.max_price.toFixed(2)} | 
                Avg: ₹${data.avg_price.toFixed(2)}
            `;
            document.getElementById('stats').innerHTML = stats;
        })
        .catch(error => {
            console.error('Error fetching price trend:', error);
            alert('Failed to load price trend data.');
        });
}

function displayChart(chartData) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (priceChart) {
        priceChart.destroy();
    }
    
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Price (₹)',
                data: chartData.prices,
                borderColor: '#2ecc71',
                backgroundColor: 'rgba(46, 204, 113, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointBackgroundColor: '#2ecc71',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: { size: 14 },
                        padding: 15
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '₹' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

// ===== Contact Seller =====
function contactSeller(listingId) {
    fetch(`/contact/${listingId}/`)
        .then(response => response.json())
        .then(data => {
            const contactInfo = `
                <h3>Contact Seller</h3>
                <p><strong>Email:</strong> <a href="mailto:${data.email}">${data.email}</a></p>
                <p><strong>Phone:</strong> <a href="tel:${data.phone}">${data.phone}</a></p>
            `;
            document.getElementById('contactModal').innerHTML = contactInfo;
            openModal('contactModal');
        })
        .catch(error => {
            console.error('Error fetching contact info:', error);
            alert('Failed to load seller contact information.');
        });
}

// ===== Search and Filter =====
function filterListings() {
    const searchInput = document.getElementById('searchInput');
    const filterValue = searchInput.value.toLowerCase();
    const listings = document.querySelectorAll('.listing');
    
    listings.forEach(listing => {
        const title = listing.querySelector('.listing-title').textContent.toLowerCase();
        const variety = listing.querySelector('.listing-variety').textContent.toLowerCase();
        
        if (title.includes(filterValue) || variety.includes(filterValue)) {
            listing.style.display = '';
        } else {
            listing.style.display = 'none';
        }
    });
}

// Real-time search as user types
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', filterListings);
}

// ===== Sort Listings =====
function sortListings(sortBy) {
    const listingsContainer = document.querySelector('.listings');
    const listings = Array.from(document.querySelectorAll('.listing'));
    
    listings.sort((a, b) => {
        let aValue, bValue;
        
        if (sortBy === 'price-low') {
            aValue = parseFloat(a.querySelector('.listing-price').textContent.replace('₹', ''));
            bValue = parseFloat(b.querySelector('.listing-price').textContent.replace('₹', ''));
            return aValue - bValue;
        } else if (sortBy === 'price-high') {
            aValue = parseFloat(a.querySelector('.listing-price').textContent.replace('₹', ''));
            bValue = parseFloat(b.querySelector('.listing-price').textContent.replace('₹', ''));
            return bValue - aValue;
        } else if (sortBy === 'newest') {
            // This would require a data attribute with creation date
            return 0;
        }
    });
    
    listings.forEach(listing => listingsContainer.appendChild(listing));
}

// ===== Logout Handler =====
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = '/logout/';
    }
}

// ===== Form Validation =====
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            input.style.borderColor = '#ecf0f1';
        }
    });
    
    return isValid;
}

// ===== Initialize Page =====
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add loading state to buttons on form submit
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Loading...';
            }
        });
    });
});

// ===== Utility Functions =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: ${type === 'success' ? '#2ecc71' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 3000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ===== Animations =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
