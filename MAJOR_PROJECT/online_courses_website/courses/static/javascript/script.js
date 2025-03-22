document.addEventListener("DOMContentLoaded", function() {
    const searchButton = document.getElementById("search-btn");
    searchButton.addEventListener("click", function() {
        const searchQuery = document.getElementById("search-input").value;
        alert("You searched for: " + searchQuery);
    });
});
