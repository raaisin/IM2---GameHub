document.addEventListener('DOMContentLoaded', function() {
    // Get the search query from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('q') || 'Unknown search term';
    
    document.getElementById('searchQuery').textContent = searchQuery;
});