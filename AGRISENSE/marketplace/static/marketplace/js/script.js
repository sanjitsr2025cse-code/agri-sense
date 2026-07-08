let chart;

function viewTrend(listingId) {
    fetch(`/price_trend/${listingId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('trendModal').style.display = 'block';
            const ctx = document.getElementById('priceChart').getContext('2d');
            if (chart) {
                chart.destroy();
            }
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.chart_data.labels,
                    datasets: [{
                        label: 'Average Price',
                        data: data.chart_data.prices,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            document.getElementById('stats').innerText = `Min: ₹${data.min_price}, Max: ₹${data.max_price}, Avg: ₹${data.avg_price}`;
        });
}

function contactSeller(listingId) {
    fetch(`/contact/${listingId}/`)
        .then(response => response.json())
        .then(data => {
            alert(`Phone: ${data.phone}\nEmail: ${data.email}`);
        });
}

function closeModal() {
    document.getElementById('trendModal').style.display = 'none';
}