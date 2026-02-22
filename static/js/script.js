/**
 * Smart Classroom System - Global Frontend Logic
 * Handles sidebar toggling, live attendance feeds, analytics, popups, and activity tracking.
 */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Mobile Sidebar Toggle Logic
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // 2. Initialize Dashboard Chart if on the Student Dashboard
    const chartCanvas = document.getElementById('attendanceChart');
    if (chartCanvas) {
        initAttendanceChart("/attendance/analytics/");
    }

    // 3. Login Success Popup (Toast) Logic
    const toastEl = document.getElementById('loginToast');
    if (toastEl) {
        const loginToast = new bootstrap.Toast(toastEl, {
            delay: 5000,
            autohide: true
        });
        loginToast.show();
    }
});

/**
 * Activity Tracking Logic
 * Pings the server to log the start of a task before opening the resource.
 */
function trackActivityStart(activityId, externalLink) {
    // Get CSRF token for the POST request
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken');

    fetch(`/activities/start/${activityId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Log entry created successfully; open the external link (YouTube, LeetCode, etc.)
            window.open(externalLink, '_blank');
        } else {
            console.error('Activity Log Error:', data.message);
        }
    })
    .catch(error => console.error('Tracking Fetch Error:', error));
}

/**
 * Projector Live Feed Logic
 * Pings the server to update the list of present students in real-time.
 */
function startLiveAttendanceFeed(entryId) {
    const listContainer = document.getElementById('live-attendance-list');
    if (!listContainer || !entryId) return;

    const updateFeed = () => {
        fetch(`/attendance/live-feed/${entryId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.students.length > 0) {
                    listContainer.innerHTML = data.students.map(student => `
                        <div class="d-flex justify-content-between align-items-center p-2 mb-2 bg-light rounded-3 animate-in">
                            <span class="fw-bold small">${student.name}</span>
                            <span class="badge bg-success rounded-pill" style="font-size: 0.7rem;">${student.time}</span>
                        </div>
                    `).join('');
                }
            })
            .catch(error => console.error('Feed Error:', error));
    };

    setInterval(updateFeed, 3000); // 3-second refresh for the SIH demo
    updateFeed();
}

/**
 * Attendance Analytics Logic
 * Renders the line chart using Chart.js based on server data.
 */
function initAttendanceChart(endpointUrl) {
    const canvas = document.getElementById('attendanceChart');
    if (!canvas) return;

    fetch(endpointUrl)
        .then(response => response.json())
        .then(res => {
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: res.labels,
                    datasets: [{
                        label: 'Classes Attended',
                        data: res.data,
                        borderColor: '#0d6efd',
                        backgroundColor: 'rgba(13, 110, 253, 0.08)',
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        pointRadius: 4,
                        pointBackgroundColor: '#0d6efd'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: { backgroundColor: '#333', titleFont: { size: 12 } }
                    },
                    scales: {
                        y: {
                            display: true,
                            beginAtZero: true,
                            ticks: { stepSize: 1, color: '#999' },
                            grid: { color: 'rgba(0,0,0,0.05)' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: '#999' }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Analytics Error:', error));
}

// Helper to get CSRF token from cookies if hidden input is missing
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}