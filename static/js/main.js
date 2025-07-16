// static/js/main.js

// Initialize Bootstrap tooltips and other main JavaScript
document.addEventListener("DOMContentLoaded", function() {
    // Main JavaScript file for Student Organization app
    console.log("FocusFlow app loaded successfully!");

    // Bootstrap tooltips initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});