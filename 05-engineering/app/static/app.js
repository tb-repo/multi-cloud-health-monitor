/**
 * Multi-Cloud Health Monitor - Dashboard JavaScript
 * Handles auto-refresh of health check data.
 */

// Auto-refresh the page every 30 seconds
const REFRESH_INTERVAL = 30000;

function updateLastRefreshTime() {
    const el = document.getElementById('last-refresh');
    if (el) {
        el.textContent = new Date().toLocaleTimeString();
    }
}

function autoRefresh() {
    updateLastRefreshTime();
    setTimeout(function() {
        window.location.reload();
    }, REFRESH_INTERVAL);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateLastRefreshTime();
    autoRefresh();
});
